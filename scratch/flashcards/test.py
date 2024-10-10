import unittest
from flashcards import Card, FlashCards

class TestFlashCards(unittest.TestCase):
    def test_card(self):
        card = Card(level=1, num_correct = 0)
        assert(card.level == 1)

        for _ in range(3): card.update(True)
        assert(card.level == 2)

        for _ in range(3): card.update(True)
        assert(card.level == 3)

        for _ in range(3): card.update(True)
        assert(card.level == 4)

        for _ in range(3): card.update(True)
        assert(card.level == 5)
        
        for _ in range(3): card.update(True)
        assert(card.level == 5)

    def test_card_rollback(self):
        card = Card(level=1, num_correct = 0)
        card.update(True)
        assert(card.num_correct == 1)
        card.update(True)
        card.update(False)
        card.update(True)
        assert(card.level == 1)
        assert(card.num_correct == 1)

    def test_flashcard_update(self):
        fc = FlashCards()
        deck = []
        cardvals = [
            {"level": 1, "num_correct": 0},
            {"level": 1, "num_correct": 2},
            {"level": 1, "num_correct": 2},
        ]

        results = [True, True, False]

        expected = [
            {"level": 1, "num_correct": 1},
            {"level": 2, "num_correct": 0},
            {"level": 1, "num_correct": 0},
        ]

        for i in range(len(cardvals)):
            card_data = cardvals[i]
            level = card_data["level"]
            num_correct = card_data["num_correct"]
            newcard = Card(level=level, num_correct=num_correct)
            deck.append(newcard)


        newdeck = fc.update(results, deck)

        for i in range(len(expected)):
            card = newdeck[i]
            assert(card.level == expected[i]["level"])
            assert(card.num_correct == expected[i]["num_correct"])
