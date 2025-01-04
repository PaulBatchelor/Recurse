import sqlite3

con = sqlite3.connect("a.db")

cur = con.cursor()


cur.execute("CREATE TABLE IF NOT EXISTS logtagnodes(node INTEGER, logid INTEGER);");
con.commit()

rows = cur.execute(
    " ".join((
        "SELECT logid, substr(tag, 4) FROM logtags ",
        "WHERE",
        "tag LIKE 'nn:%';")
))

insert_query = ""

rows = rows.fetchall()

for row in rows:
    logid, tag = row
    print(logid, tag)
    insert = " ".join((
        "INSERT INTO dz_nodes(name)",
        f"VALUES('{tag}');"
    ))
    cur.execute(insert)
    insert = " ".join((
        "INSERT INTO logtagnodes(node, logid)",
        f"VALUES((SELECT id FROM dz_nodes WHERE name is '{tag}' LIMIT 1),"
        f"{logid});"
    ))

    cur.execute(insert_query)
con.commit()
