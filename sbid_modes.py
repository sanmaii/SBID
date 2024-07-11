import os
import requests as req
import member_list as mem
from bs4 import BeautifulSoup as bs
from tkinter import *

defaultbg = '#121212'
defaultfg = '#e3e3e3'
defaultrow = 11

class modes:

    def mode0(outputbox: Text, win, path_label, pathbtn: Button):

        rectxt = r'resources\mode0record.txt'
        if not os.path.exists(rectxt):
            with open(rectxt, mode='w') as f:
                f.write(f'Mode 0\n\n\n\n\n')
        
        outputbox.config(state='normal')
        outputbox.delete('1.0')
        outputbox.insert(END, 'The information will be shown here.\n')
        
        times_label = Label(win, text='Number of Folders:', bg=defaultbg, fg=defaultfg)
        times_label.grid(column=0,row=defaultrow, sticky=W)
        times_entry = Entry(win, width=10)
        times_entry.grid(column=0, row=defaultrow,padx=(120,0), sticky=W)

        small_num_label = Label(win, text='Smaller Number:', bg=defaultbg, fg=defaultfg)
        small_num_label.grid(column=0,row=defaultrow+1, sticky=W)
        small_num_entry = Entry(win, width=10)
        small_num_entry.grid(column=0, row=defaultrow+1,padx=(120,0), sticky=W)

        big_num_label = Label(win, text='Bigger Number:', bg=defaultbg, fg=defaultfg)
        big_num_label.grid(column=0,row=defaultrow+2, sticky=W)
        big_num_entry = Entry(win, width=10)
        big_num_entry.grid(column=0, row=defaultrow+2,padx=(120,0), sticky=W)

        with open(rectxt, mode='r', encoding='utf-8') as f:
            mode0record = f.readlines()
        outputbox.insert(END, f'Details of the previous job:\nPath: {mode0record[1]}Number of Folders: {mode0record[2]}\
Smaller Number: {mode0record[3]}Bigger Number: {mode0record[4]}')
        outputbox.config(state='disabled')


        def confirm():
            times_entry.config(state='disabled')
            small_num_entry.config(state='disabled')
            big_num_entry.config(state='disabled')
            confirmbtn.config(text='Settings Confirmed!', bg='#ff9c87', state='disabled', width=16)
            pathbtn.config(state='disabled')
            startbtn.config(state='normal')
        
        def check_finished():
            if 'Job finished.' in outputbox.get('1.0', END):
                times_entry.config(state='normal')
                small_num_entry.config(state='normal')
                big_num_entry.config(state='normal')
                confirmbtn.config(text='Confirm Settings', bg='#87ffbf', command=confirm, width=16, state='normal')
                pathbtn.config(state='normal')
                startbtn.config(state='disabled')


        def start_create():
            times = int(times_entry.get())
            small_num = int(small_num_entry.get())
            big_num = int(big_num_entry.get())
            created = 0
            while created < times:
                pathbtn.config(state='disabled')
                os.makedirs(path_label['text'] + '/' + str(small_num) + "-" + str(big_num))
                small_num = big_num + 1
                big_num += 1000
                created += 1
            outputbox.config(state='normal')
            outputbox.insert(END, 'Job finished.\n')
            outputbox.see(END)
            outputbox.config(state='disabled')
            win.update()
            check_finished()
            mode0record[1] = path_label['text']
            mode0record[2] = times_entry.get()
            mode0record[3] = small_num_entry.get()
            mode0record[4] = big_num_entry.get()
            with open(rectxt, mode='w', encoding='utf-8') as f:
                f.write(f'Mode 0\n{mode0record[1]}\n{mode0record[2]}\n{mode0record[3]}\n{mode0record[4]}\n')

        confirmbtn = Button(text='Confirm Settings', bg='#87ffbf', command=confirm, width=16)
        confirmbtn.grid(column=0, row=defaultrow+3, sticky=W)

        anno = Label(win, text='Note: Smaller Number and Bigger Number refer to the names of the first image and the last image in the folder, respectively.\n\
For example: Smaller Number = 1 and Bigger Number = 1000 means that the first image and the last image in the folder are 1.jpg and 1000.jpg.\n\
The difference of the folders is 1000. (e.g. 1-200 for the first one, 201-1200 for the second one.)\n\
Of course, this requires you to move them manually to fit the name of the folder, since I am not willing to provide this function, at least for this moment. a.k.a. lazy',
justify=LEFT, wraplength=480, bg=defaultbg, fg=defaultfg)
        anno.grid(column=0, row=defaultrow+4, sticky=W)

        startbtn = Button(text='Start Job', bg='#a70404', fg=defaultfg, command=start_create, state='disabled')
        startbtn.grid(column=1, row=defaultrow+1)

    def mode1(outputbox: Text, win, path_label, pathbtn: Button):

        outputbox.config(state='normal')
        outputbox.delete('1.0')
        outputbox.insert(END, 'The information will be shown here.\n')
        outputbox.config(state='disabled')

        url_label = Label(win, text='URL:', bg=defaultbg, fg=defaultfg)
        url_label.grid(column=0, row=defaultrow, sticky=W)
        url_entry = Entry(win, width=59)
        url_entry.grid(column=0, row=defaultrow, padx=(44,0), sticky=W)

        def confirm():
            confirmbtn.config(text='Settings Confirmed!', bg='#ff9c87', state='disabled', width=16)
            pathbtn.config(state='disabled')
            startbtn.config(state='normal')
            url_entry.config(state='disabled')

        def check_finished():
            if 'Job finished.' in outputbox.get('1.0', END):
                confirmbtn.config(text='Confirm Settings', bg='#87ffbf', command=confirm, width=16, state='normal')
                pathbtn.config(state='normal')
                startbtn.config(state='disabled')
                url_entry.config(state='normal')

        def startjob():
            url = url_entry.get()
            r = req.get(url)
            file = url[url.rfind("/"):]
            filename = path_label['text'] + '/' + file[1:]        
            with open(filename, mode='wb') as img:
                img.write(r.content)
            outputbox.config(state='normal')
            outputbox.insert(END, filename + '\n')
            outputbox.insert(END, 'Job finished.\n')
            outputbox.see(END)
            outputbox.config(state='disabled')
            win.update()
            check_finished()
        
        confirmbtn = Button(text='Confirm Settings', bg='#87ffbf', command=confirm, width=16)
        confirmbtn.grid(column=0, row=defaultrow+1, sticky=W)

        anno = Label(text='Note: You must supply scheme! (https://)',justify=LEFT, wraplength=480, bg=defaultbg, fg=defaultfg)
        anno.grid(column=0, row=defaultrow+2, sticky=W)

        startbtn = Button(text='Start Job', bg='#a70404', fg=defaultfg, command=startjob, state='disabled')
        startbtn.grid(column=1, row=defaultrow+1)
            
    def mode2(outputbox: Text, win, path_label, pathbtn: Button):

        outputbox.config(state='normal')
        outputbox.delete('1.0')
        outputbox.insert(END, 'The information will be shown here.\n')
        outputbox.config(state='disabled')

        bid_label = Label(text='Blog Number:', bg=defaultbg, fg=defaultfg)
        bid_label.grid(column=0, row=defaultrow, sticky=W)
        bid_entry = Entry(win, width=10)
        bid_entry.grid(column=0, row=defaultrow, padx=(100), sticky=W)

        def confirm():
            confirmbtn.config(text='Settings Confirmed!', bg='#ff9c87', state='disabled', width=16)
            pathbtn.config(state='disabled')
            startbtn.config(state='normal')
            bid_entry.config(state='disabled')

        def check_finished():
            if 'Job finished.' in outputbox.get('1.0', END):
                confirmbtn.config(text='Confirm Settings', bg='#87ffbf', command=confirm, width=16, state='normal')
                pathbtn.config(state='normal')
                startbtn.config(state='disabled')
                bid_entry.config(state='normal')

        def startjob():
            url = 'https://www.nogizaka46.com/s/n46/diary/detail/'
            bid = bid_entry.get()
            page = req.get(url + bid)
            source = bs(page.content, "html.parser")
            images = source.find_all("img")

            for img in images:
                imglink = img.attrs.get("src")
                loc = "https://www.nogizaka46.com" + imglink
                imgdl = req.get(loc).content
                file = imglink[imglink.rfind("/"):]
                filename = path_label['text'] + '/' + file[1:]
                with open(filename, mode='wb') as img:
                    img.write(imgdl)
                outputbox.config(state='normal')
                outputbox.insert(END, filename + ' ' + imglink + '\n')
                outputbox.see(END)
                outputbox.config(state='disabled')
                win.update()
            outputbox.config(state='normal')
            outputbox.insert(END, 'Job finished.\n')
            outputbox.see(END)
            outputbox.config(state='disabled')
            check_finished()

        confirmbtn = Button(text='Confirm Settings', bg='#87ffbf', command=confirm, width=16)
        confirmbtn.grid(column=0, row=defaultrow+1, sticky=W)

        anno = Label(text='Note: There is a way for you to find blog number in Mode 4.',justify=LEFT, wraplength=480, bg=defaultbg, fg=defaultfg)
        anno.grid(column=0, row=defaultrow+2, sticky=W)

        startbtn = Button(text='Start Job', bg='#a70404', fg=defaultfg, command=startjob, state='disabled')
        startbtn.grid(column=1, row=defaultrow+1)

    def mode3(outputbox: Text, win, path_label, pathbtn: Button):

        outputbox.config(state='normal')
        outputbox.delete('1.0')
        outputbox.insert(END, 'The information will be shown here.\n')
        outputbox.config(state='disabled')

        bid_label = Label(text='Blog Number to Start With:', bg=defaultbg, fg=defaultfg)
        bid_label.grid(column=0, row=defaultrow, sticky=W)
        bid_entry = Entry(win, width=10)
        bid_entry.grid(column=0, row=defaultrow, padx=(170), sticky=W)

        max_label = Label(text='Blog Number to End With:', bg=defaultbg, fg=defaultfg)
        max_label.grid(column=0, row=defaultrow+1, sticky=W)
        max_entry = Entry(win, width=10)
        max_entry.grid(column=0, row=defaultrow+1, padx=(170), sticky=W)
        
        name_label = Label(text='Image Number:', bg=defaultbg, fg=defaultfg)
        name_label.grid(column=0, row=defaultrow+2, sticky=W)
        name_entry = Entry(win, width=10)
        name_entry.grid(column=0, row=defaultrow+2, padx=(170), sticky=W)

        def confirm():
            confirmbtn.config(text='Settings Confirmed!', bg='#ff9c87', state='disabled', width=16)
            pathbtn.config(state='disabled')
            startbtn.config(state='normal')
            bid_entry.config(state='disabled')
            max_entry.config(state='disabled')
            name_entry.config(state='disabled')

        def check_finished():
            if 'Job finished.' in outputbox.get('1.0', END):
                confirmbtn.config(text='Confirm Settings', bg='#87ffbf', command=confirm, width=16, state='normal')
                pathbtn.config(state='normal')
                startbtn.config(state='disabled')
                bid_entry.config(state='normal')
                max_entry.config(state='normal')
                name_entry.config(state='normal')

        def startjob():
            startbtn.config(state='disabled')
            url = 'https://www.nogizaka46.com/s/n46/diary/detail/'
            bid = int(bid_entry.get())
            max = int(max_entry.get())
            name = int(name_entry.get())

            while bid <= max:
                if bid < 35979:
                    bid = 35979
                elif bid in range(65327,100041):
                    bid = 100042
                page = req.get(url + str(bid))
                if page.status_code == 404:
                    bid +=1
                    continue
                source = bs(page.content, "html.parser")
                images = source.find_all("img")
                for img in images:  # images is a list.
                    imglink = img.attrs.get("src")
                    if (imglink is None or not imglink.startswith("/") or imglink.endswith('gif')):
                        continue
                    loc = "https://www.nogizaka46.com" + imglink
                    response = req.head(loc)
                    if response.status_code != 200:
                        continue
                    imgdl = req.get(loc).content
                    filename = path_label['text'] + '/' + str(name) + '.jpg'
                    name += 1
                    with open(filename, mode='wb') as f:
                        f.write(imgdl)
                    outputbox.config(state='normal')
                    outputbox.insert(END, filename + ' ' + imglink + '\n')
                    outputbox.see(END)
                    outputbox.config(state='disabled')
                    win.update()
                bid += 1
            outputbox.config(state='normal')
            outputbox.insert(END, 'Job finished.\n')
            outputbox.see(END)
            outputbox.config(state='disabled')
            check_finished()

        confirmbtn = Button(text='Confirm Settings', bg='#87ffbf', command=confirm, width=16)
        confirmbtn.grid(column=0, row=defaultrow+3, sticky=W)

        anno = Label(text='Note: Image Number refers to the name of the first image.\n\
Images in blogs which have been deleted cannot be downloaded.',justify=LEFT, wraplength=480, bg=defaultbg, fg=defaultfg)
        anno.grid(column=0, row=defaultrow+4, sticky=W)

        startbtn = Button(text='Start Job', bg='#a70404', fg=defaultfg, command=startjob, state='disabled')
        startbtn.grid(column=1, row=defaultrow+1)

    def mode4(outputbox: Text, win, path_label, pathbtn: Button):

        rectxt = r'resources\mode4record.txt'
        if not os.path.exists(rectxt):
            with open(rectxt, mode='w') as f:
                f.write(f'Mode 4\n\n\n\n\n')
        
        outputbox.config(state='normal')
        outputbox.delete('1.0')
        outputbox.insert(END, 'The information will be shown here.\n')

        mem_label = Label(text='Member Number:', bg=defaultbg, fg=defaultfg)
        mem_label.grid(column=0, row=defaultrow, sticky=W)
        mem_entry = Entry(win, width=10)
        mem_entry.grid(column=0, row=defaultrow, padx=(120), sticky=W)

        bid_label = Label(text='Blog Number:', bg=defaultbg, fg=defaultfg)
        bid_label.grid(column=0, row=defaultrow+1, sticky=W)
        bid_entry = Entry(win, width=10)
        bid_entry.grid(column=0, row=defaultrow+1, padx=(120), sticky=W)

        name_label = Label(text='Image Number:', bg=defaultbg, fg=defaultfg)
        name_label.grid(column=0, row=defaultrow+2, sticky=W)
        name_entry = Entry(win, width=10)
        name_entry.grid(column=0, row=defaultrow+2, padx=(120), sticky=W)

        with open(rectxt, mode='r', encoding='utf-8') as f:
            mode4record = f.readlines()
        outputbox.insert(END, f'Details of the previous job:\nPath: {mode4record[1]}Member: {mode4record[2]}\
Blog Number: {mode4record[3]}Last Image Number: {mode4record[4]}')
        outputbox.config(state='disabled')

        def print_mid():
            outputbox.config(state=NORMAL)
            outputbox.insert(END, mem.n46members() + '\n')
            outputbox.config(state=DISABLED)

        def print_blog():
            domain = 'https://www.nogizaka46.com'
            main = 'https://www.nogizaka46.com/s/n46/diary/MEMBER/list?ct='
            if mem_entry.get() == '':
                outputbox.config(state=NORMAL)
                outputbox.insert(END, 'You must enter Member Number first!\n')
                outputbox.config(state=DISABLED)
            else:
                mem = mem_entry.get()
                bloglist = main + mem
                bloglist_page_detail = req.get(bloglist)
                bloglist_source = bs(bloglist_page_detail.content, 'html.parser')
                last_page = bloglist_source.select('div._pager a')[0]['href']
                last_page_url = domain + last_page
                last_page_detail = req.get(last_page_url)
                last_page_source = bs(last_page_detail.content, 'html.parser')
                last_blog = last_page_source.select('div.bl--list a')[-1]['href']
                blogurl = domain + last_blog
                while True:
                    blogurl_detail = req.get(blogurl)
                    blogurl_source = bs(blogurl_detail.content, 'html.parser')
                    next_page = blogurl_source.select('a.bd--hn__a.hv--op')
                    kiji = blogurl_source.find('p', string = '次の記事')
                    if (not next_page or not kiji):
                        outputbox.config(state=NORMAL)
                        outputbox.insert(END, blogurl[blogurl.rfind('/')+1:blogurl.rfind('?')] + '\n')
                        outputbox.insert(END, blogurl_source.select('h1.bd--hd__ttl')[0].text +'\n')
                        outputbox.config(state=DISABLED)
                        win.update()
                        break
                    for link in next_page:
                        next_page_link = link.get('href')
                        if not '次の記事' in link.text:
                            continue
                        outputbox.config(state=NORMAL)
                        outputbox.insert(END, blogurl[blogurl.rfind('/')+1:blogurl.rfind('?')] + '\n')
                        outputbox.insert(END, blogurl_source.select('h1.bd--hd__ttl')[0].text +'\n')
                        outputbox.see(END)
                        outputbox.config(state=DISABLED)
                        win.update()
                        blogurl = domain + next_page_link
                outputbox.config(state=NORMAL)
                outputbox.insert(END, 'All the blogs are shown above.\n')
                outputbox.see(END)
                outputbox.config(state=DISABLED)


        def confirm():
            confirmbtn.config(text='Settings Confirmed!', bg='#ff9c87', state='disabled', width=16)
            pathbtn.config(state='disabled')
            startbtn.config(state='normal')
            bid_entry.config(state='disabled')
            mem_entry.config(state='disabled')
            name_entry.config(state='disabled')
            bid_need_help.config(state='disabled')
            mid_need_help.config(state='disabled')

        def check_finished():
            if 'Job finished.' in outputbox.get('1.0', END):
                confirmbtn.config(text='Confirm Settings', bg='#87ffbf', command=confirm, width=16, state='normal')
                pathbtn.config(state='normal')
                startbtn.config(state='disabled')
                bid_entry.config(state='normal')
                mem_entry.config(state='normal')
                name_entry.config(state='normal')
                bid_need_help.config(state='normal')
                mid_need_help.config(state='disabled')

        def startjob():
            domain = 'https://www.nogizaka46.com'
            main = 'https://www.nogizaka46.com/s/n46/diary/detail/'
            bid = bid_entry.get()
            name = int(name_entry.get())
            url = main + bid

            while True:
                page_detail = req.get(url)
                source = bs(page_detail.content, "html.parser")
                images = source.select('div.bd--edit')[0].select('img')
                for img in images:
                    imgurl = img.attrs.get("src")
                    if (imgurl is None or imgurl == "" or imgurl.endswith('gif') or not imgurl.startswith("/")):
                        continue
                    response = req.head(domain + imgurl)
                    if response.status_code != 200:
                        continue
                    imgdl = req.get(domain + imgurl).content
                    filename = path_label['text'] + '/' + str(name) + '.jpg'
                    name += 1
                    with open(filename, mode='wb') as f:
                        f.write(imgdl)
                    outputbox.config(state=NORMAL)
                    outputbox.insert(END, f'{filename} {imgurl} \n')
                    outputbox.see(END)
                    outputbox.config(state=DISABLED)
                    win.update()
                next_page = source.select('a.bd--hn__a.hv--op')    # Both previous and next blog are selected.
                kiji = source.find('p', string = '次の記事')    # For finding if there are blogs behind.
                if (not next_page or not kiji):    # If there is no blog left then ends.
                    break
                next_page_link = next_page[-1].get('href')    # The first element in the list(next_page) normally is the previous blog, so we choose the last one.
                url = domain + next_page_link
            outputbox.config(state='normal')
            outputbox.insert(END, 'Job finished.\n')
            outputbox.see(END)
            outputbox.config(state='disabled')
            check_finished()
            mode4record[1] = path_label['text']
            if mem_entry.get() != '':
                mode4record[2] = f'{source.select("p.bd--prof__name.f--head")[0].text} ({mem_entry.get()})'
            else:
                mode4record[2] = f'{source.select("p.bd--prof__name.f--head")[0].text} ({mem.n46dict[source.select("p.bd--prof__name.f--head")[0].text]})'
            mode4record[3] = source.select('div.bd--cmt__in.js-apicomment')[0].attrs.get('data-api')\
                [source.select('div.bd--cmt__in.js-apicomment')[0].attrs.get('data-api').rfind('=')+1:]
            mode4record[4] = str(name-1)
            with open(rectxt, mode='w', encoding='utf-8') as f:
                f.write(f'Mode 4\n{mode4record[1]}\n{mode4record[2]}\n{mode4record[3]}\n{mode4record[4]}\n')

        mid_need_help = Button(text='Help', bg='#f4ae2f', command=print_mid, width=8)
        mid_need_help.grid(column=0, row=defaultrow, padx=(200), sticky=W)

        bid_need_help = Button(text='Help', bg='#f4ae2f', command=print_blog, width=8)
        bid_need_help.grid(column=0, row=defaultrow+1, padx=(200), sticky=W)

        confirmbtn = Button(text='Confirm Settings', bg='#87ffbf', command=confirm, width=16)
        confirmbtn.grid(column=0, row=defaultrow+3, sticky=W)

        anno = Label(text='Note: Click the Help Button if you do not know the Member Number, same as Blog Number.',justify=LEFT, wraplength=480, bg=defaultbg, fg=defaultfg)
        anno.grid(column=0, row=defaultrow+4, sticky=W)

        startbtn = Button(text='Start Job', bg='#a70404', fg=defaultfg, command=startjob, state='disabled')
        startbtn.grid(column=1, row=defaultrow+1)

    def mode5(outputbox: Text, win, path_label, pathbtn: Button):

        rectxt = r'resources\mode5record.txt'
        if not os.path.exists(rectxt):
            with open(rectxt, mode='w') as f:
                f.write(f'Mode 5\n\n\n\n\n')
        
        outputbox.config(state='normal')
        outputbox.delete('1.0')
        outputbox.insert(END, 'The information will be shown here.\n')

        mem_label = Label(text='Member Number:', bg=defaultbg, fg=defaultfg)
        mem_label.grid(column=0, row=defaultrow, sticky=W)
        mem_entry = Entry(win, width=10)
        mem_entry.grid(column=0, row=defaultrow, padx=(120), sticky=W)

        bid_label = Label(text='Blog Number:', bg=defaultbg, fg=defaultfg)
        bid_label.grid(column=0, row=defaultrow+1, sticky=W)
        bid_entry = Entry(win, width=10)
        bid_entry.grid(column=0, row=defaultrow+1, padx=(120), sticky=W)

        name_label = Label(text='Image Number:', bg=defaultbg, fg=defaultfg)
        name_label.grid(column=0, row=defaultrow+2, sticky=W)
        name_entry = Entry(win, width=10)
        name_entry.grid(column=0, row=defaultrow+2, padx=(120), sticky=W)

        with open(rectxt, mode='r', encoding='utf-8') as f:
            mode5record = f.readlines()
        outputbox.insert(END, f'Details of the previous job:\nPath: {mode5record[1]}Member: {mode5record[2]}\
Blog Number: {mode5record[3]}Last Image Number: {mode5record[4]}')
        outputbox.config(state='disabled')

        domain = 'https://www.hinatazaka46.com'

        def print_mid():
            outputbox.config(state=NORMAL)
            outputbox.insert(END, mem.h46members() + '\n')
            outputbox.config(state=DISABLED)

        def print_blog():
            main = 'https://www.hinatazaka46.com/s/official/diary/member/list?ct='
            if mem_entry.get() == '':
                outputbox.config(state=NORMAL)
                outputbox.insert(END, 'You must enter Member Number first!\n')
                outputbox.config(state=DISABLED)
            else:
                mem = mem_entry.get()
                bloglist = main + mem
                while True:
                    bloglist_detail = req.get(bloglist)
                    bloglist_source = bs(bloglist_detail.content, 'html.parser')
                    biggest_page = bloglist_source.select('div.p-pager.p-pager--count > li.c-pager__item--count:not(.is-disable)')[-1]
                    biggest_page_url = biggest_page.select('a')
                    if not biggest_page_url:
                        break
                    biggest_page_url = biggest_page_url[0]['href']
                    bloglist = domain + biggest_page_url
                bloglist_detail = req.get(bloglist)
                bloglist_source = bs(bloglist_detail.content, 'html.parser')
                lastblog = bloglist_source.select('div.p-blog-article')[-1].select('a.c-button-blog-detail')[-1]['href']
                blogurl = domain + lastblog
                while True:
                    blogurl_detail = req.get(blogurl)
                    blogurl_source = bs(blogurl_detail.content, 'html.parser')
                    outputbox.config(state=NORMAL)
                    outputbox.insert(END, blogurl[blogurl.rfind('/')+1:blogurl.rfind('?')] + '\n')
                    outputbox.insert(END, blogurl_source.select('div.c-blog-article__title')[0].text.strip() +'\n')    # Or using re.sub(r'^\s+|\s+$').
                    outputbox.see(END)
                    outputbox.config(state=DISABLED)
                    win.update()
                    next_page = blogurl_source.select('div.c-pager__item.c-pager__item--next.c-pager__item--kiji.c-pager__item--kiji__blog > a')
                    if not next_page:
                        break
                    next_page_url = next_page[0]['href']
                    blogurl = domain + next_page_url
                outputbox.config(state=NORMAL)
                outputbox.insert(END, 'All the blogs are shown above.\n')
                outputbox.see(END)
                outputbox.config(state=DISABLED)

        def confirm():
            confirmbtn.config(text='Settings Confirmed!', bg='#ff9c87', state='disabled', width=16)
            pathbtn.config(state='disabled')
            startbtn.config(state='normal')
            bid_entry.config(state='disabled')
            mem_entry.config(state='disabled')
            name_entry.config(state='disabled')
            bid_need_help.config(state='disabled')
            mid_need_help.config(state='disabled')

        def check_finished():
            if 'Job finished.' in outputbox.get('1.0', END):
                confirmbtn.config(text='Confirm Settings', bg='#87ffbf', command=confirm, width=16, state='normal')
                pathbtn.config(state='normal')
                startbtn.config(state='disabled')
                bid_entry.config(state='normal')
                mem_entry.config(state='normal')
                name_entry.config(state='normal')
                bid_need_help.config(state='normal')
                mid_need_help.config(state='disabled')

        def startjob():
            main = 'https://www.hinatazaka46.com/s/official/diary/detail/'
            bid = bid_entry.get()
            name = int(name_entry.get())
            url = main + bid

            while True:
                page_detail = req.get(url)
                source = bs(page_detail.content, "html.parser")
                images = source.select('div.p-blog-article')[0].select('img')
                for img in images:  # images is a list.
                    imgurl = img.attrs.get("src")
                    if (imgurl is None or imgurl == "") or not imgurl.endswith("jpg"):
                        continue
                    response = req.head(imgurl)
                    if response.status_code != 200:
                        continue
                    imgdl = req.get(imgurl).content
                    filename = path_label['text'] + '/' + str(name) + '.jpg'
                    name += 1
                    with open(filename, mode='wb') as f:
                        f.write(imgdl)
                    outputbox.config(state=NORMAL)
                    outputbox.insert(END, f'{filename} {imgurl} \n')
                    outputbox.see(END)
                    outputbox.config(state=DISABLED)
                    win.update()
                next_page = source.select('div.c-pager__item.c-pager__item--next.c-pager__item--kiji.c-pager__item--kiji__blog > a')
                if not next_page:
                    break
                for link in next_page:
                    next_page_link = link["href"]
                    url = domain + next_page_link
            outputbox.config(state='normal')
            outputbox.insert(END, 'Job finished.\n')
            outputbox.see(END)
            outputbox.config(state='disabled')
            check_finished()
            mode5record[1] = path_label['text']
            if mem_entry.get() != '':
                mode5record[2] = f'{source.select("div.c-blog-member__name")[0].text.strip()} ({mem_entry.get()})'
            else:
                mode5record[2] = f'{source.select("div.c-blog-member__name")[0].text.strip()} ({mem.h46dict[source.select("div.c-blog-member__name")[0].text.strip()]})'
            mode5record[3] = source.find('meta', attrs={'property': 'og:url'}).get('content')\
                [source.find('meta', attrs={'property': 'og:url'}).get('content').rfind('/')+1:source.find('meta', attrs={'property': 'og:url'}).get('content').rfind('?')]
            mode5record[4] = str(name-1)
            with open(rectxt, mode='w', encoding='utf-8') as f:
                f.write(f'Mode 5\n{mode5record[1]}\n{mode5record[2]}\n{mode5record[3]}\n{mode5record[4]}\n')

        mid_need_help = Button(text='Help', bg='#f4ae2f', command=print_mid, width=8)
        mid_need_help.grid(column=0, row=defaultrow, padx=(200), sticky=W)

        bid_need_help = Button(text='Help', bg='#f4ae2f', command=print_blog, width=8)
        bid_need_help.grid(column=0, row=defaultrow+1, padx=(200), sticky=W)

        confirmbtn = Button(text='Confirm Settings', bg='#87ffbf', command=confirm, width=16)
        confirmbtn.grid(column=0, row=defaultrow+3, sticky=W)

        anno = Label(text='Note: Click the Help Button if you do not know the Member Number, same as Blog Number.',justify=LEFT, wraplength=480, bg=defaultbg, fg=defaultfg)
        anno.grid(column=0, row=defaultrow+4, sticky=W)

        startbtn = Button(text='Start Job', bg='#a70404', fg=defaultfg, command=startjob, state='disabled')
        startbtn.grid(column=1, row=defaultrow+1)

    def mode6(outputbox: Text, win, path_label, pathbtn: Button):

        rectxt = r'resources\mode6record.txt'
        if not os.path.exists(rectxt):
            with open(rectxt, mode='w') as f:
                f.write(f'Mode 6\n\n\n\n\n')

        outputbox.config(state='normal')
        outputbox.delete('1.0')
        outputbox.insert(END, 'The information will be shown here.\n')

        mem_label = Label(text='Member Number:', bg=defaultbg, fg=defaultfg)
        mem_label.grid(column=0, row=defaultrow, sticky=W)
        mem_entry = Entry(win, width=10)
        mem_entry.grid(column=0, row=defaultrow, padx=(120), sticky=W)

        bid_label = Label(text='Blog Number:', bg=defaultbg, fg=defaultfg)
        bid_label.grid(column=0, row=defaultrow+1, sticky=W)
        bid_entry = Entry(win, width=10)
        bid_entry.grid(column=0, row=defaultrow+1, padx=(120), sticky=W)

        name_label = Label(text='Image Number:', bg=defaultbg, fg=defaultfg)
        name_label.grid(column=0, row=defaultrow+2, sticky=W)
        name_entry = Entry(win, width=10)
        name_entry.grid(column=0, row=defaultrow+2, padx=(120), sticky=W)

        with open(rectxt, mode='r', encoding='utf-8') as f:
            mode6record = f.readlines()
        outputbox.insert(END, f'Details of the previous job:\nPath: {mode6record[1]}Member: {mode6record[2]}\
Blog Number: {mode6record[3]}Last Image Number: {mode6record[4]}')
        outputbox.config(state='disabled')

        domain = 'https://www.sakurazaka46.com'

        def print_mid():
            outputbox.config(state=NORMAL)
            outputbox.insert(END, mem.s46members() + '\n')
            outputbox.config(state=DISABLED)

        def print_blog():
            main = 'https://sakurazaka46.com/s/s46/diary/blog/list?ct='
            if mem_entry.get() == '':
                outputbox.config(state=NORMAL)
                outputbox.insert(END, 'You must enter Member Number first!\n')
                outputbox.config(state=DISABLED)
            else:
                mem = mem_entry.get()
                bloglist = main + mem
                bloglist_page_detail = req.get(bloglist)
                bloglist_source = bs(bloglist_page_detail.content, 'html.parser')
                last_page = bloglist_source.select('div.com-pager.wid1200 a')[-1]['href']
                last_page_url = domain + last_page
                last_page_detail = req.get(last_page_url)
                last_page_source = bs(last_page_detail.content, 'html.parser')
                last_blog = last_page_source.select('ul.com-blog-part.box3.fxpc > li a')[-1]['href']
                blogurl = domain + last_blog
                while True:
                    blogurl_detail = req.get(blogurl)
                    blogurl_source = bs(blogurl_detail.content, 'html.parser')
                    outputbox.config(state=NORMAL)
                    outputbox.insert(END, blogurl[blogurl.rfind('/')+1:blogurl.rfind('?')] + '\n')
                    outputbox.insert(END, blogurl_source.select('h1.title')[0].text +'\n')
                    outputbox.see(END)
                    outputbox.config(state=DISABLED)
                    win.update()
                    next_page = blogurl_source.select('p.btn-type1s.wf-a.pos-right > a')
                    if not next_page:
                        break
                    next_page_url = next_page[0]['href']
                    blogurl = domain + next_page_url
                outputbox.config(state=NORMAL)
                outputbox.insert(END, 'All the blogs are shown above.\n')
                outputbox.see(END)
                outputbox.config(state=DISABLED)

        def confirm():
            confirmbtn.config(text='Settings Confirmed!', bg='#ff9c87', state='disabled', width=16)
            pathbtn.config(state='disabled')
            startbtn.config(state='normal')
            bid_entry.config(state='disabled')
            mem_entry.config(state='disabled')
            name_entry.config(state='disabled')
            bid_need_help.config(state='disabled')
            mid_need_help.config(state='disabled')

        def check_finished():
            if 'Job finished.' in outputbox.get('1.0', END):
                confirmbtn.config(text='Confirm Settings', bg='#87ffbf', command=confirm, width=16, state='normal')
                pathbtn.config(state='normal')
                startbtn.config(state='disabled')
                bid_entry.config(state='normal')
                mem_entry.config(state='normal')
                name_entry.config(state='normal')
                bid_need_help.config(state='normal')
                mid_need_help.config(state='disabled')

        def startjob():
            main = 'https://www.sakurazaka46.com/s/s46/diary/detail/'
            bid = bid_entry.get()
            name = int(name_entry.get())
            url = main + bid

            while True:
                page_detail = req.get(url)
                source = bs(page_detail.content, "html.parser")
                images = source.select('div.box-article')[0].select('img')
                for img in images:  # images is a list.
                    imglink = img.attrs.get("src")
                    if (imglink is None or imglink == ""):
                        continue
                    elif not imglink:
                        break
                    imgurl = domain + imglink
                    response = req.head(imgurl)
                    if response.status_code != 200:
                        continue
                    imgdl = req.get(imgurl).content
                    filename = path_label['text'] + '/' + str(name) + '.jpg'
                    name += 1
                    with open(filename, mode='wb') as f:
                        f.write(imgdl)
                    outputbox.config(state=NORMAL)
                    outputbox.insert(END, f'{filename} {imgurl} \n')
                    outputbox.see(END)
                    outputbox.config(state=DISABLED)
                    win.update()
                next_page = source.select('p.btn-type1s.wf-a.pos-right > a[href]')
                if not next_page:
                    break
                for link in next_page:
                    next_page_link = link["href"]
                    url = domain + next_page_link  
            outputbox.config(state='normal')
            outputbox.insert(END, 'Job finished.\n')
            outputbox.see(END)
            outputbox.config(state='disabled')
            check_finished()
            mode6record[1] = path_label['text']
            if mem_entry.get() != '':
                mode6record[2] = f'{source.select("p.name")[0].text} ({mem_entry.get()})'
            else:
                mode6record[2] = f'{source.select("div.blog-foot div.txt p.name")[0].text} ({mem.s46dict[source.select("div.blog-foot div.txt p.name")[0].text]})'
            mode6record[3] = source.find('meta', attrs={'property': 'og:url'}).get('content')\
                [source.find('meta', attrs={'property': 'og:url'}).get('content').rfind('/')+1:source.find('meta', attrs={'property': 'og:url'}).get('content').rfind('?')]
            mode6record[4] = str(name-1)
            with open(rectxt, mode='w', encoding='utf-8') as f:
                f.write(f'Mode 6\n{mode6record[1]}\n{mode6record[2]}\n{mode6record[3]}\n{mode6record[4]}\n')

        mid_need_help = Button(text='Help', bg='#f4ae2f', command=print_mid, width=8)
        mid_need_help.grid(column=0, row=defaultrow, padx=(200), sticky=W)

        bid_need_help = Button(text='Help', bg='#f4ae2f', command=print_blog, width=8)
        bid_need_help.grid(column=0, row=defaultrow+1, padx=(200), sticky=W)

        confirmbtn = Button(text='Confirm Settings', bg='#87ffbf', command=confirm, width=16)
        confirmbtn.grid(column=0, row=defaultrow+3, sticky=W)

        anno = Label(text='Note: Click the Help Button if you do not know the Member Number, same as Blog Number.',justify=LEFT, wraplength=480, bg=defaultbg, fg=defaultfg)
        anno.grid(column=0, row=defaultrow+4, sticky=W)

        startbtn = Button(text='Start Job', bg='#a70404', fg=defaultfg, command=startjob, state='disabled')
        startbtn.grid(column=1, row=defaultrow+1)

    def mode7(outputbox: Text, win, path_label, pathbtn: Button):
        outputbox.config(state='normal')
        outputbox.delete('1.0')
        outputbox.insert(END, 'The information will be shown here.\n')
        outputbox.config(state='disabled')

        mem_label = Label(text='Member Number:', bg=defaultbg, fg=defaultfg)
        mem_label.grid(column=0, row=defaultrow, sticky=W)
        mem_entry = Entry(win, width=10)
        mem_entry.grid(column=0, row=defaultrow, padx=(120), sticky=W)

        bid_label = Label(text='Blog Number:', bg=defaultbg, fg=defaultfg)
        bid_label.grid(column=0, row=defaultrow+1, sticky=W)
        bid_entry = Entry(win, width=10)
        bid_entry.grid(column=0, row=defaultrow+1, padx=(120), sticky=W)

        name_label = Label(text='Image Number:', bg=defaultbg, fg=defaultfg)
        name_label.grid(column=0, row=defaultrow+2, sticky=W)
        name_entry = Entry(win, width=10)
        name_entry.grid(column=0, row=defaultrow+2, padx=(120), sticky=W)

        domain = 'https://www.keyakizaka46.com'

        def print_mid():
            outputbox.config(state=NORMAL)
            outputbox.insert(END, mem.k46members() + '\n')
            outputbox.config(state=DISABLED)

        def print_blog():
            main = 'https://www.keyakizaka46.com/s/k46o/diary/member/list?ct='
            if mem_entry.get() == '':
                outputbox.config(state=NORMAL)
                outputbox.insert(END, 'You must enter Member Number first!\n')
                outputbox.config(state=DISABLED)
            else:
                mem = mem_entry.get()
                bloglist = main + mem
                while True:
                    bloglist_detail = req.get(bloglist)
                    bloglist_source = bs(bloglist_detail.content, 'html.parser')
                    biggest_page = bloglist_source.select('div.pager > ul > li')[-1]
                    biggest_page_url = biggest_page.select('a')
                    if not biggest_page_url:
                        break
                    biggest_page_url = biggest_page_url[0]['href']
                    bloglist = domain + biggest_page_url
                bloglist_detail = req.get(bloglist)
                bloglist_source = bs(bloglist_detail.content, 'html.parser')
                lastblog = bloglist_source.select('div.box-main > article')[-1].select('li.singlePage > a')[0]['href']
                blogurl = domain + lastblog
                while True:
                    blogurl_detail = req.get(blogurl)
                    blogurl_source = bs(blogurl_detail.content, 'html.parser')
                    outputbox.config(state=NORMAL)
                    outputbox.insert(END, blogurl[blogurl.rfind('/')+1:blogurl.rfind('?')] + '\n')
                    outputbox.insert(END, blogurl_source.select('div.box-ttl > h3')[0].text.strip() +'\n')    # Or using re.sub(r'^\s+|\s+$').
                    outputbox.see(END)
                    outputbox.config(state=DISABLED)
                    win.update()
                    next_page = blogurl_source.select('div.btn-navi.btn-next > a')
                    if not next_page:
                        break
                    next_page_url = next_page[0]['href']
                    blogurl = domain + next_page_url
                outputbox.config(state=NORMAL)
                outputbox.insert(END, 'All the blogs are shown above.\n')
                outputbox.see(END)
                outputbox.config(state=DISABLED)

        def confirm():
            confirmbtn.config(text='Settings Confirmed!', bg='#ff9c87', state='disabled', width=16)
            pathbtn.config(state='disabled')
            startbtn.config(state='normal')
            bid_entry.config(state='disabled')
            mem_entry.config(state='disabled')
            name_entry.config(state='disabled')
            bid_need_help.config(state='disabled')
            mid_need_help.config(state='disabled')

        def check_finished():
            if 'Job finished.' in outputbox.get('1.0', END):
                confirmbtn.config(text='Confirm Settings', bg='#87ffbf', command=confirm, width=16, state='normal')
                pathbtn.config(state='normal')
                startbtn.config(state='disabled')
                bid_entry.config(state='normal')
                mem_entry.config(state='normal')
                name_entry.config(state='normal')
                bid_need_help.config(state='normal')
                mid_need_help.config(state='disabled')

        def startjob():
            main = 'https://www.keyakizaka46.com/s/k46o/diary/detail/'
            bid = bid_entry.get()
            name = int(name_entry.get())
            url = main + bid

            while True:
                page_detail = req.get(url)
                source = bs(page_detail.content, "html.parser")
                images = source.select('div.box-article')[0].select('img')
                for image in images:
                    imglink = image.attrs.get("src")
                    if (imglink is None or imglink == ""):
                        continue
                    elif not imglink:
                        break
                    response = req.head(imglink)
                    if response.status_code != 200:
                        continue
                    imgdl = req.get(imglink).content
                    filename = path_label['text'] + '/' + str(name) + '.jpg'
                    name += 1
                    with open(filename, mode='wb') as f:
                        f.write(imgdl)
                    outputbox.config(state=NORMAL)
                    outputbox.insert(END, f'{filename} {imglink} \n')
                    outputbox.see(END)
                    outputbox.config(state=DISABLED)
                    win.update()
                next_page = source.select('div.btn-navi.btn-next > a[href]')
                if not next_page:
                    break
                for link in next_page:
                    next_page_link = link["href"]
                    url = domain + next_page_link
            outputbox.config(state='normal')
            outputbox.insert(END, 'Job finished.\n')
            outputbox.see(END)
            outputbox.config(state='disabled')
            check_finished()

        mid_need_help = Button(text='Help', bg='#f4ae2f', command=print_mid, width=8)
        mid_need_help.grid(column=0, row=defaultrow, padx=(200), sticky=W)

        bid_need_help = Button(text='Help', bg='#f4ae2f', command=print_blog, width=8)
        bid_need_help.grid(column=0, row=defaultrow+1, padx=(200), sticky=W)

        confirmbtn = Button(text='Confirm Settings', bg='#87ffbf', command=confirm, width=16)
        confirmbtn.grid(column=0, row=defaultrow+3, sticky=W)

        anno = Label(text='Note: Click the Help Button if you do not know the Member Number, same as Blog Number.',justify=LEFT, wraplength=480, bg=defaultbg, fg=defaultfg)
        anno.grid(column=0, row=defaultrow+4, sticky=W)

        startbtn = Button(text='Start Job', bg='#a70404', fg=defaultfg, command=startjob, state='disabled')
        startbtn.grid(column=1, row=defaultrow+1)