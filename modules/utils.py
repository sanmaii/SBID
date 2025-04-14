import configparser
from customtkinter import *
from CTkMessagebox import CTkMessagebox

# Cut a string into serveral pieces with specified number of characters
def cut_str(cut: str, index: int):
    output = ''
    for i in range(0, len(cut), index):
        if len(cut)-i < index:
            output += cut[i:i+index]
        else:
            output += cut[i:i+index] + '\n'
    return output

# Concatenate the selected directory
def concat_dir(dir_label: CTkLabel = None, directory: str = None):
    # Either enter a CTkLabel or a directory string
    if dir_label is not None:
        concatted_dir = dir_label.cget('text')
        if '\n' in concatted_dir:
            concatted_dir = concatted_dir.replace('\n', '')
    if directory is not None:
        concatted_dir = directory
        if '\n' in directory:
            concatted_dir = directory.replace('\n', '')
    return concatted_dir

# Modify the config file
def modify_config(config_file: str, section: str, option: str, value):
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    with open(config_file, 'w', encoding='utf-8') as f:
        config.set(section, option, value)
        config.write(f)

# Disable widgets
def disable_widgets(*widgets: CTkButton | CTkEntry | CTkOptionMenu):
    for i in widgets:
        i.configure(state='disabled')

# Enalbe widgets
def enable_widgets(*widgets: CTkButton | CTkEntry | CTkOptionMenu):
    for i in widgets:
        i.configure(state='normal')

# Check whether all the inputted widgets are selected
def check_select(*select_widgets: CTkComboBox | CTkOptionMenu):
    for select_widget in select_widgets:
        if select_widget.get() == '' or select_widget.get() == '-' or select_widget.get().startswith('*'):
            return True
    return False

# Send info messages
def send_info(lang:str, msg: str, additional_msg_front: str = '', additional_msg_back: str = ''):
    langconfig_file = f'languages/locales/{lang}.ini'
    langconfig = configparser.ConfigParser()
    langconfig.read(langconfig_file, encoding='utf-8')
    CTkMessagebox(title='Info', message=f"{additional_msg_front}{langconfig['Info'][msg]}{additional_msg_back}", icon='check')

# Send error messages
def send_error(lang:str, msg: str, additional_msg_front: str = '', additional_msg_back: str = ''):
    langconfig_file = f'languages/locales/{lang}.ini'
    langconfig = configparser.ConfigParser()
    langconfig.read(langconfig_file, encoding='utf-8')
    CTkMessagebox(title='Error', message=f"{additional_msg_front}{langconfig['Error'][msg]}{additional_msg_back}", icon='cancel')