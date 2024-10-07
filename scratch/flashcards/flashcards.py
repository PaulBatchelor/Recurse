import sys

class Card:
    def __init__(self, level=1, front=None, back=None, correct=0):
        self.level = level
        self.front = front
        self.back = back
        self.correct = correct

    def update(self, result):
        if result and self.level < 5:
            self.correct += 1
            if self.correct >= 3:
                self.correct = 0
                self.level += 1

class FlashCards:
    def __init__(self, path="a.db"):
        pass

    def fill_caches(self, ncards):
        pass

    def generate_deck(self):
        pass

    def present(self, deck):
        pass

    def update(self, results, deck):
        pass

    def save(self, deck):
        pass

    def close(self):
        pass
