import unittest
from flashcards import Card

class TestFlashCards(unittest.TestCase):
    def test_card(self):
        card = Card(level=1, correct = 0)
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
        
