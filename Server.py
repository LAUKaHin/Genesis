#!/usr/bin/env python3
"""
License: MIT License
Copyright (c) 2023 Miel Donkers
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import Genesis
import os

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()  

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for\n {}".format(self.path).encode("utf-8"))
        self.wfile.write(self.app.systemContents[1]["text"].encode('utf-8'))
        print(self.path)

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        self._set_response()
        self.app.PushImgToUser(post_data.get("image"), post_data.get("fileType"))
        hasTextMsg=post_data.get("text")!=""
        if(hasTextMsg):
            self.app.PushMsgToUser("text", post_data.get("text"))
        self.app.result=self.app.TXRX("openai/gpt-4o-mini")
        self.wfile.write(("POST request for: "+self.app.result).format(self.path).encode('utf-8'))
        if(hasTextMsg):
            self.app.PopMsgOfUser()
        self.app.PopMsgOfUser()

def CreateClothsList(path):
    clothsList=""
    dirList=os.listdir(path)
    for i in range(dirList):
        filename=path+"/"+dirList[i]+"/"+dirList[i]+".md"
        if(os.path.isfile(filename)==False):
           continue
        clothsData=open(filename, 'rb')
        clothsList+=clothsData
        clothsData.close()
    print("[:DEBUG:] "+clothsList)
    return clothsList

def Run(server_class=HTTPServer, handler_class=S, port=8080):
    #Setup application
    key="DerKey"
    httpRef=""
    projectTitle="GenOutfit"
    handler_class.app=Genesis.Genesis(key, httpRef, projectTitle)
    handler_class.app.PushMsgToSystem("You are a fashion stylist, you will recommend the most suitable dress from GU for the user according to their face, height and body type. You can only choose the dress provided in my file. After you give recommendation, you should give simple sumary that include all the cloths you suggested but not need to give descrption to it. The summary need to include: full name of each colths + ID + Color")
    handler_class.app.PushMsgToSystem(CreateClothsList("GU_Product_Details"))
    handler_class.app.PushMsgToUser("text", "Hello! what color of cloth would you recommend to me? Here is my selfee.")

    #Setup server
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    del handler_class.app
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        Run(port=int(argv[1]))
    else:
        Run()