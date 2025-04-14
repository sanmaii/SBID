# Get the latest blog number of n46.

import requests as req
from bs4 import BeautifulSoup as bs
from sbid_headers import *

def get_n46_latest_blog_num():
    napi = req.get('https://www.nogizaka46.com/s/n46/api/list/blog', headers=headers)
    data = bs(napi.content, 'html.parser')
    latest_blog_num = data.text[(data.text.index('"code":"') + len('"code":"')):(data.text.index('"', (data.text.index('"code":"') + len('"code":"'))))]
    return latest_blog_num

def get_n46_latest_blog_content(latest_blog_num: str):
    latest_blog_content = bs(req.get(f'https://www.nogizaka46.com/s/n46/diary/detail/{latest_blog_num}', headers=headers).content, 'html.parser')
    return latest_blog_content