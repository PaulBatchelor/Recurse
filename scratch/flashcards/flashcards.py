import sys
import sqlite3
import math
import random
from pprint import pprint
from pathlib import Path
import json
from copy import deepcopy

class Card:
    def __init__(self, level=1, front=None, back=None, num_correct=0, name=None):
        self.level = level
        self.front = front
        self.back = back
        self.num_correct = num_correct
        self.name = name

    def update(self, result):
        if result and self.level < 5:
            self.num_correct += 1
            if self.num_correct >= 3:
                self.num_correct = 0
                self.level += 1
        else:
            self.num_correct = 0

    def save(self, db):
        query = [
            "INSERT OR REPLACE INTO",
            "flashcard_metadata(name, level, num_correct)",
            "VALUES(",
            ",".join(["'" + self.name + "'", str(self.level), str(self.num_correct)]),
            ");"
        ]
        query = " ".join(query)
        db.execute(query)

class FlashCards:
    def __init__(self):
        self.cache = [None]*4
        self.bucket = []
        self.total_cache_size = 0

    def open(self, path="a.db"):
        if not Path(path).is_file():
            return error(f"Could not file databse f{path}")

        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS flashcard_metadata(name STRING UNIQUE, level INTEGER, num_correct INTEGER)")

    def preload(self):
        # check and see if there are more cards
        # in the dagzet flashcards table.
        # skip if they are the same

        carddiff = int(self.db.execute(" ".join([
            "SELECT",
            "(SELECT COUNT(*) FROM dz_flashcards) -",
            "(SELECT COUNT(*) FROM flashcard_metadata)"
        ])).fetchone()[0])

        if carddiff == 0:
            return

        print("Preloading")

        # find missing flash cards
        query = " ".join([
            "SELECT name FROM dz_flashcards",
            "INNER JOIN dz_nodes ON",
            "dz_nodes.id = dz_flashcards.node",
            "WHERE name not in"
            "(SELECT name from flashcard_metadata)",
        ])

        res = self.db.execute(query)

        # load results into card structure

        new_cards = []

        for row in res:
            new_cards.append(Card(name=row[0]))

        # save cards to metadata
        for card in new_cards:
            print(f"saving: {card.name}")
            card.save(self.db)

        self.db.commit()

    def read_cards_from_disk(self, ncards, level=1):
        query = " ".join([
            "SELECT name FROM dz_flashcards",
            "INNER JOIN dz_nodes ON node=id",
            f"order by RANDOM() limit {ncards}"
        ])
        cards = []

        res = self.db.execute(query)
        for row in res:
            cards.append(row[0])

        return cards

    def fill_caches(self, total_cache_size, min_cache_size=None):
        # load cards of the 4 levels into separate
        # caches. Load more than needed to compensate
        # for randomness: 2N cards ought to do it

        # random distribution is done with fibonacci proportions
        # level 1 is the most likely, level 4 least likely.
        # looks like this: 4332221111

        min_cache_size = min_cache_size or total_cache_size

        ncards = [
            # level 1 has 5/11 cards, or ~45%
            math.floor(total_cache_size * (5/11)),

            # level 2 has 3/11 cards, or ~27%
            math.floor(total_cache_size * (3/11)),

            # level 3 has 2/11 cards, or ~18%
            math.floor(total_cache_size * (2/11)),

            # let it be remainder
            0,
        ]

        # level 4 has 1/11 cards, or ~9%
        # make level 4 be the remainder of cards so far
        ncards[3] = total_cache_size - sum(ncards)

        # attempt to fill caches
        # TODO: if a cache for a particular level misses
        # quota, how to compensate?

        db = self.db

        # if (total_flashcards > total_metadata):
        #     # get a bucket of flashcards not being tracked
        #     # by the metadata

        ncached = 0
        for lvl in range(4):
            print(f"filling cache for level {lvl} ({ncards[lvl]} cards)")
            self.cache[lvl] = self.read_cards_from_disk(ncards[lvl], lvl)
            ncached += len(self.cache[lvl])

        if ncached < total_cache_size:
            needed = total_cache_size - ncached
            print(f"Attempting to bucket {needed} more cards")
            query = " ".join([
                "SELECT name FROM dz_flashcards",
                "INNER JOIN dz_nodes ON",
                "dz_nodes.id = dz_flashcards.node",
                "WHERE name not in"
                "(SELECT name from flashcard_metadata)",
                "ORDER BY random()",
                f"LIMIT {needed};"
            ])
            res = db.execute(query)
            bucket = []
            for row in res:
                bucket.append(row[0])
            self.bucket = bucket

        total_loaded = len(self.bucket) + ncached
        # fatal error if minimum cache size not met
        if total_loaded < min_cache_size:
            print(f"Could not load cache of size {min_cache_size}, got {total_loaded} instead")
            exit(1)

        self.total_cache_size = total_loaded

        # TODO: how/when to recycle cards from level 5?

        # TODO: how to ignore cards?

    def name_to_card(self, name):
        if name is None:
            return
        data = self.db.execute(" ".join([
            "SELECT front, back",
            "FROM dz_flashcards",
            "INNER join dz_nodes ON id=node",
            f"WHERE name is '{name}'",
            "LIMIT 1"
        ])).fetchone()

        metadata = self.db.execute(" ".join([
            "SELECT level, num_correct",
            "FROM flashcard_metadata",
            f"WHERE name IS '{name}'"
        ])).fetchone()

        front = " ".join(json.loads(data[0]))
        back = " ".join(json.loads(data[1]))
        card = Card(name=name, front=front, back=back)

        if metadata:
            card.level = metadata[0]
            card.num_correct = metadata[1]

        return card

    def generate_deck(self, ncards):
        # ncards is the requested amount, but that might
        # not be guaranteed if there aren't that many cards
        # to choose from


        # - determine total cache size, and change card
        #   request size if too large

        if ncards > self.total_cache_size:
            ncards = self.total_cache_size

        # discrete random distribution
        rd = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        rd_len = len(rd)

        deck = []
        deck_set = set()

        for _ in range(ncards):
            # pick a level 1-4 from distributed RNG
            level = rd[random.randrange(rd_len)] - 1
            card = None

            # attempt to pop value from corresponding cache
            if len(self.cache[level]) > 0:
                card = self.cache[level].pop()
            else:
                # sweep through other level caches to find
                # a card
                for i in range(3):
                    newlevel = (level + i) % 4
                    if len(self.cache[newlevel]) > 0:
                        card = self.cache[newlevel].pop()

            # fallback: select card from bucket
            if card is None and len(self.bucket) > 0:
                card = self.bucket.pop()

            # quick fix: avoid duplicates, even if it means we
            # miss a card
            if card not in deck_set:
                deck_set.add(card)
                deck.append(self.name_to_card(card))

        return deck

    def present(self, deck):
        results = []
        result_lookup = {"y":True, "n":False}
        for card in deck:
            print("Card: " + card.name)
            print("Front: " + card.front)
            input()
            print("Back: " + card.back)
            print("Got it right? [y/n]")
            answer = input()
            print("answer", answer)
            while answer != "y" and answer != "n":
                print("Please answer y or n.")
                answer = input()

            results.append(result_lookup[answer])

        return results

    def update(self, results, deck):
        new_deck = []
        # Go through each of the results, and apply
        # result to the card deck. This will update the
        # state properly

        for i in range(0, len(results)):
            card = deepcopy(deck[i])
            card.update(results[i])
            new_deck.append(card)

        return new_deck

    def save(self, deck):
        # self.db.execute("INSERT into flashcard_metadata(name, level, num_correct) VALUES('foo', 22, 22)")
        for card in deck:
            print(f"saving {card.name}")
            card.save(self.db)
            # print(f"saving {card.name}")
            # query = [
            #     "INSERT OR REPLACE INTO",
            #     "flashcard_metadata(name, level, num_correct)",
            #     "VALUES(",
            #     ",".join(["'" + card.name + "'", str(card.level), str(card.num_correct)]),
            #     ");"
            # ]
            # query = " ".join(query)
            # self.db.execute(query)
        self.db.commit();

    def close(self):
        self.db.close()
