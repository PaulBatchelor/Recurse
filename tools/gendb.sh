sqlite3 a.db <<EOF
    DROP TABLE IF EXISTS dz_nodes;
    DROP TABLE IF EXISTS dz_connections;
    DROP TABLE IF EXISTS dz_connection_remarks;
    DROP TABLE IF EXISTS dz_lines;
    DROP TABLE IF EXISTS dz_remarks;
    DROP TABLE IF EXISTS dz_hyperlinks;
    DROP TABLE IF EXISTS dz_tags;
    DROP TABLE IF EXISTS dz_graph_remarks;
    DROP TABLE IF EXISTS dz_flashcards;
    DROP TABLE IF EXISTS dz_file_ranges;
    DROP TABLE IF EXISTS dz_images;
    DROP TABLE IF EXISTS dz_audio;
    DROP TABLE IF EXISTS dz_textfiles;
    DROP TABLE IF EXISTS dz_pages;
    DROP TABLE IF EXISTS dz_todo;
EOF

LUA="mnolth lua"
GRAPH_DATA_DIR="dagzet/graph"
DAGZET_LUA="tools/dagzet.lua"
function add_to_dagzet() {
    DZFILE=$1
    if [ -f $DZFILE ]
    then
        echo $DZFILE
        $LUA $DAGZET_LUA $DZFILE | sqlite3 a.db
    else
        echo "Warning: $DZFILE does not exist"
    fi

    if [[ ! $? -eq 0 ]]
    then
        exit 1
    fi
}

function import_code() {
    NAMESPACE=$1
    FILENAME=$2
    $LUA \
        dagzet/util/import_file.lua \
        $NAMESPACE dagzet/code/$FILENAME | sqlite3 a.db
}

add_to_dagzet knowledge/cargo_book.dz
add_to_dagzet knowledge/how_not_to_learn_rust.dz
add_to_dagzet knowledge/misc.dz
add_to_dagzet knowledge/rust.dz
add_to_dagzet knowledge/rust_by_example.dz
add_to_dagzet knowledge/rust_libs.dz
add_to_dagzet knowledge/software_foundations.dz
add_to_dagzet knowledge/workflow_planning.dz
