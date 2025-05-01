# User interface of SBID.
import os
import configparser
import webbrowser
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    modules_dir = f'{Path(sys.executable).parent}/modules'
else:
    modules_dir = f'{Path(__file__).parent}/modules'
sys.path.append(modules_dir)


from modules import version
from modules import nogi_ui
from modules import sakura_ui
from modules import hinata_ui
from modules import settings_ui
from modules import update
from modules import member
from modules.get_icon_path import get_icon_path
from customtkinter import *
from datetime import datetime
from PIL import Image

# Main UI
class App(CTk):
    def __init__(self):
        super().__init__()
        self.w_mon = self.winfo_screenwidth() # Get the width of the screen
        self.h_mon = self.winfo_screenheight() # Get the height of the screen
        self.w_size = int(self.w_mon/2)
        self.h_size = int(self.h_mon/2)
        self.x_pos = int((self.w_mon-self.w_size)/2) # Set app's x position.
        self.y_pos = int((self.h_mon-self.h_size)/2) # Set app's y postiopn.
        self.title(f'SBID {version.version}')
        self.iconbitmap(get_icon_path(r'resources\138.ico'))
        self.geometry('%dx%d+%d+%d' % (self.w_size, self.h_size, self.x_pos, self.y_pos))
        self.minsize(300,200)
        self.resizable(0,0)
        # Load config
        self.config_file = './config.ini'
        self.config = configparser.ConfigParser()
        self.load_config()
        self.theme = self.config.get('Settings', 'theme', fallback='Dark')
        set_appearance_mode(self.theme)
        # Load language config
        self.language = self.config.get('Settings', 'lang', fallback='en_UK')
        self.langconfig = configparser.ConfigParser()
        self.load_locale()
        # Load member config
        self.update_mem_config()
        # Setup UI
        self.setup_ui()
        # Check for update
        self.check_update()

    def load_config(self):
        # Load the perferred settings in the configuration file
        # Create a config file if it does not exist
        if not os.path.exists(self.config_file):
            self.config['Settings'] = {'lang': 'en_UK',
                                        'theme': 'Dark'}
            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
        # If the config file exists, read the file
        else:
            self.config.read(self.config_file, encoding='utf-8')

    def load_locale(self):
        # Load language settings file
        try:
            self.langconfig.read(f'languages/locales/{self.language}.ini', encoding='utf-8')
        except Exception:
            pass

    def update_mem_config(self):
        # Create a member config file if it does not exist
        # Update the config file to ensure the member list is up to date
        members = member.fetch_member_list()
        member.load_member_config(members)
        member.update_mem_config(members)
        

    def setup_ui(self):
        # Set up the main user interface
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        frame = CTkFrame(self)
        frame.grid(row=0, column=0, padx=int(self.w_size/48), pady=int(self.h_size/27), sticky='nsew')
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)

        # Display the name of the app
        app_text_label = CTkLabel(frame, text=f'SBID {version.version}', font=CTkFont(weight='bold', size=50), cursor='hand2')
        app_text_label.grid(row=0, column=0, columnspan=3, pady=20, sticky='nesw')
        app_text_label.bind('<Button-1>', lambda x: webbrowser.open('https://github.com/sanmaii/SBID'))
        support_msg = CTkLabel(frame, text=self.langconfig['Main']['support'], font=CTkFont(size=30))
        support_msg.grid(row=1, column=0, columnspan=3, pady=10, sticky='n')
        
        # Images and Buttons
        nogi_image = CTkLabel(frame, text='', image=CTkImage(Image.open('resources/2.png'), Image.open('resources/52.png'), size=(60,60)), cursor='hand2')
        nogi_image.bind('<Button-1>', lambda x: webbrowser.open('https://www.nogizaka46.com/s/n46/artist/48015'))
        nogi_image.grid(row=2, column=0)
        sakura_image = CTkLabel(frame, text='', image=CTkImage(Image.open('resources/3.png'), Image.open('resources/53.png'), size=(60,60)), cursor='hand2')
        sakura_image.bind('<Button-1>', lambda x: webbrowser.open('https://sakurazaka46.com/s/s46/artist/57'))
        sakura_image.grid(row=2, column=1)
        hinata_image = CTkLabel(frame, text='', image=CTkImage(Image.open('resources/4.png'), Image.open('resources/54.png'), size=(60,60)), cursor='hand2')
        hinata_image.bind('<Button-1>', lambda x: webbrowser.open('https://www.hinatazaka46.com/s/official/artist/34'))
        hinata_image.grid(row=2, column=2)

        nogi_button = CTkButton(frame, text=self.langconfig['Main']['n46'], command=lambda: nogi_ui.nogi_ui(self.language))
        nogi_button.grid(row=3, column=0, padx=20, pady=20, sticky='ew')      
        sakura_button = CTkButton(frame, text=self.langconfig['Main']['s46'], command=lambda: sakura_ui.sakura_ui(self.language))
        sakura_button.grid(row=3, column=1, padx=20, pady=20, sticky='ew')
        hinata_button = CTkButton(frame, text=self.langconfig['Main']['h46'], command=lambda: hinata_ui.hinata_ui(self.language))
        hinata_button.grid(row=3, column=2, padx=20, pady=20, sticky='ew')

        # Date and time
        def update_datetime():
            datetime_label = CTkLabel(frame, text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), font=CTkFont(size=20))
            datetime_label.grid(row=4, column=0, padx=20, pady=20, sticky='w')
            datetime_label.after(1000, update_datetime)
        update_datetime()

        # Settings
        settings_label = CTkLabel(frame, text='', image=CTkImage(Image.open('resources/6.png'), Image.open('resources/56.png'), size=(40,40)), cursor='hand2')
        settings_label.grid(row=4, column=2, padx=20, sticky='e')
        settings_label.bind('<Button-1>', lambda x: settings_ui.settings_ui(self.language))

    # Check update
    def check_update(self):
        if update.check_update(self.language) == self.langconfig['Update']['yes']:
            update.pull_latest()

if __name__ == "__main__":
    app = App()
    app.mainloop()