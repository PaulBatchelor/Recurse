import sqlite3

db = sqlite3.connect("a.db").cursor()


rows = db.execute(
    " ".join((
        "SELECT logid, substr(tag, 4) FROM logtags ",
        "WHERE",
        "tag LIKE 'nn:%';")
))


for row in rows:
    logid, tag = row
    print(logid, tag)
