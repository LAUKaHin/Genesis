# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 18:02:05 2024

@author: Victor Mctrix
"""

from Genesis import Genesis

#Example of how to run this program
def main():
    #Define the key and project title
    key="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"
    httpRef=""
    projectTitle="DressUp"
    stylist=Genesis(key, httpRef, projectTitle)#Create object
    stylist.systemContents.append(stylist.CreateDict("text", "Your job is to describe the person in an image that user has provided. You need to describe including but not limiting to the hair, face, gender, skin, body shape, cloths, shoes, gender and age. All this information should be included in one paragraph"))
    stylist.userContents.append(stylist.CreateDict("text", "Hello! Could you please help me to describe follwing image?"))
    while(True):
        stylist.userContents.append(stylist.CreateDict("image_url", input("Please input your filename with extension:\n")))
        print(stylist.SendAndReceive("openai/gpt-4o-mini")+"\n")#Send the request and receive it
        stylist.userContents.pop()#Remember to delete everytime after receive the msg.

if __name__ == "__main__":
    main()