# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import random
import requests
import time

hostName = "localhost"
serverPort = 8080
return_queue = []

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        global return_queue
        self.send_response(200)
        self.end_headers()
        return_queue.append(int(self.path[1:]))
        print(return_queue)


def prod_info():
    while True:
        # print("this works")
        requests.get("http://localhost:8081/" + str(random.randrange(0, 100)))
        time.sleep(3)

generator_threads = 6
generators = [threading.Thread(target=prod_info) for i in range(generator_threads)]

if __name__ == "__main__":
    for thread in generators:
        thread.start()
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")