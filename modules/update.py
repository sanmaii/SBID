import version
import requests as req
import webbrowser
import configparser
from sbid_headers import *
from CTkMessagebox import CTkMessagebox

# Check if the version is up to date
def check_update(lang: str):
    api = req.get('https://api.github.com/repos/sanmaii/SBID/releases/latest', headers=headers)
    latest_version = api.json()['tag_name']
    current_version = f'v{version.version}'
    # If there is an update available
    if latest_version != current_version:
        langconfig_file = f'languages/locales/{lang}.ini'
        langconfig = configparser.ConfigParser()
        langconfig.read(langconfig_file, encoding='utf-8')
        msg = CTkMessagebox(title=langconfig['Update']['title'], message=f"{langconfig['Update']['msg']}\n{langconfig['Update']['latest']} {latest_version}\n{langconfig['Update']['current']} {current_version}",
                    option_1=langconfig['Update']['no'], option_2=langconfig['Update']['yes'], icon='question', button_width=100)
        ans = msg.get()
        return ans

# Guide to the latest version
def pull_latest():
    webbrowser.open('https://github.com/sanmaii/SBID/releases/latest')