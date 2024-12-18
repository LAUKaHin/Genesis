# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 16:10:31 2024

@author: Victor Mctrix
"""

#Import libraries
import json
import base64
import requests
from markitdown import MarkItDown

class Genesis:
    #Define constructor, you need to set the key and project title
    def __init__(self, key, httpRef, projTitle):
        self.key=key
        self.httpRef=httpRef
        self.projTitle=projTitle
        self.systemContents=[]
        self.userContents=[]
        
    
    #Import image and convert it to base64 string (If image is stored in local)
    def ImgToBase64(self, filename):
        fileType=""
        if("jpg" in filename or "jpeg" in filename or "JPG" in filename or "JPEG" in filename):
            fileType="jpeg"
        elif("png" in filename or "PNG" in filename):
            fileType="png"
        elif("webp" in filename or "WEBP" in filename):
            fileType="webp"
        else:
            print("Error: file type not supported")
            return None
        image=open(filename, 'rb')
        encoded="data:image/"+fileType+";base64,"+base64.b64encode(image.read()).decode('ascii')
        image.close()
        return encoded
    
    #Import file and convert it to string (If filee is stored in local)
    def FileToMD(self, filename):
        return MarkItDown().convert(filename)
    
    #Create new dictionary for content
    def CreateDict(self, dicttype, value):
        if(dicttype=="image_url" and ("http" in value)!=True):
            value=self.ImgToBase64(value)
        return {
                   "type": dicttype,
                    dicttype: value
               }
    
    #Send msg to AI
    def SendAndReceive(self, LLM=""):
        response = requests.post(
          url="https://openrouter.ai/api/v1/chat/completions",
          headers={
            "Authorization": f"Bearer {self.key}",
            "HTTP-Referer": f"{self.httpRef}", # Optional, for including your app on openrouter.ai rankings.
            "X-Title": f"{self.projTitle}", # Optional. Shows in rankings on openrouter.ai.
          },
          data=json.dumps({
            "model": LLM, # Optional
            "messages":
            [
                {
                    "role": "system",
                    "content": self.systemContents
                },
                {
                    "role": "user",
                    "content": self.userContents
                }
            ]
          })
        )
        return json.loads(response.text)["choices"][0]["message"]["content"]
        #return json.loads(response.text)["choices"]["message"]["content"]
        #return json.dumps(json.loads(response.text), indent=4)#Readable Format
    
    #Show the info for the class
    def __str__(self):
        return "Defined Rule:\n" + self.systemContents[0]["text"] + "\n\n" + "User's message:\n" + self.userContents[0]["text"]          

        
#Example of how to run this program
def main():
    #Define the key and project title
    print("Running G Main")
    key="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"
    httpRef=""
    projectTitle="DressUp"
    stylist=Genesis(key, httpRef, projectTitle)#Create object
    stylist.systemContents.append(stylist.CreateDict("text", "You are a fashion stylist, you will recommend the most suitable dress from GU for the user according to their face, height and body type. You can only choose the dress provided in my file."))
    stylist.userContents.append(stylist.CreateDict("text", "Hello! who are you?"))
    print(stylist)#Show the status of the object
    print(stylist.SendAndReceive("openai/gpt-4o-mini"))#Send the request and receive it
    del stylist.userContents#Remember to delete everytime after receive the msg.
    del stylist# Delete the object