#!/usr/bin/env python
""" 
Author: KylesDev
"""

# Import standard modules
import datetime


# Import Libraries

# Import Application Modules


class Food:

    def __init__(self, name: str = "", code: str = "", image_url: str = "", permanent: bool = False):
        self.name = name
        self.code = code
        self.image_url = image_url
        self.permanent = permanent

    def __str__(self):
        return f"{self.name}".strip()

    def fancy_name(self):
        return self.name.lower().capitalize()

    def get_telegram_link(self):
        return f"[{self.fancy_name()}]({self.image_url})"


class Menu:

    def __init__(self, timestamp: float, daily_menu: dict[str, Food], permanent_menu: dict[str, Food]):
        self.timestamp = timestamp
        self.daily_menu = daily_menu
        self.permanent_menu = permanent_menu

    def __str__(self):
        daily_menu_str = ""
        for food in self.daily_menu.values():
            daily_menu_str += f"- {food}\n"
        permanent_menu_str = ""
        for food in self.permanent_menu.values():
            permanent_menu_str += f"- {food}\n"
        day_str = datetime.datetime.fromtimestamp(self.timestamp).strftime("%d/%m/%Y")
        return f"----- Menu for {day_str}-----\n----- Daily menu -----\n{daily_menu_str}\n" + \
               f"-----Permanent menu-----\n{permanent_menu_str}"

    def get_telegram_message(self, full):

        # Check if there's any food in the menu
        if len(self.daily_menu.values()) == 0 and not full:
            return "Non ci sono menù disponibili per oggi"

        daily_menu_str = ""
        for food in self.daily_menu.values():
            daily_menu_str += f"- {food.get_telegram_link()}\n"
        permanent_menu_str = ""
        if full:
            for food in self.permanent_menu.values():
                permanent_menu_str += f"- {food.get_telegram_link()}\n"
        day_str = datetime.datetime.fromtimestamp(self.timestamp).strftime("%d/%m/%Y")
        final_message = f"**----- Menù per il giorno {day_str}-----**\n\n**----- Menù del giorno -----**\n{daily_menu_str}\n"
        if full:
            final_message += f"**-----Menù fisso-----**\n{permanent_menu_str}"
        return final_message

