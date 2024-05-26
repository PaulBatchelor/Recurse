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
    (string/replace-all "\n" "\n\n" comment))

(defn render-day-entry [db day]
  (def day-rows (get-day db day))
  (def dayblurb (get-dayblurb db day))

  (org (string
         "** "
         day
         (if (is-valid-key dayblurb "title")
           (string " " (dayblurb "title")))
           "\n"))

  (if (is-valid-key dayblurb "blurb")
      (org (string (format-comment (dayblurb "blurb")) "\n\n")))

  (each row day-rows
    (org
      (string
        "<span class=\"timestamp\">"(row "time")"</span>"
        ": "
        (row "title")
        "\n\n"))
    (if-not (= (row "comment") "")
      (org
        (string
          "<div class=\"comment-block\">"
          # line breaks in comments are doubled to trigger
          # paragraph breaks in org parser
          (row "comment")
          #(pp (string/replace-all "\n" "\n\n" (row "comment")))
          "</div>\n\n")))
  ))

(defn render-daily-logs [db]
  (def days (get-available-days db))
  (each day days (render-day-entry db (day "day"))))
