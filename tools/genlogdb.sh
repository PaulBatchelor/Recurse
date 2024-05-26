sqlite3 a.db <<EOM
    DROP TABLE IF EXISTS dayblurbs;
    DROP TABLE IF EXISTS logs;
EOM

while read -r line
do
    ./tools/evparse.sh $line | sqlite3 a.db
done < logs/logfiles.txt
