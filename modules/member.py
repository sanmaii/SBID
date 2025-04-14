import requests as req
import configparser
import os
import threading
from sbid_headers import *


n46mem_config_file = 'members/n46mem.ini'
s46mem_config_file = 'members/s46mem.ini'
h46mem_config_file = 'members/h46mem.ini'
n46memconfig = configparser.ConfigParser()
s46memconfig = configparser.ConfigParser()
h46memconfig = configparser.ConfigParser()

# Get the member list from repo
def fetch_member_list():
    member_url = 'https://raw.githubusercontent.com/sanmaii/SBID/main/members/members.json'
    response = req.get(member_url, headers=headers)
    members = response.json()
    return members

# Load the config file
# If the config file does not exist, create one
def load_member_config(members):
    # Nogizaka config
    if os.path.exists(n46mem_config_file):
        n46memconfig.read(n46mem_config_file, encoding='utf-8')
    else:
        for i in members['n46members']:
            n46memconfig[i] = {'last_blog': '',
                                'directory': '',
                                'img_num': ''}
        with open(n46mem_config_file, 'w', encoding='utf-8') as f:
            n46memconfig.write(f)

    # Sakurazaka config
    if os.path.exists(s46mem_config_file):
        s46memconfig.read(s46mem_config_file, encoding='utf-8')
    else:
        for i in members['s46members']:
            s46memconfig[i] = {'last_blog': '',
                                'directory': '',
                                'img_num': ''}
        with open(s46mem_config_file, 'w', encoding='utf-8') as f:
            s46memconfig.write(f)

    # Hinatazaka config
    if os.path.exists(h46mem_config_file):
        h46memconfig.read(h46mem_config_file, encoding='utf-8')
    else:
        for i in members['h46members']:
            h46memconfig[i] = {'last_blog': '',
                                'directory': '',
                                'img_num': ''}
        with open(h46mem_config_file, 'w', encoding='utf-8') as f:
            h46memconfig.write(f)

# Update the member config to ensure it is up to date with the member list if available
def update_mem_config(members):
    nogi_members = members['n46members']
    sakura_members = members['s46members']
    hinata_members = members['h46members']
    def update_nogi_config():
        for member in nogi_members:
            if not n46memconfig.has_section(member):
                n46memconfig[member] = {'last_blog': '',
                                    'directory': '',
                                    'img_num': ''}
        with open(n46mem_config_file, 'w', encoding='utf-8') as f:
            n46memconfig.write(f)

    def update_sakura_config():
        for member in sakura_members:
            if not s46memconfig.has_section(member):
                s46memconfig[member] = {'last_blog': '',
                                    'directory': '',
                                    'img_num': ''}
        with open(s46mem_config_file, 'w', encoding='utf-8') as f:
            s46memconfig.write(f)

    def update_hinata_config():
        for member in hinata_members:
            if not h46memconfig.has_section(member):
                h46memconfig[member] = {'last_blog': '',
                                    'directory': '',
                                    'img_num': ''}
        with open(h46mem_config_file, 'w', encoding='utf-8') as f:
            h46memconfig.write(f)

    t1 = threading.Thread(target=update_nogi_config())
    t2 = threading.Thread(target=update_sakura_config())
    t3 = threading.Thread(target=update_hinata_config())
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()