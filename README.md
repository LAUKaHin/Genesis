# Genesis
Genesis.py, a broker between OpenRouter and end users/devices based on OpenRouter and request library. Because OpenAI has forbiding Hong Kong from using ChatGPT, I have created this class for another approuch.

Current Version: 0.0.3\
Support Python Version: 3.10

## Basic Principles
### Theory
### Application
### Azure

## Genesis.py
This class can help to transmit text, image and markdown to OpenRouter. Here are the PUBLIC functions:

### __init__(self, key, httpRef, projTitle)
It is a constructor, you need to set the key in order to use GenAI service from OpenRouter. Set the name of project title is recommended but not necessary. httpRef is not not necessary.

### TXRX(self, LLM="")
Major function of Genesis.py, the LLM is for AI/LLM model selection. It can transmit the data and receive it. This function will return string when there is no error. Otherwise, error code (str) will be returned

### PushMsgToSystem(self, value)
Push string into contents of system. Note that it cannot stored non ascii string in it.

### PushFileToSystem(self, value)
Push file into contents of system. Note that the file cannot contain non ascii string, special math symbols and images.

### PopMsgOfSystem(self)
Pop the last message of the content in system

### PushMsgToUser(self, dicttype, value)
Push string into contents of user. Note that it cannot stored non ascii string in it.

### PushFileToUser(self, value)
Push file into contents of user. Note that the file cannot contain non ascii string, special math symbols and images.

### PopMsgOfUser(self)
Pop the last message of the content in user

### __str__(self)
Show the info for the class

## Limitation
This python class is depends on OpenRouter, request and MarkItDown. Due to the their limitation, there are constraints:

### OpenRouter
It cannot transmit file to GenAI directly, need to be converted to markdown first. Library namely MarkItDown will be used.

### request
Cannot send reqest data with "UTF-8" encode. Don't send text other than English.

### MarkItDown
Please ensure you input file do not have these contents.
1. Cannot convert image of folder to base64 string or either bytearray.
2. Cannot convert Math symbol or LaTex to normal text.

## Template / Example
In main() of Genesis has shown the example of usage. Here provided two templates to showcase how to use Genesis.py
1. DescriptionProvider.py\
   Show how to input filename in CMD and upload image to the GenAI to finish the task
2. Server.py\
   Demonstrate how to handle get and post request and responsethem
