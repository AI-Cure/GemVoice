# English_8th_GP
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![Generic badge](https://img.shields.io/badge/Maintained-Yes-<COLOR>.svg)](https://shields.io)





A School Project made on the basis of newly released AI of **Google Gemini Pro**. This uses Gemini Pro API to get the meaning of the words by Gemini and converting into Speech using the python library
*`pyttsx3`*. You can ask any questions from Gemini.

  

## Prerequisites

* Python
* Google Generative AI API key
* Choose desired model and download that file and use the command `pip install -r requirements.txt`

# Installation Steps


After installing the prerequisites follow the below mentioned steps.

1. Open the terminal and go to the folder in which you have stored the project select from both the versions you like (Gui-based, Speech-based)
2. Put the Google API key at
   ###### GUI based
   > At line number 16 
    ```
    self.Model = AImodel(api_key="API KEY HERE") 

    ```
    ###### Speech Based
   > At line number 93

   ```
   Model = AImodel(api_key="API KEY HERE")

   ``` 
    
3. Run your code. 

# Future Improvements

* ~~Making it fully voice accessible~~
> The Code for speech recognition is fully working in `with_speech.py`
* Adding Google Gemini Pro Vision
* ~~Make a `requirements.txt` file for the packages~~
* Making the GUI Look better
