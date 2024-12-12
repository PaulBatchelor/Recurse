from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from flashcards import FlashCards
from pprint import pprint

def generate_flashcard_data():
    flashcards = FlashCards()
    flashcards.open("../../a.db")

    # check for new cards and load them into flashcard memory
    flashcards.preload()

    # TODO: have this be a CLI parameter
    ncards = 10

    # load some potential values from disk into memory
    flashcards.fill_caches(ncards*2, min_cache_size=ncards)
    #flashcards.fill_caches(ncards*2)

    # generate a deck from the internal cache of values
    # this will read more data from disk, and load metadata
    deck = flashcards.generate_deck(ncards)

    cards = []

    for card in deck:
        cards.append({
            "question": card.front,
            "answer": card.back,
            "num_correct": card.num_correct,
            "name": card.name,
        })

    return cards

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Home Page')
        elif self.path == '/about':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'About Page')
        elif self.path == '/v1/get/flashcards':
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            cards = generate_flashcard_data()
            self.wfile.write(json.dumps(cards).encode())
        else:
            self.send_error(404)

    def do_POST(self):
        # Handle POST requests similarly
        pass

server = HTTPServer(('localhost', 8001), SimpleHTTPRequestHandler)
print('Server running on http://localhost:8001')
server.serve_forever()