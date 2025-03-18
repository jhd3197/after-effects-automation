import pandas as pd
import json


class botMixin:
    """
    Bot Mixin
    """
    
    def startBot(self,file_name):
        """
        startBot
        """
        print("start Bot")

        # Get File with json using utf-8
        with open(file_name, encoding="utf8") as json_file:
            data = json.load(json_file)

        self.startAfterEffect(data)
