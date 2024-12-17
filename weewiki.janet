(def personal-wiki-path "/wiki")
(def ww-dir "_site/recurse")
(def webroot (if (ww-server?) "/wiki" "/recurse"))
(import templates)

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

# I am bad at names
(defn pagelink (link &opt name)
  (def url (string webroot link))
  (if (nil? name)
    (org (string "[[" url "][" link "]]"))
    (org
     (string
      "[["
      url
      "]["
      name
      "]]"))))

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

(defn html-header [] (templates/header (ww-name)))
(defn html-footer [] (templates/footer (ww-name)))

(defn dzref [dzpath]
  (def split-path (string/split "/" dzpath))
  (def graph (string/join (array/slice split-path 0 (- (length split-path) 1)) "/"))
  (def node (split-path (- (length split-path) 1)))
  (org (string
    "&lt;&lt;"
    (refstr (string "dz/" graph) (string graph "/" node) node)
    "&gt;&gt;")))

(import tools/genhtml :as genhtml)
(defn dagzet-page [filepath]
  (genhtml/generate filepath webroot))

(genhtml/load-global-index "data_keys")

(import tools/logparse)

(defn wikiref [name]
  (org (string "[[" personal-wiki-path "/" name "][" name "]]")))

(defn taskref [task]
 (ref (logparse/generate-task-page-name task) task))

(defn img [path &opt alt]
  (print
   (string
    "<img src=\""
    path "\""
    (if-not (nil? alt) (string " alt=\"" alt "\""))
    ">")))


