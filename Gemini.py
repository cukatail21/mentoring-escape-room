from google import genai
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(dotenv_path=Path(__file__).parent / ".env")
TOKEN = os.getenv("GEMINI_TOKEN")

client = genai.Client(api_key=TOKEN)
class Gemini:
    start_string = "you are the dungeon master in a digital escape room whos rooms are [rooms]. give the start prompt to the users to explain the situation in less than 2000 chars"
    # should be __init__?
    def start(self):
        #TODO: when yuval finishes add rooms from his file
        response = client.models.generate_content(model="gemini-2.0-flash",contents=self.start_string)
        return response.text
    
    def respond_to_message(self,user,content):
        response = client.models.generate_content(model="gemini-2.0-flash",contents=f"user:{user} sent {content}")
        return response.text
    

