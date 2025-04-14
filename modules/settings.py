import configparser
import utils
from customtkinter import *


config_file = './config.ini'
config = configparser.ConfigParser()
config.read(config_file, encoding='utf-8')

# Get the current language of the user interface
def get_lang():
    lang_menu_values = ['en_UK', 'zh_CN', 'zh_HK']
    return lang_menu_values
    
# Change the language
def change_lang(menu: CTkOptionMenu):
    lang = menu.get()
    utils.modify_config(config_file, 'Settings', 'lang', lang)
    utils.send_info(lang, 'restart_interface')

# Get the current theme of the user interface
def get_theme():
    theme_menu_values = ['Dark', 'Light']
    return theme_menu_values

# Change the theme
def change_theme(menu: CTkOptionMenu):
    theme = menu.get()
    set_appearance_mode(theme)
    utils.modify_config(config_file, 'Settings', 'theme', get_appearance_mode())