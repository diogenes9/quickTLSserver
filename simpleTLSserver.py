#!/usr/bin/python
# this is for python 2.7. Converting to python3 should be trivial

import ssl
# from http.server import BaseHTTPRequestHandler, HTTPServer
import BaseHTTPServer, SimpleHTTPServer

# class myHTTPServer_RequestHandler(BaseHTTPServer):
class myHTTPServer_RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        print('Headers:')
        print self.headers
        # print to file and close--you'd want to do this differently
        # for any sort of high-volume traffic
        f=open("./headers.txt", "a+")
        f.write(bytes(self.headers))
        f.write("-----------------------------\n")
        f.close()
        # Send something back to client (optional)
        message = "<h2>Thanks for your request</h2>"
        # Write content as utf-8 data # caused an error that I couldn't fix
        # self.wfile.write(bytes(message, "UTF8"))
        self.wfile.write(bytes(message))
        return


def run():
    print('starting server...')
    # danger! using this line will expose the port on all network interfaces
    # server_address = ('0.0.0.0', 8000) 
    server_address = ('127.0.0.1', 8000)  # this is safer 
    httpd = BaseHTTPServer.HTTPServer(server_address, myHTTPServer_RequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='../cert/certificate.pem',keyfile='../cert/key.pem',  server_side=True)
    print('running server...')
    httpd.serve_forever()

# use this command to make a unprotected self-signed cert:
# openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out certificate.pem

run()

