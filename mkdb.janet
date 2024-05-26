# open and clear wiki db

(ww-open "a.db")
(ww-clear)

# unlinked pages

(ww-add-page "dz/reading/how_not_to_learn_rust" `@!(dagzet-page "data/reading/how_not_to_learn_rust/index.json")!@`)
(ww-add-page "dz/reading" `@!(dagzet-page "data/reading/index.json")!@`)
(ww-add-page "dz/misc" `@!(dagzet-page "data/misc/index.json")!@`)
(ww-add-page "dz/career" `@!(dagzet-page "data/career/index.json")!@`)
(ww-add-page "dz/planning/workflow_planning" `@!(dagzet-page "data/planning/workflow_planning/index.json")!@`)
(ww-add-page "dz/planning" `@!(dagzet-page "data/planning/index.json")!@`)
(ww-add-page "dz/software_foundations/01_logical_foundations/02_induction" `@!(dagzet-page "data/software_foundations/01_logical_foundations/02_induction/index.json")!@`)
(ww-add-page "dz/software_foundations/01_logical_foundations/01_basics" `@!(dagzet-page "data/software_foundations/01_logical_foundations/01_basics/index.json")!@`)
(ww-add-page "dz/software_foundations/01_logical_foundations/00_preface" `@!(dagzet-page "data/software_foundations/01_logical_foundations/00_preface/index.json")!@`)
(ww-add-page "dz/software_foundations/01_logical_foundations" `@!(dagzet-page "data/software_foundations/01_logical_foundations/index.json")!@`)
(ww-add-page "dz/software_foundations" `@!(dagzet-page "data/software_foundations/index.json")!@`)
(ww-add-page "dz/web" `@!(dagzet-page "data/web/index.json")!@`)
(ww-add-page "dz/rust/books/rust_by_example" `@!(dagzet-page "data/rust/books/rust_by_example/index.json")!@`)
(ww-add-page "dz/rust/books/cargo_book" `@!(dagzet-page "data/rust/books/cargo_book/index.json")!@`)
(ww-add-page "dz/rust/books" `@!(dagzet-page "data/rust/books/index.json")!@`)
(ww-add-page "dz/rust/libs" `@!(dagzet-page "data/rust/libs/index.json")!@`)
(ww-add-page "dz/rust" `@!(dagzet-page "data/rust/index.json")!@`)
(ww-add-page "dz" `@!(dagzet-page "data/index.json")!@`)
(ww-add-page "logs" `#+TITLE: logs
I have developed a reasonably simple
text-based log format to keep
track of what I do day-to-day. These get parsed and turned
into SQLite tables, then those tables get presented here
in HTML.

@!(logparse/render-daily-logs (ww-db))!@
`)

# linked pages

(ww-add-link "index" "wiki/index.org")

# sync and close

(ww-sync)
(ww-close)
