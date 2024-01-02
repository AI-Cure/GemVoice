import speech_recognition as sr
import pyttsx3
import google.generativeai as genai

WAKEWORD = None  # If this is a string, it will only pass the converted text to Gemini if this word is in the converted text, If it is None this is simply Ignored. This can be used to replicate functionality like "Hey Alexa".


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

def TakeCommand():
    # Take Command Takes Input from a Microphone then Turns it into a string output
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print('Listening...')
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source=source)
            audio = r.listen(source)

        try:
            print('Recognizing..')
            qeury = r.recognize_google(audio, language='en-in')
        except Exception as e:
            print(e)
            return "none".lower()
        return qeury
    

def GetResponseAndSpeak(query:str):
    Voice = VoiceEngine()
    Model = AImodel(api_key="AIzaSyDQRGF8n7nrdXCYRBy089w3EfpgIji1B2o")

    response = Model.generateOutput(question=query)
    print(response)
    response = response.replace("*","")
    
    Voice.speak(Text=response)


if "__main__" == __name__:    
    
    
    while True:
        query = TakeCommand()
        query = query.lower()
        print(f"{query}")
        if query == "none": # Returns none when a error is passed
            print("An error was encountered while recognizing voice")

        if WAKEWORD == None:
            GetResponseAndSpeak(query=query) # PASSES SENTENCE TO GEMINI HERE
        elif isinstance(WAKEWORD,str):
            if WAKEWORD.lower() in query:
                GetResponseAndSpeak(query=query) # PASSES SENTENCE TO GEMINI HERE
            else:
                print("WAKEWORD NOT IN QUERY")