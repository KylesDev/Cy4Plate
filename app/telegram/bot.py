#!/usr/bin/env python
""" 
Author: KylesDev
"""
import datetime
import time

# Import standard modules

# Import Libraries
import telebot

# Import Application Modules
from app.config.config_parser import CONFIG
from app.scraper.menu_scraper import get_menu

BOT = telebot.TeleBot(CONFIG["telegram"]["token"])

HELP_MESSAGE = """- Usa il comando /menu per ricevere il menù di oggi.\n- Se vuoi ricevere il menù completo, 
inclusi i piatti permanenti, usa il comando /fullmenu.\n- In entrambi i casi puoi anche specificare una data nel 
formato **dd/mm/yyyy** per ricevere il menù di quella data. """


@BOT.message_handler(commands=["start"])
def start(message):
    BOT.send_message(message.chat.id, f"Ciao, sono **Cy4Plate**, il bot che ti comunica il menù della mensa.\n\n{HELP_MESSAGE}"
                     ,
                     parse_mode="Markdown")


@BOT.message_handler(commands=["menu", "fullmenu"])
def send_menu(message):
    """This method sends the menu to the user"""

    # Check if the message starts with fullmenu
    full_menu = True if message.text.startswith("/fullmenu") else False

    # Check if the message contains a date in the format dd/mm/yyyy
    if len(message.text.split()) > 1:
        date = message.text.split()[1]
        # Check if the date is valid
        try:
            timestamp = datetime.datetime.strptime(date, "%d/%m/%Y").timestamp()
            BOT.send_message(message.chat.id, "Ricevo il menù per la data specificata...")
            menu = get_menu(timestamp)
            BOT.send_message(message.chat.id, menu.get_telegram_message(full_menu), parse_mode="Markdown",
                             disable_web_page_preview=True)
        except ValueError:
            BOT.send_message(message.chat.id,
                             "La data inserita non è valida. Inviami la data nel formato **dd/mm/yyyy**")

    elif message.text == "/menu" or message.text == "/fullmenu":
        timestamp = time.time()
        BOT.send_message(message.chat.id, "Ricevo il menù per oggi...")
        menu = get_menu(timestamp)
        BOT.send_message(message.chat.id, menu.get_telegram_message(full_menu), parse_mode="Markdown",
                         disable_web_page_preview=True)

    else:
        BOT.send_message(message.chat.id,
                         "Non ho capito cosa vuoi. Usa il comando /help per avere informazioni sull'utilizzo del bot.")


@BOT.message_handler(commands=["help"])
def send_help(message):
    BOT.send_message(message.chat.id, HELP_MESSAGE, parse_mode="Markdown")
