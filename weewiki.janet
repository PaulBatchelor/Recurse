(def personal-wiki-path "/wiki")
(def ww-dir "_site/recurse")
(def webroot (if (ww-server?) "/wiki" "/recurse"))
(def css-path 
  (if (ww-server?)
    "/css/style.css"
    (string webroot "/css/style.css")))

(defn pgexists? (name)
  (var db (ww-db))
  (var x
       (sqlite3/eval
        db (string
            "SELECT EXISTS(SELECT key from wiki "
            "where key is \""name"\") as doiexist;")))
  (= ((x 0) "doiexist") 1))

(defn pglink (page &opt target)
  (var link "")
  (if (nil? target)
    (set link page)
    (set link (string page "#" target)))
  (cond
    (= page "index")
    (string webroot "/")
    (pgexists? page)
    (string webroot "/" link) "#"))

(defn refstr (link &opt name target)
  (default target nil)
  (if (nil? name)
    (string "[[" (pglink link) "][" link "]]")
    (string
      "[["
      (pglink link target)
      "]["
      name
      "]]")))

(defn ref (link &opt name target)
  (default target nil)
  (if (nil? name)
    (org (string "[[" (pglink link) "][" link "]]"))
    (org
     (string
      "[["
      (pglink link target)
      "]["
      name
      "]]"))))

(defn html-header []
  (print
    (string/join
      @["<!DOCTYPE html>"
        "<html lang=\"en\">"
        "<head>"
        "<meta charset=\"utf-8\">"
        (string
          "<link rel=\"stylesheet\" href=\""
          css-path
          "\">")
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\" />"
        "</head>"
        "<body>"
        "<div id=\"main\">"] "\n")))

(defn html-footer
  []
  (print
``
</div>
</body>
</html>
``
))

(import tools/genhtml :as genhtml)
(defn dagzet-page [filepath]
  (genhtml/generate filepath webroot))

(import tools/logparse)

(defn wikiref [name]
  (org (string "[[" personal-wiki-path "/" name "][" name "]]")))
