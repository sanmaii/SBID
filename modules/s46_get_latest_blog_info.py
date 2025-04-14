# Get the title, member and date of the latest blog of s46.

from s46_get_latest_blog_num import *

def get_s46_latest_blog_info():
    latest_blog_num, s46_blog_list_content = get_s46_latest_blog_num()
    title = s46_blog_list_content.select('h3.title')[0].text
    member = s46_blog_list_content.select('p.name')[0].text
    latest_blog_content = bs(req.get(f'https://sakurazaka46.com/s/s46/diary/detail/{latest_blog_num}', headers=headers).content, 'html.parser')
    date = latest_blog_content.select('div.blog-foot p.date.wf-a')[0].text
    return latest_blog_num, title, member, date