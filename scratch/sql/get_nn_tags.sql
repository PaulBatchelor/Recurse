SELECT logid, substr(tag, 4) FROM logtags
WHERE
tag LIKE 'nn:%'
;
