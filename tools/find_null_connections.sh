FILE=knowledge/zzz.dz

function name_exists() {
    NAME=$1
    echo "SELECT count(*) == 1 FROM dz_nodes WHERE name is '$1'" | sqlite3 a.db
}

PLEFT=""
PRIGHT=""

grep "^cx " < $FILE |\
   while read -r line
   do
       LEFT=$(echo $line | cut -d ' ' -f 2)
       RIGHT=$(echo $line | cut -d ' ' -f 3)
       if [ $LEFT == "^" ]
       then
           LEFT=$PLEFT
       fi

       if [ $RIGHT == "^" ]
       then
            RIGHT=$PRIGHT
       fi

       if [ $(name_exists $LEFT) == "0" ]
       then
           echo "Bad left connection"
           echo $LEFT $RIGHT
           exit 1
       fi

       if [ $(name_exists $RIGHT) == "0" ]
       then
           echo "Bad right connection"
           echo $LEFT $RIGHT
           exit 1
       fi

       PLEFT=$LEFT
       PRIGHT=$RIGHT
   done
