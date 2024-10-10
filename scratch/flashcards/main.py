import sys
from flashcards import FlashCards
from pprint import pprint

def main():
    flashcards = FlashCards()
    flashcards.open("../../a.db")

    # TODO: have this be a CLI parameter
    ncards = 3

    # load some potential values from disk into memory
    flashcards.fill_caches(ncards*2, min_cache_size=ncards)
    #flashcards.fill_caches(ncards*2)

    # generate a deck from the internal cache of values
    # this will read more data from disk, and load metadata
    deck = flashcards.generate_deck(ncards)

    # run through the program, return results
    results = flashcards.present(deck)

    # update the state of the cards of the deck, based
    # on the results of the presentation.
    new_deck = flashcards.update(results, deck)

    # save the states of the cards in new_deck to disk
    flashcards.save(new_deck)

    # close the database
    flashcards.close()
    return 0

if __name__ == '__main__':
    sys.exit(main())
