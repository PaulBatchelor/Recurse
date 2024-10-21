sqlite3 ../../a.db <<EOM
.mode tabs
SELECT name, level, num_correct from flashcard_metadata
ORDER BY name ASC;
;
EOM
