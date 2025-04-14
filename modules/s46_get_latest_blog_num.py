# Get the latest blog number of s46.

import requests as req
from bs4 import BeautifulSoup as bs
from sbid_headers import *

def get_s46_latest_blog_num():
    s46_blog_list_content = bs(req.get('https://sakurazaka46.com/s/s46/diary/blog/list', headers=headers).content, 'html.parser')
    latest_blog = s46_blog_list_content.select('li.box a')[0]['href']
    latest_blog_num = latest_blog[latest_blog.rfind('/')+1:latest_blog.rfind('?')]
    return latest_blog_num, s46_blog_list_content