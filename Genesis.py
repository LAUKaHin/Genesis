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
        
    def CheckUserContentsExist(self):
        return len(self.userContents)>0
    
    def CheckSystemContentsExist(self):
        return len(self.systemContents)>0
    
    #---Public Functions---#
    #Push system message (Add new message in contents of system)
    def PushMsgToSystem(self, value):
        self.systemContents.append(self.CreateDict("text", value))
        
    #Push system attachment (Add new attachment in contents of system)
    def PushFileToSystem(self, value):
        self.systemContents.append(self.CreateDict("text", self.FileToMD(value)))
    
    #Check each item in system contents
    def DebugCheckSystem(self):
        for i in range(0, len(self.systemContents), 1):
            print(self.systemContents)
        
    #Pop the last message of the content in system
    def PopMsgOfSystem(self):
        self.systemContents.pop()
        
    #Push user message (Add new message in contents of user)
    def PushMsgToUser(self, dicttype, value):
        self.userContents.append(self.CreateDict(dicttype, value))
    
    #Push image to user content by parsing base64 string
    def PushImgToUser(self, value, fileType):
        self.userContents.append(self.CreateDict("text", "data:image/"+fileType+";base64,"+value))
        
    #Push user attachment (Add new attachment in contents of system)
    def PushFileToUser(self, value):
        self.UserContents.append(self.CreateDict("text", self.FileToMD(value)))
        
    #Check each item in user contents
    def DebugCheckUser(self):
        for i in range(0, len(self.userContents), 1):
            print(self.userContents)
        
    #Pop the last message of the content in user
    def PopMsgOfUser(self):
        self.userContents.pop()
    
    #Send msg to AI
    def TXRX(self, LLM="", provider=[""]):
        if(self.CheckSystemContentsExist()==False or self.CheckUserContentsExist()==False):
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
            ],
            "provider":
            {
              "order": provider
            }
          }, ensure_ascii=False).encode("utf-8"))#Set string data to UTF-8 encoding format
        if(response.status_code!=200):
            return "error"+str(response.status_code)
        elif("error" in response.text):
            return json.loads(response.content.decode("utf-8"))["error"]
        elif("choices" in response.text):#Handle the OpenRouter response nothing
            return json.loads(response.content.decode("utf-8"))["choices"][0]["message"]["content"]
        else:
            return "error 520: OpenRouter has failed to response"
    
    #Show the info for the class
    def __str__(self):
        name="Genesis v0.1.0\n\n"
        if(self.CheckSystemContentsExist()==False):
            print("Error: missing element in systemContents.")
            return name
        elif(self.CheckUserContentsExist()==False):
            print("Error: missing element in userContents.")
            return name
        else:
            return name + "Defined Rule:\n" + self.systemContents[0]["text"] + "\n\n" + "User's message:\n" + self.userContents[0]["text"]
        
#Example of how to run this program
def main():
    #Define the key and project title
    key="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"
    httpRef=""
    projectTitle="Investment"
    AI=Genesis(key, httpRef, projectTitle)#Create object
    AI.PushMsgToSystem("你係投資顧問，你需要提供具體的投資建議或推薦特定股票。")#Set system prompt msg
    AI.PushMsgToUser("text", "Hello! 身為價值投資者，你會推薦我投資咩股票？")#Set user prompt msg
    print("\AI's answer: "+str(AI.TXRX("openai/gpt-4o-2024-08-06", "Azure")))#transmit request and receive response from it
    del AI# Delete the object
    
if __name__ == "__main__":
    main()