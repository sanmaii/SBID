import configparser
import settings
from customtkinter import *

def settings_ui(lang: str):
    # Basic properties
    settings_window = CTkToplevel()
    settings_window.title("Settings")
    w_mon = settings_window.winfo_screenwidth()
    h_mon = settings_window.winfo_screenheight()
    w_size = int(w_mon/3)
    h_size = int(h_mon/3)
    settings_window.geometry('%dx%d' % (w_size, h_size))
    settings_window.resizable(0,0)
    settings_window.configure(padx=20, pady=20)

    # Config
    config_file = './config.ini'
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    langconfig_file = f'languages/locales/{lang}.ini'
    langconfig = configparser.ConfigParser()
    langconfig.read(langconfig_file, encoding='utf-8')
    
    def setup_ui(win: CTkToplevel):
        # Set up the  user interface
        win.grid_rowconfigure(0, weight=1)
        win.grid_columnconfigure(0, weight=1)
        
        #Set up frame
        frame = CTkFrame(win)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Widgets
        lang_text = CTkLabel(frame, text=langconfig['Settings']['language'])
        lang_text.grid(row=0, column=0, padx=10, pady=10)
        lang_menu = CTkOptionMenu(frame, width=100, corner_radius=10, values=settings.get_lang(), command=lambda x: settings.change_lang(lang_menu))
        lang_menu.set(config['Settings']['lang'])
        lang_menu.grid(row=0, column=1, padx=10, pady=10)
        theme_text = CTkLabel(frame, text=langconfig['Settings']['theme'])
        theme_text.grid(row=1, column=0, padx=10, pady=10)
        theme_menu = CTkOptionMenu(frame, width=100, corner_radius=10, values=settings.get_theme(), command=lambda x: settings.change_theme(theme_menu))
        theme_menu.set(config['Settings']['theme'])
        theme_menu.grid(row=1, column=1, padx=10, pady=10)


    setup_ui(settings_window)