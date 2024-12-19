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
        
    #---Helper Functions---#
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
        return str(MarkItDown().convert(filename).text_content)
    
    #Create new dictionary for content
    def CreateDict(self, dicttype, value):
        if(dicttype=="image_url" and ("http" in value)!=True):
            value=self.ImgToBase64(value)
        return {
                   "type": dicttype,
                    dicttype: value
               }
    
    #---Public Functions---#
    #Push system message (Add new message in contents of system)
    def PushMsgToSystem(self, dicttype, value):
        self.systemContents.append(self.CreateDict(dicttype, value))
        
    #Push system attachment (Add new attachment in contents of system)
    def PushFileToSystem(self, value):
        self.systemContents.append(self.CreateDict("text", self.FileToMD(value)))
        
    #Pop the last message of the content in system
    def PopMsgOfSystem(self):
        self.systemContents.pop()
        
    #Push user message (Add new message in contents of user)
    def PushMsgToUser(self, dicttype, value):
        self.userContents.append(self.CreateDict(dicttype, value))
        
    #Push user attachment (Add new attachment in contents of system)
    def PushFileToUser(self, value):
        self.UserContents.append(self.CreateDict("text", self.FileToMD(value)))
        
    #Pop the last message of the content in user
    def PopMsgOfUser(self):
        self.userContents.pop()
    
    #Send msg to AI
    def TXRX(self, LLM=""):
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
    key="YourKey"
    httpRef=""
    projectTitle="DressUp"
    stylist=Genesis(key, httpRef, projectTitle)#Create object
    stylist.PushMsgToSystem("text", "You are a fashion stylist, you will recommend the most suitable dress from GU for the user according to their face, height and body type. You can only choose the dress provided in my file.")
    stylist.PushFileToSystem("GU_Cloths.docx")
    stylist.PushMsgToUser("text", "Hello! what color of cloth would you recommended to me? Here is my selfee.")
    stylist.PushMsgToUser("image_url", "1.jpg")
    print(stylist)#Show the status of the object
    print(stylist.TXRX("openai/gpt-4o-mini"))#Send the request and receive it
    del stylist# Delete the object
    
if __name__ == "__main__":
    main()