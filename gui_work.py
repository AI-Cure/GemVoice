import flet as ft 
import google.generativeai as genai
import pyttsx3




class main:
    def __init__(self,page: ft.Page):
        self.page = page
        
        self.page.title = "Flet counter example"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        
        self.Voice = VoiceEngine()
        self.Model = AImodel("AIzaSyDQRGF8n7nrdXCYRBy089w3EfpgIji1B2o")
        
        self.text_field = ft.TextField(label="Enter your question!")
        self.submit = ft.ElevatedButton(text="Submit", on_click=self.processInput)
        
        self.page.add(self.text_field,self.submit)

    def processInput(self,e):
        self.question = self.text_field.value
        self.text_field.value = ""
        self.page.update()
        response = self.Model.generateOutput(question=self.question)
        print(response)
        response = response.replace("*","")
        self.Voice.speak(response)
        self.Voice = None
        self.Voice = VoiceEngine()
        

        
        
        
        
        
class VoiceEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('rate',180)
        self.engine.setProperty('voice',self.voices[0].id)
    

    
    def speak(self,Text:str):
        if self.engine._inLoop:
            self.engine.endLoop()
        self.engine.say(Text)
        self.engine.runAndWait()
        self.engine.endLoop()
        if self.engine._inLoop:
            self.engine.endLoop()
            
class AImodel:
    def __init__(self,api_key):
        self.api_key = api_key

        genai.configure(api_key=self.api_key)

        # Set up the model
        self.generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 512,
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


ft.app(target=main)