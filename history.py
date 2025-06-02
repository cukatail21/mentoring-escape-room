import os
import json

class History:
    
    def __init__(self):
        # TODO: make sure duplicate prompts are not lost
        self.history_dict = {
            "bot":[],
            "users":[]
        }   

    # does work, but not used
    def get_history(self):
        return self.history_dict
    
    def update_history(self,message, user, bot):
        """
        Updates the history with a new message.
        PARAMS:
            message: the message to add
            user: the user who sent the message
            bot: true if the message is from the bot, false if it is from a user
        """
        to_add = {user: message}
        if bot:
            self.history_dict["bot"].append(to_add)
            return
        self.history_dict["users"].append(to_add)

    def reset_history(self):
        """Resets the history to the initial state."""
        self.history_dict = {
            "bot":[],
            "users":[]
        }