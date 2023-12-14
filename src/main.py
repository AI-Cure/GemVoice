import os
import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
import json


class VoiceEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('rate',180)
        self.engine.setProperty('voice',self.voices[0].id)
    
    def speak(self,Text:str):
        self.engine.say(Text)
        self.engine.runAndWait()

class AImodel:
    def __init__(self,api_key):
        self.api_key = api_key

        genai.configure(api_key=self.api_key)

        # Set up the model
        self.generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
        }

        self.safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_LOW_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_LOW_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_LOW_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_LOW_AND_ABOVE"
        }
        ]

        self.model = genai.GenerativeModel(model_name="gemini-pro",
                                    generation_config=self.generation_config,
                                    safety_settings=self.safety_settings)

    def generateOutput(self,question:str):
        self.question = question
        self.response = self.model.generate_content(contents=self.question)

        return self.response.text


Model = AImodel("AIzaSyDQRGF8n7nrdXCYRBy089w3EfpgIji1B2o")
Voice = VoiceEngine()

def takeCommandEnglish(): 
         
    r = sr.Recognizer() 
    with sr.Microphone() as source: 
        r.adjust_for_ambient_noise(source=source)          
        # seconds of non-speaking audio before  
        # a phrase is considered complete 
        print('Listening') 
        audio = r.listen(source)   
        try: 
            print("Recognizing") 
            Query = r.recognize_vosk(audio_data=audio,language='en')
            Query = json.loads(Query)
            # for listening the command in indian english 
            Query = Query['text']            
            
            if Query == "":
                return None
            
            print(f"{Query}")
            return Query 

        # handling the exception, so that assistant can  
        # ask for telling again the command 
        except Exception as e: 
            print(e)   
            return "Can you Please Say that Again?" 
  

while True:
    question = takeCommandEnglish()

    

    if question == None:
        print("No response from Mic")
    else:
        response = Model.generateOutput(question=question)
        print(response)
        response = response.replace("*","")
        Voice.speak(response)


