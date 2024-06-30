sqlite3 a.db <<EOM
DELETE FROM wiki WHERE key LIKE 'dzf/%'
EOM

function query() {
sqlite3 a.db <<EOM
SELECT distinct(filename) from dz_textfiles
EOM
}

function insert {
cat <<EOM
INSERT INTO wiki(key, value)
VALUES('dzf/$1', '@!(genhtml/textlines "$1")!@');
EOM
}

query | \
while read -r line
do
insert $line
done | sqlite3 a.db
