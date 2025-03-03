# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 18:02:05 2024

@author: Victor Mctrix
"""

import Genesis

#Example of how to run this program
def main():
    #Define the key and project title
    key="DerKey"
    httpRef=""
    projectTitle="GenOutfit"
    helper=Genesis.Genesis(key, httpRef, projectTitle)#Create object
    helper.PushMsgToSystem("Your job is to describe the person in an image that user has provided. You need to describe including but not limiting to the hair, face, gender, skin, body shape, cloths, shoes, gender and age. All this information should be included in one paragraph")
    helper.PushMsgToUser("text", "Hello! Could you please help me to describe follwing image?")
    try:
        while(True):
            helper.PushMsgToUser("image_url", input("Please input your filename with extension:\n"))
            print(helper.TXRX("openai/gpt-4o-mini")+"\n")#Send the request and receive it
            helper.PopMsgOfUser()#Remember to delete everytime after receive the msg.
    except KeyboardInterrupt:
        del helper

if __name__ == "__main__":
    main()