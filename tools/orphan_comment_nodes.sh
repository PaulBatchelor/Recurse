sqlite3 a.db <<EOM
.mode line
SELECT day, title, logid, substr(tag,4) as nodename FROM logtags
INNER join logs on logs.rowid = logtags.logid
WHERE nodename NOT in
(SELECT substr(tag,4) as nodename FROM logtags
JOIN dz_nodes on dz_nodes.name = nodename
WHERE
tag LIKE 'dz:%')
AND tag LIKE 'dz:%'
;
EOM
