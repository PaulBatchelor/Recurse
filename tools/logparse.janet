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

  (if (is-valid-key dayblurb "blurb")
    (org (string (format-comment (dayblurb "blurb")) "\n\n")))

  (each row day-rows
    (print-entry row)))

(defn render-daily-logs [db]
  (def days (get-available-days db))
  (each day days (render-day-entry db (day "day"))))


(defn render-logs-from-tag [db tag]
  (org (string "#+TITLE " tag))
  (def logs (get-logs-by-tag db tag))
  (each log logs (print-entry log true)))
