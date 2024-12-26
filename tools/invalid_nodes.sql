SELECT substr(tag,4) as nodename FROM logtags
WHERE nodename NOT in
(SELECT substr(tag,4) as nodename FROM logtags
JOIN dz_nodes on dz_nodes.name = nodename
WHERE
tag LIKE 'dz:%')
AND tag LIKE 'dz:%'
;
