(defn get-available-days [db]
  (sqlite3/eval db
    (string
      "SELECT distinct(day) as day FROM logs "
      "ORDER by day DESC;"
      )))

(defn get-day [db day]
  (sqlite3/eval db
    (string
      "SELECT day, time, title, comment, position "
      "FROM logs WHERE day is '" day "' "
      "AND category is '' "
      "ORDER by position;"
      )))

(defn get-logs-by-tag [db tag]
  (sqlite3/eval
    db
    (string
      "SELECT day, time, title, comment from logs "
      "INNER join logtags ON "
      "logs.rowid = logtags.logid "
      "WHERE logtags.tag is '" tag "' "
      "ORDER BY logs.rowid ASC ;"
      )))

(defn get-dayblurb [db day]
  (def q (sqlite3/eval
           db
           (string
             "SELECT day, title, blurb "
             "FROM dayblurbs WHERE day is '" day "' "
             )))

   (if (> (length q) 0) (q 0) nil))

(defn is-valid-key [x key]
  (not
    (or
      (nil? x)
      (nil? (x key)) (= (x key) ""))))

(defn format-comment [comment]
    (string/replace-all "---" "\n\n" comment))


(defn day-timestamp-html [day]
  (def id (string/replace-all "-" "_" day))
  (string 
    "<a href=\"#" id "\" id=\"" id "\">"
    day
    "</a>"
    ))

(defn day-timestamp-html-no-id [day]
  (def id (string/replace-all "-" "_" day))
  (string 
    "<a href=\"#" id "\">"
    day
    "</a>"
    ))

(defn day-entry-html [day time &opt fulldate]
  (default fulldate false)
  (def id
    (string
      (string/replace-all "-" "_" day) "_"
      (string/replace-all ":" "_" time)))

  (string 
    "<a href=\"#" id "\" id=\"" id "\">"
    (if fulldate (string day " " time) time)
    "</a>"
    ))


(defn print-org-comment [comment]
  (print "<div class=\"comment-block\">")
  (org (string comment "\n\n"))
  (print "</div>"))

(defn print-entry [row &opt fulldate]
  (default fulldate false)
  (print
    (string
      "<p>"
      (day-entry-html (row "day") (row "time") fulldate)
      ": "
      (row "title")
      "</p>"))
  (if-not (= (row "comment") "")
          (print-org-comment (format-comment (row "comment")))))

(defn render-day-entry [db day]
  (def day-rows (get-day db day))
  (def dayblurb (get-dayblurb db day))

  (org (string
         "** "
         (day-timestamp-html day)
         (if (is-valid-key dayblurb "title")
           (string " " (dayblurb "title")))
         "\n"))

  (print "<a href=\"#top\">jump to top</a>")

  (if (is-valid-key dayblurb "blurb")
    (org (string (format-comment (dayblurb "blurb")) "\n\n")))

  (each row day-rows
    (print-entry row)))

(defn generate-log-jumplink [db day]
  (def dayblurb (get-dayblurb db (day "day")))

  (string
    (day-timestamp-html-no-id (day "day"))
    (if (is-valid-key dayblurb "title")
      (string " " (dayblurb "title")))))

(defn render-daily-logs [db]
  (def days (get-available-days db))
  (print "<ul id=\"top\">")
  (each day days
    (print "<li>")
    (print (generate-log-jumplink db day))
    (print "</li>"))
  (print "</ul>")

  (each day days (render-day-entry db (day "day"))))

(defn get-task-row [db tag]
  (sqlite3/eval
    db
    (string
      "SELECT title, description FROM tasks WHERE "
      "name IS '" tag "'")))

(defn render-logs-from-tag [db tag]
  (def task-row (get-task-row db tag))
  (def task-desc ((task-row 0) "description"))
  (def task-title ((task-row 0) "title"))
  (org (string "#+TITLE " task-title "\n"))
  (if (> (length task-desc) 0)
    (org (string task-desc "\n\n")))
  (org (string "task id: " tag "\n\n"))
  (def logs (get-logs-by-tag db tag))
  (each log logs (print-entry log true)))

(defn get-tasks-from-group [db group]
  (sqlite3/eval db
    (string
      "SELECT name, title "
      "FROM tasks WHERE task_group is '" group "' "
      # TODO: add position
      "ORDER by name;"
      )))

(defn generate-task-page-name [task]
  (string "tasks/" (string/replace-all "-" "_" task)))

(defn print-task [task]
  (print "<li>")
  (ref
    (generate-task-page-name (task "name"))
    (task "name"))
  (org (string ": " (task "title")))
  (print "</li>"))

(defn render-tasks-from-group [db group]
  (def tasks (get-tasks-from-group db group))
  (org (string "#+TITLE " group "\n"))
  (print "<ul>")
  (each task tasks
    (print-task task)))

(defn get-taskgroups [db]
  (sqlite3/eval db
    (string
      "SELECT distinct(task_group) as task_group FROM tasks "
      "ORDER by task_group;"
      )))

(defn render-taskgroups-directory [db] 
  (def taskgroups (get-taskgroups db))
  (org "#+TITLE Task Groups\n")
  (print "<ul>")
  (each tg taskgroups
    (print "<li>")
    (ref (string "taskgroups/" (tg "task_group")) (tg "task_group"))
    (print "</li>"))
  (print "</ul>"))

(defn get-tasks [db]
  (sqlite3/eval db
    (string
      "SELECT name, title, task_group FROM tasks "
      "WHERE task_group is NOT 'done' "
      "ORDER by name;"
      )))

(defn render-tasks-directory [db] 
  (def tasks (get-tasks db))
  (org "#+TITLE Tasks\n")
  (each task tasks
    (org (string
           (refstr
             (generate-task-page-name (task "name"))
             (task "name"))
           ": "
           (task "title") " "
           "("
           (refstr
             (string "taskgroups/" (task "task_group"))
             (task "task_group"))
           ")"
           "\n\n"))))

