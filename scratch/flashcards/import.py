from pprint import pprint
import sqlite3

fp = open("cards.tsv", "r")
db_path = "../../a.db"
db = sqlite3.connect(db_path)

print("About to overwrite data with saved data. Continue? [y/n]")
answer=input()
while answer != "y" and answer != "n":
    print("please answer y or n")
    answer=input()

if answer == "n":
    print("aborting")
    exit()

db.execute("CREATE TABLE IF NOT EXISTS flashcard_metadata(name STRING UNIQUE, level INTEGER, num_correct INTEGER)")

db.execute("DELETE FROM flashcard_metadata WHERE 1;")
db.commit()

for line in fp:
    (name, level, num_correct) = line.rstrip("\r\n").split("\t")
    print(name, level, num_correct)
    db.execute("INSERT INTO flashcard_metadata(name, level, num_correct) VALUES(?, ?, ?)", [name, level, num_correct])

db.commit()
db.close()
