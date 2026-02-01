from google import genai
import os

client = genai.Client(api_key="AIzaSyAxP8tXlyv5OtYJugbwiDR9U69iGcY-xo0")

for model in client.models.list():
    print(model.name)