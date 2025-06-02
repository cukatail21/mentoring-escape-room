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
        """returns the rooms as plain text"""
        with open("mentoring-escape-room/rooms.json", 'r') as f:
            rooms = f.read()
        return rooms

    def get_rooms_as_json(self):
        """returns the rooms as a json object"""
        with open("mentoring-escape-room/rooms.json", 'r') as f:
            rooms = json.load(f)
        return rooms
    
    def __init__(self):

        self.rooms = self.get_rooms()
        print(self.rooms)
        self.start_string = f"you are the dungeon master in a digital escape room whos rooms are {self.rooms}."
        "give the start prompt to the users to explain the situation in less than 2000 chars. "
        "if they passed the room, return the keyword \"passed\". the next prompts sent to you are"
        " from the users, and your answers will be relayed straight to them"

    
    def start(self):
        """starts the game using the start_string. exists because init can't return a value"""
        response = client.models.generate_content(model="gemini-2.0-flash",contents=self.start_string)
        history.update_history(self.start_string, "bot", True)
        return response.text    

    def respond_to_message(self,user,content):
        """
        Responds to a message from a user and updates the history.
        PARAMS:
             user: the user who sent the message
             content: the content of the message
        """
        try:
            response = client.models.generate_content(
            model="gemini-2.0-flash",contents=f"user with username:\"{user.name}\" sent \"{content}\". answer them. here is you chat history :{history.history_dict}. they are in the room {self.rooms[self.current_room]} "
            )
        except genai.errors.ServerError as e:
            return "Sorry, there was an error processing your request. Please try again later."
        
        history.update_history(content, user.name, False)
        history.update_history(response.text, "bot", True)
        return response.text
    
    
    def describe_room(self):
        """returns the description of the current room"""
        if self.game_over:
            return
        return self.get_rooms_as_json()[self.current_room]["appearance"]
    
    def reset_game(self):
        """resets the game, history and current room"""
        self.current_room = 0
        self.game_over = False
        history.reset_history()
        return "Game reset. You are back in the first room."
    
    def end_prompt(self):
        """runs when the game is over"""
        Response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="The game is over, give the user a congratulatory message and end the game. tell them they can reset the game with the command !reset_game if they wamt to play again."
        )
        return Response.text