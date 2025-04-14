# Get the title, member and date of the latest blog of h46.

from h46_get_latest_blog_num import *

def get_h46_latest_blog_info():
    latest_blog_num, latest_blog_content = get_h46_latest_blog_num()
    title = latest_blog_content.select('p.c-blog-main__title')[0].text
    member = latest_blog_content.select('div.c-blog-main__name')[0].text
    date = latest_blog_content.select('time.c-blog-main__date')[0].text
    return latest_blog_num, title, member, date