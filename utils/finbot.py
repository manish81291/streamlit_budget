from gtts import gTTS
import streamlit as st
import os
import uuid
import base64
import streamlit.components.v1 as components
from google import genai


class FinFlowBot:

    def __init__(self):
        self.client = genai.Client(
                vertexai=True, project='hack-team-finfluenzers', location='us-central1'
            )

    def call_ai(self,prompt):

        response = self.client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt
            )
    
        return response
    
    def textToSpeech(self,text):
        if text.strip():
            tts = gTTS(text)
            filename = f"speech_{uuid.uuid4().hex}.mp3"
            tts.save(filename)

            # Read the file and encode to base64
            with open(filename, "rb") as audio_file:
                audio_bytes = audio_file.read()
                b64 = base64.b64encode(audio_bytes).decode()

            # Autoplay using HTML audio tag
            audio_html = f"""
            <audio autoplay controls>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
            """
            components.html(audio_html, height=80)

            os.remove(filename)





