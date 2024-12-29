#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import json
from flashcards import FlashCards
from pprint import pprint
import socketserver
import threading

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
            "question": " ".join(card.front) if isinstance(card.front, list) else card.front,
            "answer": " ".join(card.back) if isinstance(card.back, list) else card.back,
            "num_correct": card.num_correct,
            "name": card.name,
        })

    return cards

class CustomSimpleHTTPRequestHandler(BaseHTTPRequestHandler):
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

def run_card_server():
    server = HTTPServer(('localhost', 8001), CustomSimpleHTTPRequestHandler)
    print('Server running on http://localhost:8001')
    server.serve_forever()

class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="webapp", **kwargs)

def run_file_server():
    PORT = 8000
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

def start_servers():
    card_server = threading.Thread(target=run_card_server)
    file_server = threading.Thread(target=run_file_server)

    card_server.start()
    file_server.start()

    try:
        card_server.join()
        file_server.join()
    except KeyboardInterrupt:
        print("Shutting down servers...")

start_servers()
