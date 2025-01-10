NODE=$1
sqlite3 a.db <<EOM
.mode lines
SELECT substr(tag, 4) as node, group_concat(distinct(day))
AS days FROM logtags
INNER JOIN logs ON logs.rowid = logtags.logid
WHERE tag LIKE 'dz:$NODE'
GROUP by node
ORDER by day DESC, time DESC
LIMIT 10
;
EOM
