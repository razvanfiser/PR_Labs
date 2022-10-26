from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import requests
import threading

hostName = "localhost"
serverPort = 8082
li = []

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        global li
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        li.append(int(self.path[1:]))
        print(li)

def list_extractor():
    global li

    while True:
        if len(li) > 0:
            first = li.pop(0)
            requests.post(("http://localhost:8081/" + str(int(- first / 10))))
            time.sleep(5)
        else:
            time.sleep(5)

extractor_threads = 6
extractors = [threading.Thread(target=list_extractor) for i in range(extractor_threads)]

if __name__ == "__main__":
    for thread in extractors:
        thread.start()

    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")