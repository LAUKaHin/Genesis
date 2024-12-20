# Genesis
Genesis.py, a broker between OpenRouter and end users/devices based on OpenRouter and request library. Because OpenAI has forbiding Hong Kong from using ChatGPT, I have created this class for another approuch.

Python Version: 3.10

## Genesis.py
This class can help to transmit text, image and markdown to OpenRouter. Due to the limitation on OpenRouter and MarkItDown, it is not possible to transmit other file directly. here are the functions:

### __init__(self, key, httpRef, projTitle)
It is a constructor, you need to set the key in order to use GenAI service from OpenRouter. Set the name of project title is recommended but not necessary. httpRef is not not necessary.

### ImgToBase64(self, filename)
It import image and convert it and return a base64 string. It for the image that stored in local (because of formatting of json for OpenRouter)

### FileToMD(self, filename)
It convert the file to markdown format (This function is rely on MarkItDown and it is buggy as it is a new library)

### CreateDict(self, dicttype, value)
It will create new dictionary for every message. You can only either "text" or "image_url" as dicttype.

### SendAndReceive(self, LLM="")
Main function of Genesis.py, the LLM is for AI/LLM model selection

### __str__(self)
Show the info for the class
