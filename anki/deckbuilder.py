import genanki
import sqlite3
import json

def from_dagzet(cur=None, prefix = "", deckname="Dagzet deck", outfile="out.apkg"):
    cur = con.cursor()

    model = genanki.Model(
      1607392319,
      'Simple Model',
      fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'Path'},
      ],
      templates=[
        {
          'name': 'Card 1',
          'qfmt': '<div><i>{{Path}}</i></div><div><h3>{{Question}}</h3></div>',
          'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
      ])

    deck = genanki.Deck(
      2059400110,
      deckname)

    rows = cur.execute("\n".join((
        "SELECT name, front, back FROM dz_flashcards",
        "INNER JOIN dz_nodes on dz_flashcards.node = dz_nodes.id",
        f"WHERE name like '{prefix}%'",
        "ORDER BY name",
        ";",
        )))

    for card in rows:
        name, front, back = card
        front = " ".join(json.loads(front))
        back = " ".join(json.loads(back))
        note = genanki.Note(
          model=model,
          fields=[front, back, name])
        deck.add_note(note)


    genanki.Package(deck).write_to_file(outfile)

if __name__ == "__main__":
    args = ["DZ Deck", "anki_test", "test.apkg"]
    con = sqlite3.connect("../a.db")
    cur = con.cursor()
    with open("decks.txt") as fp:
        for line in fp:
            deckname, prefix, outfile = line[:-1].split(":")
            print(deckname, prefix, outfile)
            from_dagzet(cur=cur, prefix=prefix, deckname=deckname, outfile=outfile)
