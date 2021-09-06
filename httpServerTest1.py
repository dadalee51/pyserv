import http.server
import socketserver
PORT = 8000
h= http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), h) as sv:
    print("server started...")
    sv.serve_forever()
    

