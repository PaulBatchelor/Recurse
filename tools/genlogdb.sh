sqlite3 a.db <<EOM
    DROP TABLE IF EXISTS dayblurbs;
    DROP TABLE IF EXISTS logs;
    DROP TABLE IF EXISTS logtags;
EOM

while read -r line
do
    echo $line
    ./tools/evparse.sh $line | sqlite3 a.db
done < logs/logfiles.txt
