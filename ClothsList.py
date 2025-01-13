# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 14:34:15 2025

@author: Victor Mctrix
"""
import os

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
            clothsData=open(filename, 'r', encoding="utf-8")
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
            return self.men
        elif(option=="W" or option=="w"):
            return self.woman
        elif(option=="C" or option=="c"):
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