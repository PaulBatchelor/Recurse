import sys
from flashcards import FlashCards

def main():
    flashcards = FlashCards("../../a.db")

    # TODO: have this be a CLI parameter
    ncards = 10

    # load some potential values from disk into memory
    flashcards.fill_caches(ncards)

    # generate a deck from the internal cache of values
    # this will read more data from disk, and load metadata
    deck = flashcards.generate_deck()

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
