from google import genai
from dotenv import load_dotenv
from pathlib import Path
import os
import History
import json

load_dotenv(dotenv_path=Path(__file__).parent / ".env")
TOKEN = os.getenv("GEMINI_TOKEN")

client = genai.Client(api_key=TOKEN)
history = History.History()
class Gemini:

    rooms = []
    current_room = 0
    users = []
    content = ""
    game_over = False
    

    def get_rooms(self):
        with open("mentoring-escape-room/rooms.json", 'r') as f:
            rooms = f.read()
        return rooms

    def get_rooms_as_json(self):
        with open("mentoring-escape-room/rooms.json", 'r') as f:
            rooms = json.load(f)
        return rooms
    
    def __init__(self):
        # self.users = users
        self.rooms = self.get_rooms()
        print(self.rooms)
        self.start_string = f"you are the dungeon master in a digital escape room whos rooms are {self.rooms}."
        "give the start prompt to the users to explain the situation in less than 2000 chars. "
        "if they passed the room, return the keyword \"passed\". the next prompts sent to you are"
        " from the users, and your answers will be relayed straight to them"

    
    
    # this method exists because init can't return a value
    def start(self):
        response = client.models.generate_content(model="gemini-2.0-flash",contents=self.start_string)
        return response.text    

    def respond_to_message(self,user,content):

        response = client.models.generate_content(
            model="gemini-2.0-flash",contents=f"user with username:\"{user}\" sent \"{content}\". answer them. here is you chat history :{history.history_dict}. they are in the room {self.rooms[self.current_room]} "

            )
        print(history.history_dict)
        return response.text
    
    
    def describe_room(self):
        return self.get_rooms_as_json()[self.current_room]["appearance"]
    

    # currently not used, logic is in main.py
    # def game(self):
    #     response=self.respond_to_message(self,self.users,self.content)
    #     if "passed" in response.text:
    #         current_room += 1
    #     return response.text
