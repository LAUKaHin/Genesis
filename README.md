# Genesis
Genesis.py, a broker between OpenRouter and end users/devices based on OpenRouter and request library. Because OpenAI has forbiding Hong Kong from using ChatGPT, I have created this class for another approuch.

Current Version: 0.0.9\
Support Python Version: 3.10

## News
Version updated since 14thJanuary,2025:
Add OpenRouter crash error

## Basic Principles
### Theory
Prompt engineering is the means by which LLMs are programmed via prompts.[1] A prompt is a set of instructions provided to an LLMthat programs the LLM by customizing it and/or enhancing or refining its capabilities.[2] To obtain more desired response from GenAI/LLM, there are not only have user prompt, but also have system prompt. User prompt is the type of prompt that comes from the user. Which is the most common form of prompting and is how prompts are usually delivered in consumer applications.[2] System prompt is the core set of instructions that we give an LLM to not only scope what it can do, but also how it interacts with the user.[3]\
In system prompt, by adding a role, context and instructions, those content can prompt for richer behavior. [3] Although it is hard to say is the information provided from user is rich enough, system prompt can set instruction to make LLM/GenAI keep asking question untill LLM/GenAI has collect sufficient information to generate the satisfactory response.[1]

### Application
Use one of our project "「智 」識搭" (Use "GenOutfit" for short) as an example, if cloths shops want to use GenAI to give dressing recommendation to customers. The system prompt can be written as: You are a fashion stylist, you will recommend the most suitable dress from my cloths shops for the user according to their face, height and body type. You can only choose the dress provided in my file.\
User prompt: Hello! what outfits are most suitable for me? Here is my selfee.\
Then the GenAI will chose the suitable cloths for the customer according the selfie from customer and the cloths list has givin in system prompt.

### Azure
Use the previous as an example, To prevent the big load of the client devicce, it is suggested Azure virtual machine service be used, which stored all cloths information in a list. When the server has received the post request from client, it will also send the cloths list to OpenRouter. To make the application more scalable, author strongly recommended all the cloths are listed into one file/document instead of separated individually.

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
Show the info for the class, also show the version of Genesis

## Limitation
This python class is depends on OpenRouter and MarkItDown. Due to the their limitation, there are constraints:

### OpenRouter
It cannot transmit file to GenAI directly, need to be converted to markdown first. Library namely MarkItDown will be used.

### MarkItDown
Please ensure you input file do not have these contents.
1. Cannot convert image inside file to base64 string or either bytearray.
2. Cannot convert Math symbol or LaTex to normal text.

## Template / Example
In main() of Genesis has shown the example of usage. Here provided two templates to showcase how to use Genesis.py
1. DescriptionProvider.py\
   Show how to input filename in CMD and upload image to the GenAI to finish the task
2. Server.py\
   Demonstrate how to handle get and post request and responsethem

# References
[1] J. White et al., “A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT,” 2023. Available: https://arxiv.org/pdf/2302.11382\
[2] P. Liu, W. Yuan, J. Fu, Z. Jiang, H. Hayashi, and G. Neubig, “Pre train, prompt, and predict: A systematic survey of prompting methods in natural language processing,” ACM Computing Surveys, vol. 55, no. 9, pp. 1–35, 2023.\
[3] M. Groenewege, “System prompt design: Bridging the gap between novice mental models and reality,” Discourse & Communication, Aug. 2024, doi: https://doi.org/10.1177/17504813241267055.
