function query() {
sqlite3 a.db <<EOM
SELECT name from tasks;
EOM
}

function generate_insert_statement() {
    PAGE_NAME=$(echo $1 | tr "-" "_")
    PAGE_NAME="tasks/$PAGE_NAME"
    printf "INSERT INTO wiki(key, value) "
    printf "VALUES('$PAGE_NAME', "
    printf "'@!(logparse/render-logs-from-tag (ww-db) \"$1\")!@');\n"
}

function generate_sqlite () {
    while read -r line
    do
        generate_insert_statement $line
    done
}

function delete_previous_task_pages() {
    sqlite3 a.db <<EOM
DELETE FROM wiki WHERE key LIKE 'tasks/%'
EOM
}

delete_previous_task_pages
query | generate_sqlite | sqlite3 a.db
