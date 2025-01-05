#!/bin/sh

abort()
{
    echo >&2 '
***************
*** ABORTED ***
***************
'
    echo "An error occurred. Exiting..." >&2
    exit 1
}

trap 'abort' 0

set -eo pipefail

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
    DROP TABLE IF EXISTS dz_noderefs;
EOF

LUA="mnolth lua"
GRAPH_DATA_DIR="dagzet/graph"
DAGZET_LUA="tools/dagzet.lua"


function dagzet_util()
{
    DZFILE=$1
    $LUA $DAGZET_LUA $DZFILE 

    if [[ ! $? -eq 0 ]]
    then
        exit 1
    fi
}

function add_to_dagzet() {
    #DZFILE=$1
    echo $*
    dagzet $* | sqlite3 a.db
}

function import_code() {
    NAMESPACE=$1
    FILENAME=$2
    $LUA \
        dagzet/util/import_file.lua \
        $NAMESPACE dagzet/code/$FILENAME | sqlite3 a.db
}

function import_dzfiles() {
    DZDIR=$1
    DB=$2
    # cd $LINE
    while read -r LINE
    do
        if [ -d "$LINE" ]
        then
            echo "DIRECTORIES NOT YET IMPLEMENTED"
            exit 1
        else
            echo $LINE
            dagzet $LINE | sqlite3 $DB
        fi
    done < $DZDIR/dzfiles.txt
    # cd -
}

import_dzfiles knowledge a.db

trap : 0
