# Get the title, member and date of the latest blog of n46.

from n46_get_latest_blog_num import *

def get_n46_latest_blog_info():
    latest_blog_num = get_n46_latest_blog_num()
    latest_blog_content = get_n46_latest_blog_content(latest_blog_num)
    title = latest_blog_content.select('h1.bd--hd__ttl.f--head.a--tx.js-tdi')[0].text
    member = latest_blog_content.select('p.bd--prof__name.f--head')[0].text
    date = latest_blog_content.select('p.bd--hd__date.a--tx.js-tdi')[0].text
    return latest_blog_num, title, member, date