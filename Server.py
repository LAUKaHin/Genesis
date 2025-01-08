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
import ast
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
        postDict=ast.literal_eval(post_data.decode('utf-8'))
        self.app.PushImgToUser(postDict.get("image"), postDict.get("fileType"))
        hasTextMsg=postDict.get("text")!=""
        self.app.PushMsgToSystem(self.clothsList.GetClothsList(postDict.get("clothing")))
        if(hasTextMsg):
            self.app.PushMsgToUser("text", postDict.get("text"))
        #self.app.result=self.app.TXRX("openai/gpt-4o-mini")
        print(self.app.result)
        self.wfile.write(("[:DEBUG:] Image inserted: "+str(self.app.userContents[0]!="")))
        self.wfile.write(("[:DEBUG:] Text inserted: "+str(self.app.userContents[1])))
        self.wfile.write(("[:DEBUG:] Clothing inserted: "+str(postDict.get("clothing"))))
        #self.wfile.write(("POST request for: "+self.app.result).format(self.path).encode('utf-8'))
        if(hasTextMsg):
            self.app.PopMsgOfUser()
        self.app.PopMsgOfUser()

class ClothsList():
    def __init__(self, path):
        self.men=""
        self.woman=""
        self.children=""
        dirList=os.listdir(path)
        for i in range(len(dirList)):
            filename=path+"/"+dirList[i]+"/"+dirList[i]+".md"
            if(os.path.isfile(filename)==False):
                continue
            clothsData=open(filename, 'r')
            currentCloth=clothsData.read()
            if("男裝" in currentCloth):
                self.men+=currentCloth
            elif("女裝" in currentCloth):
                self.woman+=currentCloth
            elif("童裝" in currentCloth):
                self.children+=currentCloth
            else:
                self.men+=currentCloth
                self.woman+=currentCloth
                self.children+=currentCloth
            clothsData.close()

    def GetClothsList(self, option):
        if(option=="M" or option=="m"):
            print(self.men)
            return self.men
        elif(option=="W" or option=="w"):
            print(self.woman)
            return self.woman
        elif(option=="C" or option=="c"):
            print(self.children)
            return self.children
        else:
            print("Error: cannot identify input: " +str(option))

    def PrintClothsList(self,option):
        if(option=="M" or option=="m"):
            print(self.men)
        elif(option=="W" or option=="w"):
            print(self.woman)
        elif(option=="C" or option=="c"):
            print(self.children)
        else:
            print("Error: cannot identify input: " +str(option))


def Run(server_class=HTTPServer, handler_class=S, port=8080):
    #Setup application
    key="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"
    httpRef=""
    projectTitle="GenOutfit"
    handler_class.app=Genesis.Genesis(key, httpRef, projectTitle)
    handler_class.app.PushMsgToSystem("You are a fashion stylist, you will recommend the most suitable dress from GU for the user according to their face, height and body type. You can only choose the dress provided in my file. After you give recommendation, you should give simple sumary that include all the cloths you suggested but not need to give descrption to it. The summary need to include: full name of each colths + ID + Color")
    handler_class.app.PushMsgToUser("text", "Hello! what color of cloth would you recommend to me? Here is my selfee.")
    handler_class.clothsList=ClothsList("GU_ClothsList")
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