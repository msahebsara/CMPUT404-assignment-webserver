#  coding: utf-8 
import socketserver, os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        request_arr = [itm.decode("utf-8") for itm in self.data.split()]
        request_method = request_arr[0]
        request_path = request_arr[1]
        www_dir = os.getcwd() + '/www'
        file_serve = 'index.html'

        print('requestmethod', request_method)
        print('request_path', request_path)

        if(request_method != 'GET'):
            return self.generate_response(405)

        if(request_path.endswith('/')):
            path_serve = www_dir + request_path + file_serve
        else: 
            path_serve = www_dir + request_path

        print('pathtoserve', path_serve)
        
        if(os.path.isfile(path_serve)):
            return self.generate_response(200, open(path_serve, 'r').read())
        else: 
            return self.generate_response(404)


    def generate_response(self, status, content = False):
        if(status == 405):
            payload = "HTTP/1.1 405 Method Not Allowed\r\nConnection: close\r\n\r\n"

        if(status == 404):
            payload = "HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n"

        if(status == 200):
            payload = "HTTP/1.1 200 OK\r\n\r\n"

        if(content): payload += content
        self.request.sendall(payload.encode())

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
