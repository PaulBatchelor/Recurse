(defn generate [data-filepath &opt webroot]
 (default webroot "/wiki")
 (def fp (file/open data-filepath))
 (def page-data (json/decode (file/read fp :all)))
 (def namespace (page-data "namespace"))
 (def gnodes (page-data "nodes"))
 (def positions (page-data "positions"))
 (def tree (page-data "tree"))
 (def subgraphs (sort (page-data "subgraphs")))

 (defn generate-marker-name [namespace name]
#(string (string/replace-all "/" "-" namespace) "-" name)
  name)

 (defn html-header
  []
  (print
   (string/format ``<!DOCTYPE html>
    <html lang="en">
    <head>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="%s">

    </head>
    <body>
    <div id="main">
    `` "style.css"))
 )

 (defn html-footer
  []
  (print
   ``
   </div>
   </body>
   </html>
   ``
  ))

 (defn is-external-node? [name]
# anything that has a backslash in the name is
# considsered to be an "external node" outside
# the current namespace.
  (not (nil? (string/find "/" name))))

# if external node name shares stuff in common with
# the current namespace, remove the common bits to
# remove clutter
 (defn display-name [namespace name]
  (string/replace (string namespace "/") "" name))

# external nodes are part of a subgraph
# so /foo/bar/cat would be foo/bar#cat
 (defn ext-path-with-marker [name]
  (def path (string/split "/" name))
  (string
   (string/join
    (array/slice path 0 (- (length path) 1))
    "/")
   "#"
   (path (- (length path) 1))))

    (defn html-ext-link-str [namespace name &opt remark]
     (default remark nil)
     (string "<a href=\""
      webroot
      "/dz/" (ext-path-with-marker name) "\">"
      (display-name namespace name) "</a>"
      (if-not (nil? remark)
       (string " (" (string/join remark ",")")"))))

    (defn html-jump-link-str [namespace name &opt remark]
     (default remark nil)
     (string "<a href=#" (generate-marker-name namespace name) ">"
      name "</a>"
      (if-not (nil? remark)
       (string " (" (string/join remark ",")")"))))

    (defn html-link-str [namespace name &opt remark]
     (default remark nil)
     (if (is-external-node? name)
      (html-ext-link-str namespace name remark)
      (html-jump-link-str namespace name remark)))

    (defn html-jump-link [namespace name]
     (prin (html-jump-link-str namespace name)))

    (defn html-ext-link [namespace name]
     (prin (html-ext-link-str namespace name)))

    (defn html-link [namespace name]
     (if (is-external-node? name)
      (html-ext-link namespace name)
      (html-jump-link namespace name)))

    (defn html-marker [namespace name &opt permalink]
     (default permalink true)
     (print
      (string
       "<a id=\""
       (generate-marker-name namespace name) "\""
       ">"
       (if permalink (html-link namespace name) name)
       "</a>")))

    (defn link-with-remark [namespace link]
     (html-link-str namespace (link "name") (link "remarks")))

    (defn generate-jump-links [namespace nodes]
     (var links @[])
     (each c nodes
      (if (string? c)
       (array/push links (html-link-str namespace c))
       (array/push links (link-with-remark namespace c))
      ))
     (string/join links ", "))

    (defn children-links [namespace children]
     (generate-jump-links namespace children))

    (defn parent-links [namespace parents]
     (generate-jump-links namespace parents))

    (defn escape-html [str]
     (string/replace-all
      ">" "&gt;"
      (string/replace-all "<" "&lt;" str)))
    (defn table-keyval [key val &opt escape]
     (default escape false)
     (print "<tr>")
     (print "<td>")
     (print key)
     (print "</td>")
     (print "<td>")
     (if escape
      (print (escape-html val))
      (print val))
     (print "</td>")
     (print "</tr>"))

    (defn any-messages? [namespace node-name]
     (def rows
      (sqlite3/eval (ww-db)
       (string
        "SELECT COUNT(value) == 1 as result FROM wikizet "
        "WHERE value is '@" namespace "/" node-name "'"
        " LIMIT 1;")))
     (= ((rows 0) "result") 1))

    (defn get-zet-messages [namespace node-name]
     (def rows
      (sqlite3/eval (ww-db)
       (string
        "WITH messages as ("

        "SELECT "
        "strftime('%Y-%m-%d %H:%M:%S', time, 'localtime') as time, "
        "UUID, value FROM wikizet "
        "WHERE value like '>%'"
        "),"
        "node_rows as ("
        "SELECT UUID from wikizet "
        "WHERE value like '#' || '"
        (ww-zet-resolve (string "@" namespace "/" node-name))
        "'"
        ")"
        "SELECT * from messages "
        "WHERE messages.UUID in node_rows")))
     rows)

    (defn display-zet-messages [rows] 
     (each row rows
      (print
       "<p>"
       (row "time") " "
       (string/slice (row "value") 1 -1)
       "</p>")))

    (defn generate-node-card [nd namespace]
     (print "<table border=\"1px\">")
     (print "<tr>")
     (print "<td colspan=2>")
     (html-marker namespace (nd "name"))
     (print "</td>")
     (print "</tr>")
     (if-not (nil? (nd "lines"))
      (table-keyval
       "content"
       (string/join (nd "lines") " ") true))

     (if-not (empty? (nd "children"))
      (table-keyval
       "children"
       (children-links namespace (nd "children"))))

     (if-not (empty? (nd "parents"))
      (table-keyval
       "parents"
       (parent-links namespace (nd "parents"))))

     (if-not (nil? (nd "remarks"))
      (table-keyval
       "remarks"
       (string/join (nd "remarks") " ")))

     (if-not (nil? (nd "hyperlink"))
      (table-keyval
       "hyperlink"
       (string "<a href=\""
        (nd "hyperlink")
        "\">"
        (nd "hyperlink")
        "</a>")
      ))

     (if-not (nil? (nd "tags"))
      (table-keyval
       "tags" (string/join (nd "tags") ", ")))

     (if-not (nil? (nd "flashcard"))
      (do
       (def card (nd "flashcard"))
       (if-not (nil? (card "front"))
        (table-keyval
         "flashcard (front)" (string/join (card "front") " "))
       )
       (if-not (nil? (card "back"))
        (table-keyval
         "flashcard (back)" (string/join (card "back") " "))
       )
      ))

     (if-not (nil? (nd "image"))
      (table-keyval
       "image"
       (string
        "<img src=\"/res/recurse/dz/"
        (nd "image")
        "\">")
      ))

     (if-not (nil? (nd "audio"))
      (table-keyval
       "audio"
       (string
        "<audio controls>"
        "<source src=\"/res/recurse/dz/"
        (nd "audio")
        "\"><audio>")
      ))

     (if-not
       (nil? (nd "file_ranges"))
       (table-keyval
         "file reference"
         (string
           ((nd "file_ranges") "filename")
           ":"
           ((nd "file_ranges") "start")
           (if-not
             (nil? ((nd "file_ranges") "end"))
             (string "-" ((nd "file_ranges") "end"))))))

     (print "</table><br>")

     (if (any-messages? namespace (nd "name"))
      (display-zet-messages
       (get-zet-messages namespace (nd "name")))))

       (defn node-card [nd namespace]
        (if-not (is-external-node? (nd "name"))
         (generate-node-card nd namespace)))

(defn get-node-name [nd] (if (string? nd) nd (nd 0)))

    (defn generate-node-list [top-node]
#(print "<ul>")
     (print "<li>")
     (html-link namespace (get-node-name top-node))

     (if (array? top-node)
      (do
       (print "<ul>")
       (each nd (top-node 1) (generate-node-list nd))
       (print "</ul>")))

     (print "</li>")
#(print "</ul>")
    )

    (defn extract-local-name [namespace]
     (let
      (vals (string/split "/" namespace))
      (vals (- (length vals) 1))))

    (defn subgraph-link [sg &opt webroot]
     (default webroot "/wiki")
     (string
      "<a href=\""
      webroot "/dz/"
      namespace (if (> (length namespace) 0) "/") sg
      "\">"
      sg
      "</a>"))

    (defn namespace-as-links [namespace &opt webroot]
     (default webroot "/wiki")
     (def names (string/split "/" (string "dz/" namespace)))
     (var namelinks @[])
     (var names-so-far @[])
     (each n names
      (array/push
       namelinks
       (string
        "<a href=\""
        webroot "/"
        (string/join names-so-far "/")
        (if (> (length names-so-far) 0) "/") n
        "\">"
        n
        "</a>"))
      (array/push names-so-far n))
     (print (string/join namelinks " / "))
    )
# Begin page generation

    (print (string "<title>" namespace "</title>"))
    (print (string "<h1>" (extract-local-name namespace)  "</h1>"))
    (print (string "<p>" (namespace-as-links namespace webroot) "</p>"))

    (if-not (nil? (page-data "remarks"))
     (do
      (print "<h2>Summary</h2>")
      (print "<p>")
      (print (string/join (page-data "remarks") " "))
      (print "</p>")))

(if (> (length subgraphs) 0)
 (do
  (print "<h2>Subgraphs</h2>")
  (print "<ul>")
  (each sg subgraphs
   (print (string "<li>" (subgraph-link sg webroot) "</li>")))
  (print "</ul>")))

(if (> (length tree) 0)
 (do
  (print (string "<h2>Node Tree</h2>"))
  (print "<ul>")
  (each nd tree
   (generate-node-list nd))
  (print "</ul>")))

    (defn sort-nodes-by-pos [nodes]
     (sorted-by (fn [x] (x "position")) nodes))

(if (> (length gnodes) 0)
 (do
  (print (string "<h2>Nodes</h2>"))
  (each nd (sort-nodes-by-pos gnodes) (node-card nd namespace))))

(file/close fp))

(defn get-link-rows [db]
 (def query (sqlite3/eval db
             (string
              "SELECT tag, group_concat(substr(name, 7), \",\") as nodes "
              "FROM dz_nodes "
              "INNER JOIN dz_tags ON dz_tags.node = dz_nodes.id "
              "WHERE name like \"links/%\""
              "GROUP by tag "
              "ORDER by tag ASC;")))
  query)

(defn htmlize-nodes [nodes]
 (def links @[])
 (each nd nodes
  (array/push links (refstr "dz/links" nd nd)))
 (org (string/join links ", ")))

(defn generate-links-table []
  (def link-rows (get-link-rows (ww-db)))
  (print "<table>")
  (print "<thead>")
  (print "<tr>")
  (print "<th scope=\"col\">tag</th>")
  (print "<th scope=\"col\">nodes</th>")
  (print "</tr>")
  (print "</thead>")

  (print "<tbody>")

  (each row link-rows
    (print "<tr>")
    (print (string "<td>" (row "tag") "</td>"))
    (print (string "<td>"))
    (htmlize-nodes (string/split "," (row "nodes")))
    (print "</td>")
    (print "</tr>"))

  (print "</tbody>")
  (print "</table>"))


(defn get-link-rows-by-tag [db tag]
 (def link-rows @{})
 (def query (sqlite3/eval db
             (string
              "SELECT substr(name, 7) as name, lines, hyperlink FROM dz_nodes "
              "INNER JOIN "
              "dz_tags ON dz_tags.node = dz_nodes.id, "
              "dz_lines ON dz_lines.node = dz_nodes.id, "
              "dz_hyperlinks ON dz_hyperlinks.node = dz_nodes.id "
              "WHERE name like 'links/%' "
              "AND tag like '" tag "' "
              "ORDER by name ;")))
  query)

(defn links-by-tag [tag]
 (def rows (get-link-rows-by-tag (ww-db) tag))

 (each row rows
  (org (string
    (refstr "dz/links" (row "name") (row "name")) ": "))
  (org (string/join (json/decode (row "lines")) " "))
  (org (string " [[" (row "hyperlink") "]]"))
  (org "\n")
 ))
