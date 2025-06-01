import os
import json

class History:
    
    def __init__(self):
        # TODO: make sure duplicate promts are not lost
        self.history_dict = {
            "bot":[],
            "users":[]
        }   

    # doesnt work, here for nostalgic values
    def get_history(self):
        return self.history_dict
    
    def update_history(self,message, user, bot):
        to_add = {user: message}
        if bot:
            self.history_dict["bot"].append(to_add)
            return
        self.history_dict["users"].append(to_add)

    def reset_history(self):
        self.history_dict = {
            "bot":[],
            "users":[]
        }