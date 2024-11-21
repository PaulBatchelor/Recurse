OUTFILE="cards.tsv"
sqlite3 ../../a.db > $OUTFILE <<EOM
.mode tabs
SELECT name, level, num_correct from flashcard_metadata
ORDER BY name ASC;
;
EOM

echo "Exported data to $OUTFILE"
