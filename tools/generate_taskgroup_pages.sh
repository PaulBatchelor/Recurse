function query() {
    sqlite3 a.db <<EOM
    SELECT distinct(task_group) from tasks
    ORDER by task_group;
EOM
}

function generate_insert_statement() {
    PAGE_NAME=$(echo $1 | tr "-" "_")
    PAGE_NAME="taskgroups/$PAGE_NAME"
    printf "INSERT INTO wiki(key, value) "
    printf "VALUES('$PAGE_NAME', "
    printf "'@!(logparse/render-tasks-from-group (ww-db) \"$1\")!@');\n"
}

function generate_sqlite () {
    while read -r line
    do
        generate_insert_statement $line
    done
}

function delete_previous_pages() {
    sqlite3 a.db <<EOM
DELETE FROM wiki WHERE key LIKE 'taskgroups%'
EOM
}

function create_directory_listing() {
    sqlite3 a.db <<EOM
INSERT INTO wiki(key, value)
VALUES('taskgroups', '@!(logparse/render-taskgroups-directory (ww-db))!@')
EOM
}

delete_previous_pages
query | generate_sqlite | sqlite3 a.db
create_directory_listing
