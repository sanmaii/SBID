# Get the latest blog number of h46.

import requests as req
from bs4 import BeautifulSoup as bs
from sbid_headers import *

def get_h46_latest_blog_num():
    latest_blog_content = bs(req.get('https://www.hinatazaka46.com/s/official/diary/member', headers=headers).content, 'html.parser')
    latest_blog = latest_blog_content.select('a.p-blog-main__image')[0]['href']
    latest_blog_num = latest_blog[latest_blog.rfind('/')+1:latest_blog.rfind('?')]
    return latest_blog_num, latest_blog_content