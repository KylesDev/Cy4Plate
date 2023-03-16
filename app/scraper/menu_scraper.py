#!/usr/bin/env python
""" 
Author: KylesDev
"""
# Import standard modules
import time
import requests
import datetime

# Import Libraries
from bs4 import BeautifulSoup

# Import Application Modules
from app.config.config_parser import CONFIG
from app.model.models import Food, Menu
from app.logging import logger


def generate_urls(timestamp: float) -> dict[str, str]:
    """
    This method generates the urls for the different menu pages

    :param timestamp:   the timestamp of the menu
    :return:            a dict of urls
    """
    base_url: str = CONFIG["url"]["base"]
    menu_urls = {}
    for menu_type in CONFIG["menu"]:
        menu_code = CONFIG["menu"][menu_type]
        menu_url = f"{base_url}/{timestamp}/0/{menu_code}"
        menu_urls[menu_type] = menu_url
    return menu_urls


def fetch_menu(menu_url: str) -> dict[str, Food]:
    """
    This method scrapes the menu from the website and returns a dictionary
    with the menu items

    :param menu_url:    the url of the menu page
    :return:            a dict of menu items
    """
    menu = {}
    html_page = requests.get(menu_url, verify=False)
    menu_page = BeautifulSoup(html_page.content, "html.parser")
    menu_items = menu_page.find_all("div", {"class": "cbp-item"})
    for item in menu_items:
        food = Food()
        item_name = item.find("div", {"class": "cbp-l-grid-masonry-projects-title"}).text
        food.name = item_name
        item_image_div = item.find("div", {"class": "cbp-caption-defaultWrap"})
        if item_image_div:
            item_image = item_image_div.find("img")
            if item_image:
                food.image_url = item_image["src"]
        # get the parameter data-id of item
        item_code = item["data-id"]
        food.code = item_code
        # if the item is of class alternativa_fissa, it is a permanent item
        if "alternativa_fissa" in item["class"]:
            food.permanent = True
        else:
            food.permanent = False
        menu[item_code] = food
    return menu


def get_menu(timestamp: float) -> Menu:
    """
    This method collects the menus from the website and returns a dictionary
    with the menu items

    :param timestamp:   the timestamp of the menu
    :return:            a dict of menu items
    """
    logger.info("Collecting menus for Day: {}({})".format(datetime.datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y"), timestamp))

    logger.debug("Generating menu urls")
    menu_urls = generate_urls(timestamp)
    menus = {}

    logger.debug("Collecting menus")
    for menu_type in menu_urls.keys():
        menu = fetch_menu(menu_urls[menu_type])
        menus[menu_type] = menu

    # Merge all the "daily" and "permanent" items of every menu type into a single dict
    logger.debug("Merging menus")
    daily_items = {}
    permanent_items = {}
    for menu in menus.values():
        for item in menu.values():
            if item.permanent:
                permanent_items[item.code] = item
            else:
                daily_items[item.code] = item
    logger.debug("Menus collected")

    return Menu(timestamp, daily_items, permanent_items)


def test():
    timestamp = time.time()
    menus = get_menu(timestamp)
    return menus
