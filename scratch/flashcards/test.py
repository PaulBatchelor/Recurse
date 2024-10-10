import unittest
from flashcards import Card

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
