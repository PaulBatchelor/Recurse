(defn get-available-days [db]
  (sqlite3/eval db
    (string
      "SELECT distinct(day) as day FROM logs "
      "ORDER by day DESC;"
      )))

(defn get-day [db day]
  (sqlite3/eval db
    (string
      "SELECT time, title, comment, position "
      "FROM logs WHERE day is '" day "' "
      "ORDER by position;"
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

(defn day-entry-html [day time]
  (def id
    (string
      (string/replace-all "-" "_" day) "_"
      (string/replace-all ":" "_" time)))

  (string 
    "<a href=\"#" id "\" id=\"" id "\">"
    time
    "</a>"
    ))


(defn print-org-comment [comment]
  (print "<div class=\"comment-block\">")
  (org (string comment "\n\n"))
  (print "</div>"))

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
    (print
      (string
        "<p>"
        (day-entry-html day (row "time"))
        ": "
        (row "title")
        "</p>"))
    (if-not (= (row "comment") "")
            (print-org-comment (format-comment (row "comment"))))
  ))

(defn render-daily-logs [db]
  (def days (get-available-days db))
  (each day days (render-day-entry db (day "day"))))
