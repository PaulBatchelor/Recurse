(def css-path 
  (if (ww-server?)
    "/css/style.css"
    (string webroot "/css/style.css")))

(defn header-default []
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


(defn footer-default
  []
  (print
``
</div>
</body>
</html>
``
))

(defn use-template [pgname]
  (def path (string/split "/" pgname))
  (if (and (> (length path) 0) (= (path 0) "dzf"))
    false
    true))

(defn header [pgname]
  (if (use-template pgname)
    (header-default)))

(defn footer [pgname]
  (if (use-template pgname) (footer-default)))

# global mutable state hack for HTMLized files
