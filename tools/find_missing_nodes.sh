FILE=$1

PLEFT=""
PRIGHT=""

does_it_exist() {
    KEY=$1

    sqlite3 a.db <<EOM
SELECT count(name) FROM dz_nodes
WHERE NAME IS '$KEY'
EOM
}
run() {
    LEFT=$2
    RIGHT=$3

    if [ $LEFT == "^" ]
    then
        LEFT=$PLEFT
    fi

    if [ $RIGHT == "^" ]
    then
        RIGHT=$PRIGHT
    fi

    PLEFT=$LEFT
    PRIGHT=$RIGHT
    
    # EXISTS=$(get_counts $LEFT)

    EXISTS=$(does_it_exist $LEFT)
    if [ "$EXISTS" -lt 1 ]
    then
        echo $LEFT
    fi

    EXISTS=$(does_it_exist $RIGHT)
    if [ "$EXISTS" -lt 1 ]
    then
        echo $RIGHT
    fi
}

grep "^cx" < $FILE | \
while read -r LINE
do
    run $LINE
done
