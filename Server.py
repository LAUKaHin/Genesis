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
import ClothsList
import ast

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()  

    def do_GET(self):
        #logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for\n {}".format(self.path).encode("utf-8"))
        self.wfile.write(self.app.systemContents[1]["text"].encode('utf-8'))
        #print(self.path)

    def do_POST(self):
        rxStr=""
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        #logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",str(self.path), str(self.headers), post_data.decode('utf-8'))
        self._set_response()
        postDict=ast.literal_eval(post_data.decode('utf-8'))
        self.app.PushImgToUser(postDict.get("image"), postDict.get("fileType"))
        hasTextMsg=postDict.get("text")!=""
        self.app.PushMsgToSystem(self.clothsList.GetClothsList(postDict.get("clothing")))
        if(hasTextMsg):
            self.app.PushMsgToUser("text", postDict.get("text"))
        if(self.netPort==8023):
            rxStr=self.app.TXRX("google/gemini-pro-1.5")
            while("error 520" in rxStr):#Rerey to get response
                rxStr=self.app.TXRX("google/gemini-pro-1.5")
        else:
            #isExist=self.app.userContents[1]!=""
            #self.wfile.write(("[:DEBUG:] Image inserted: "+str(isExist)+"\n").encode("utf-8"))
            #self.wfile.write(("[:DEBUG:] File type: "+str(postDict.get("fileType"))+"\n").encode("utf-8"))
            #self.wfile.write(("[:DEBUG:] Text inserted: "+str(self.app.userContents[2].get("text"))+"\n").encode("utf-8"))
            #self.wfile.write(("[:DEBUG:] Clothing inserted: "+str(postDict.get("clothing"))+"\n").encode("utf-8"))
            rxStr="""{"text": "你selfie張相影得好靚！睇得出你身形勻稱，高度適中。我推薦你著女裝 Oxford Striped Short Shirt 352564，呢件衫嘅窄間隔直紋圖案好易襯衫，而且剪裁修身，會令你望落更加俐落。同時，Oxford 布料舒適透氣，好啱夏天著。如果想更加突出腰身，可以配搭一條幼腰帶。", "cloths": [{"name": "女裝 Oxford Striped Short Shirt 352564", "color": "GCL34", "image": "https://www.gu-global.com/hk/hmall/test/u0000000003060/main/first/1000/1.jpg"}]}"""

        if("error" in rxStr):
            print("Quota Error")
            self.wfile.write(str({"text": rxStr}).encode('utf-8'))
        elif("json```" in rxStr):
            self.wfile.write(rxStr[7:-3].encode('utf-8'))
        else:
            self.wfile.write(rxStr.encode('utf-8'))
        if(hasTextMsg):
            self.app.PopMsgOfUser()
        self.app.PopMsgOfUser()

def Run(server_class=HTTPServer, handler_class=S, key="", port=8080):
    #Setup application
    httpRef=""
    projectTitle="GenOutfit"
    rxJsonFile=open("response.json", 'r', encoding="utf-8")
    jsonFormat=rxJsonFile.read()
    rxJsonFile.close()
    handler_class.app=Genesis.Genesis(key, httpRef, projectTitle)
    handler_class.app.PushMsgToSystem("You are a fashion stylist, you will recommend the most suitable dress from GU for the user according to their face, height and body type in the selfie. You need to give explaination for your choice. You can only choose the dress provided in my file. You should include all these information in following json format, you should selete the the url of the image that match the color and the cloth of your choice. Do not use new line for the response. No other information or format is allowed:"+jsonFormat)
    handler_class.app.PushMsgToUser("text", "Hello! what cloths would you recommend to me? Here is my selfee.")
    handler_class.clothsList=ClothsList.ClothsList("GU_ClothsList")
    handler_class.netPort=port
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

    if len(argv) >= 3:
        Run(key=str(argv[1]),port=int(argv[2]))
    elif len(argv) >= 2:
        Run(key=str(argv[1]))
    else:
        Run()