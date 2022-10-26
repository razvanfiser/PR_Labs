from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import requests
import threading

hostName = "localhost"
serverPort = 8081
li = []
li2 = []

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        global li
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        li.append(int(self.path[1:]))
        print(("l1: ", li))

    def do_POST(self):
        global li2
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        li2.append(int(self.path[1:]))
        print(("l2: ", li2))

def list_extractor():
    global li

    while True:
        if len(li) > 0:
            first = li.pop(0)
            requests.get("http://localhost:8082/" + str(first * 10))
            time.sleep(5)
        else:
            time.sleep(5)

def second_list_extractor():
    global li2

    while True:
        if len(li2) > 0:
            first = li2.pop(0)
            requests.get("http://localhost:8080/" + str(first))
            time.sleep(5)
        else:
            time.sleep(5)

extractor_threads = 6
extractors = [threading.Thread(target=list_extractor) for i in range(extractor_threads)]

second_extractor_threads = 6
second_extractors = [threading.Thread(target=second_list_extractor) for i in range(extractor_threads)]

if __name__ == "__main__":
    for thread in extractors + second_extractors:
        thread.start()

    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")