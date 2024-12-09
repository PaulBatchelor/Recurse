from http.server import HTTPServer, BaseHTTPRequestHandler
import json

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
            cards = [{
                "question": "A question from the backend?",
                "answer": "no, it can't be!",
            }]
            self.wfile.write(json.dumps(cards).encode())
        else:
            self.send_error(404)

    def do_POST(self):
        # Handle POST requests similarly
        pass

server = HTTPServer(('localhost', 8001), SimpleHTTPRequestHandler)
print('Server running on http://localhost:8001')
server.serve_forever()