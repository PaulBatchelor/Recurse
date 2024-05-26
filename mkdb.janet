# open and clear wiki db

(ww-open "a.db")
(ww-clear)

# unlinked pages


# linked pages

(ww-add-link "index" "wiki/index.org")

# sync and close

(ww-sync)
(ww-close)
