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

    def fill_caches(self, total_cache_size):
        # load cards of the 4 levels into separate
        # caches. Load more than needed to compensate
        # for randomness: 2N cards ought to do it

        # random distribution is done with fibonacci proportions
        # level 1 is the most likely, level 4 least likely.
        # looks like this: 4332221111

        # level 1 has 5/11 cards, or ~45%
        # level 2 has 3/11 cards, or ~27%
        # level 3 has 2/11 cards, or ~18%
        # level 4 has 1/11 cards, or ~9%
        # make level 4 be the remainder of cards

        # attempt to fill caches
        # TODO: if a cache for a particular level misses
        # quota, how to compensate?
        
        # TODO: if the total number of cards falls short,
        # how to compensate?

        # TODO: how/when to recycle cards from level 5?

        # TODO: how to ignore cards?

        pass

    def generate_deck(self, ncards):
        # ncards is the requested amount, but that might
        # not be guaranteed if there aren't that many cards
        # to choose from

        # - determine total cache size, and change card
        #   request size if too large
        # - begin loop
        # - pick a level 1-4 from distributed RNG
        # - attempt to pop value from corresponding cache
        # - if the cache is empty, try to pop from neighboring
        #   caches. There should be a card somewhere...
        # - once a card has been found, load the card data
        #   from disk. This is the front/back content as
        #   well as any persisted metadata from previous
        #   flashcard sessions.
        # - end loop
        # return the deck
        pass

    def present(self, deck):
        # this will start ncurses
        # event loop:
        # present front of card
        # hit space
        # present front and back of card
        # correct answer? Y/N
        # mark response, go to next card
        pass

    def update(self, results, deck):
        # TODO: write words
        pass

    def save(self, deck):
        # TODO: write words
        pass

    def close(self):
        # TODO: write words
        pass
