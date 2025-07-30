import h46_get_latest_blog_info
import requests as req
import utils
import threading
import configparser
import output_ui
import h46dl
import member as mem
from sbid_headers import *
from customtkinter import *
from bs4 import BeautifulSoup as bs

# Get the latest blog
def get_latest_blog():
    latest_blog_num, title, member, date = h46_get_latest_blog_info.get_h46_latest_blog_info()
    return latest_blog_num, f'{latest_blog_num} --- {title.strip()}\n{member.strip()} {date.replace(".", "/")} (GMT+9)'

# Get the members from the member list
def get_members():
    return mem.fetch_member_list()['h46members']

# Get the latest blogs of the selected member
def get_blogs(member: str, blog_menu: CTkOptionMenu, lang: str, langconfig: configparser.ConfigParser, dir_label: CTkLabel, img_num_entry: CTkEntry):
    mem_config_file = 'members/h46mem.ini'
    mem_config = configparser.ConfigParser()
    mem_config.read(mem_config_file, encoding='utf-8')
    domain = 'https://www.hinatazaka46.com/s/official/diary/member/list?ct='
    mid = mem.fetch_member_list()['h46dict'].get(member)
    blog_list = domain + mid
    blog_page = 1
    count = 0
    i = 0
    blogs = []
    while count < blog_page:
        try:
            bloglist_detail = req.get(blog_list, headers=headers)
            bloglist_source = bs(bloglist_detail.content, 'html.parser')
            blog_count = len(bloglist_source.select('a.c-button-blog-detail'))
            half = blog_count/2
            if half < 1:
                half == 1
            else:
                half = int(half)
            def get_half(small_num: int, big_num: int):
                while small_num < big_num:                   
                    blog_order = bloglist_source.select('a.c-button-blog-detail')[small_num]['href']
                    blog_num = blog_order[blog_order.rfind('/')+1:blog_order.rfind('?')]
                    blog_title = bloglist_source.select('div.c-blog-article__title')[small_num].text.strip()
                    if len(blog_title) > 30:
                        blog_title = utils.cut_str(blog_title, 30)
                    blogs.append(f'{blog_num} {blog_title}')
                    small_num += 1
            count += 1
        except IndexError:
            count += 1
            i = 0
    t1 = threading.Thread(target=get_half(i, half))
    t2 = threading.Thread(target=get_half(half, blog_count))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # Automatically select the blog
    last_blog = mem_config[member]['last_blog']
    if last_blog == '':
        auto_opt = langconfig['DL']['auto_not_available']
    else:
        for i in range(2):
            domain = 'https://www.hinatazaka46.com/s/official/diary/detail/'
            url = domain + last_blog
            page_detail = req.get(url, timeout=60, headers=headers)
            source = bs(page_detail.content, 'html.parser')
            if i == 1:
                blog_title = source.select('div.c-blog-article__title')[0].text.strip()
                auto_opt = f"{last_blog} {blog_title} {langconfig['DL']['auto']}"
            else:
                next_blog = source.select('div.c-pager__item.c-pager__item--next.c-pager__item--kiji.c-pager__item--kiji__blog > a')
                if not next_blog:
                    blog_title = source.select('div.c-blog-article__title')[0].text.strip()
                    auto_opt = langconfig['DL']['auto_not_available']
                    break
                for link in next_blog:
                    next_page_link = link['href']
                    last_blog = next_page_link[next_page_link.rfind('/')+1:next_page_link.rfind('?')]
    blog_menu.set(auto_opt)  
    blogs_values = ['-', auto_opt, *blogs]
    blog_menu.configure(values=blogs_values, state='normal')

    # Automatically select the directory
    last_dir = mem_config[member]['directory']
    if last_dir == '':
        dir_label.configure(text='')
    else:
        if len(last_dir) > 50:
            last_dir = utils.cut_str(last_dir, 50)
        dir_label.configure(text=last_dir)

    # Automatically insert the image number
    try:
        last_img_num = mem_config[member]['img_num']
        img_num_entry.delete(0, 'end')
        num = int(last_img_num) + 1
        img_num_entry.insert(0, num)
    except:
        img_num_entry.configure(placeholder_text=langconfig['DL']['img_num_entry_placeholder'])
    utils.send_info(lang, 'blogs_loaded')


# Select a directory
def select_dir(dir_label: CTkLabel):
    directory = filedialog.askdirectory()
    if len(directory) > 35:
        directory = utils.cut_str(directory, 50)
    dir_label.configure(text=directory)

# Open the selected directory
def open_dir(directory: str):
    try:
        os.startfile(utils.concat_dir(directory=directory))
    except Exception:
        os.startfile(os.path.realpath(__file__))

# Download images
def download(member: str, lang: str, mem_menu: CTkOptionMenu, blog_menu: CTkOptionMenu, blog_entry: CTkEntry,
                    select_dir_btn: CTkButton, open_dir_btn: CTkButton, img_num_entry: CTkEntry, dl_single_btn: CTkButton, dl_latest_btn: CTkButton, dir_label: CTkLabel,
                    mode: str):
    mem_config_file = 'members/h46mem.ini'
    mem_config = configparser.ConfigParser()
    mem_config.read(mem_config_file, encoding='utf-8')
    main = 'https://www.hinatazaka46.com/s/official/diary/detail/'
    if blog_menu.get() != '-' and not blog_menu.get().startswith('*'):
        bid = blog_menu.get()[:5]
    elif (blog_menu.get() == '-' or blog_menu.get().startswith('*')) and blog_entry.get().isdigit():
        temp_bid = blog_entry.get()
        if len(blog_entry.get()) == 5:
            if req.head(main + temp_bid).status_code != 200:
                utils.send_error(lang, 'provide_valid_blog_num')
                return
            else:
                temp_source = bs(req.get(main + temp_bid, headers=headers).content, 'html.parser')
                ts_name = temp_source.select('div.c-blog-article__name')[0].text.strip()
                if ts_name != mem_menu.get():
                    utils.send_error(lang, 'unmatched_member', additional_msg_back=f' {member}')
                    return
                else:
                    bid = temp_bid
        else:
            utils.send_error(lang, 'provide_valid_blog_num')
            return
    elif not img_num_entry.get().isdigit():
        utils.send_error(lang, 'provide_valid_img_num')
        return
    else:
        if not blog_entry.get().isdigit():
            utils.send_error(lang, 'provide_valid_blog_num')
            return
        elif utils.check_select(mem_menu, blog_menu):
            utils.send_error(lang, 'select_essential')
            return
    img_num = int(img_num_entry.get())
    url = main + bid
    utils.disable_widgets(mem_menu, blog_menu, blog_entry, select_dir_btn, open_dir_btn, img_num_entry, dl_single_btn, dl_latest_btn)
    output_ui.output_ui()
    bid, directory, img_num, dl_count = h46dl.dl(img_num, url, dir_label.cget('text'), mode)
    utils.send_info(lang, additional_msg_front=f"{str(dl_count)} ", msg='images_downloaded')
    utils.enable_widgets(mem_menu, blog_menu, blog_entry, select_dir_btn, open_dir_btn, img_num_entry, dl_single_btn, dl_latest_btn)

    # Modify the config file
    utils.modify_config(mem_config_file, member, 'last_blog', bid)
    utils.modify_config(mem_config_file, member, 'directory', directory)
    utils.modify_config(mem_config_file, member, 'img_num', str(img_num))
