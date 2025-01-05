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
        encoded="data:image/"+fileType+";base64,"+base64.b64encode(image.read()).decode('utf-8')
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
        
    def CheckUserContents(self):
        return len(self.userContents)>0
    
    def CheckSystemContents(self):
        return len(self.systemContents)>0
    
    #---Public Functions---#
    #Push system message (Add new message in contents of system)
    def PushMsgToSystem(self, value):
        self.systemContents.append(self.CreateDict("text", value))
        
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
        if(self.CheckSystemContents()==False or self.CheckUserContents()==False):
            print("Error in TXRX(): missing systemContent or userContent.")
            return
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
          }, ensure_ascii=False).encode("utf-8"))#Set string data to UTF-8 encoding format
        if(response.status_code!=200):
            return str(response.status_code)
        else:
            return json.loads(response.content.decode("utf-8"))["choices"][0]["message"]["content"]
    
    #Show the info for the class
    def __str__(self):
        if(self.CheckSystemContents()==False):
            print("Error: missing element in systemContents.")
            return ""
        elif(self.CheckUserContents()==False):
            print("Error: missing element in userContents.")
            return ""
        else:
            return "Defined Rule:\n" + self.systemContents[0]["text"] + "\n\n" + "User's message:\n" + self.userContents[0]["text"]
        
#Example of how to run this program
def main():
    #Define the key and project title
    key="DerKey"
    httpRef=""
    projectTitle="GenOutfit"
    stylist=Genesis(key, httpRef, projectTitle)#Create object
    stylist.PushMsgToSystem("")
    #stylist.PushFileToSystem("GU_Cloths.docx")
    stylist.PushMsgToUser("text", "想問吓點解香港科技大學會被叫做The University of Stress and Tension？")
    #stylist.PushMsgToUser("image_url", "me.jpg")
    print(stylist)#Show the status of the object
    print("\nGenAI's answer: "+stylist.TXRX("openai/gpt-4o-mini"))#transmit request and receive response from it
    del stylist# Delete the object
    
if __name__ == "__main__":
    main()