import requests as req
import sbid_modes as pwtm
import threading
import os
import webbrowser
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from datetime import datetime
from bs4 import BeautifulSoup as bs

class App:
    def __init__(self, win):    
        self.win = win
        self.latest_blog_timer = None
    
    def app_initialize(self):
        self.basic_config()
        self.create_menu()
        self.centre_window(1280, 720)
        self.show_mode_description('#121212', '#e3e3e3', 'left', 0, 0)
        self.get_current_time()
        self.get_directory()
        self.create_output_detail_box()
        self.get_latest_blogs_num()
        self.win.title('SBID')
        self.win.protocol('WM_DELETE_WINDOW', self.quit_ui)
    
    def basic_config(self):
        self.win.title('Initializing...')
        self.win.config(bg='#121212')
        self.win.resizable(0,0)
        self.win.iconbitmap(self.get_icon_path(r'resources\138.ico'))

    def get_icon_path(self, iconloc):
        if os.path.exists(iconloc):
            return iconloc
        elif os.path.exists(iconloc[iconloc.rfind('\\')+1:]):
            return iconloc[iconloc.rfind('\\')+1:]
        else:
            return None
        
    def create_menu(self):
        self.menu = Menu(self.win)
        self.win.config(menu=self.menu)
        self.modemenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='Modes', menu=self.modemenu)
        self.menu_add_modes()

    def centre_window(self, w, h):
        ws = self.win.winfo_screenwidth()
        hs = self.win.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.win.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def show_mode_description(self, bg: str, fg: str, justify: str, column: int, row: int):
        description_title = Label(text='Description:', font='"Yu Gothic" 20', justify=justify, bg=bg, fg=fg)
        description_title.grid(column=column, row=row, sticky=W)
        modes_des = [
            'Mode 0: Create folders.',
            'Mode 1: Download the image from the URL directly.',
            'Mode 2: Download all images from one blog. (乃木坂46)',
            'Mode 3: Download all images from blogs continuously. (乃木坂46)',
            'Mode 4: Download all images from one member only. (乃木坂46)',
            'Mode 5: Download all images from one member only. (日向坂46)',
            'Mode 6: Download all images from one member only. (櫻坂46)',
            'Mode 7: Download all images from one member only. (欅坂46)'
        ]
        for i, mode in enumerate(modes_des):
            mode_label = Label(text=mode, font='Meiryo 12', justify=justify, bg=bg, fg=fg)
            mode_label.grid(column=column, row=i+1, sticky=W)

    def get_directory(self):
        def savepath():
            path = askdirectory()
            path_label.config(text=path)
        blank = Label(text='', bg='#121212')
        blank.grid(column=0, row=9)
        path = ''
        path_label = Label(text=path, width=65, relief=SUNKEN)
        path_label.grid(column=0, row=10, sticky=W)
        pathbtn = Button(text='Save Directory', command=savepath, bg='#bb86fc', cursor='hand2')
        pathbtn.grid(column=1, row=10)
        return path_label, pathbtn

    def get_current_time(self):
        time_label = Label(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), font='"Segoe UI" 14', bg='#121212', fg='#e3e3e3')
        time_label.place(relx=0.86, rely=0)
        time_label.after(1000, self.get_current_time)

    def openurl(self, domain, lbn):
            webbrowser.open(f'{domain}{lbn}')

    def n46latestblog(self, bg: str, fg: str, font: str):
        domain = 'https://www.nogizaka46.com/s/n46/diary/detail/'
        # filename = r'resources\n46latestblognum.txt'
        # try:
        #     with open(filename, 'r') as f:
        #         num = int(f.read())
        # except FileNotFoundError:
        #     num = 102610
        # bid = num
        # lbid = bid
        # while True:
        #     url = domain + str(bid)
        #     response = req.head(url)
        #     if response.status_code == 200:
        #         bid +=1
        #         lbid +=1
        #     else:
        #         lbid -=1
        #         code_list = []
        #         for i in range(5):
        #             bid +=1
        #             url = domain + str(bid)
        #             response = req.head(url)
        #             code_list.append(response.status_code)
        #             if response.status_code == 200:
        #                 lbid = bid
        #         if 200 not in code_list:
        #             break
        # url = domain + str(lbid)
        # with open(filename, 'w') as f:
        #     f.write(str(lbid))
        # latest_blog_num = url[url.rfind('/')+1:]
        napi = req.get('https://www.nogizaka46.com/s/n46/api/list/blog')
        data = bs(napi.content, 'html.parser')
        latest_blog_num = data.text[(data.text.index('"code":"') + len('"code":"')):(data.text.index('"', (data.text.index('"code":"') + len('"code":"'))))]
        url = domain + latest_blog_num
        member_get = bs(req.get(url).content, 'html.parser')
        member = member_get.select('p.bd--prof__name.f--head')[0].text
        date_get = bs(req.get(url).content, 'html.parser')
        date = date_get.select('p.bd--hd__date.a--tx.js-tdi')[0].text
        n46latestblog_label = Label(text=f'Latest Blog of 乃木坂46: {latest_blog_num} --- {member} {date.replace(".", "/")} (GMT+9)', bg=bg, fg=fg, font=font, cursor='hand2')
        n46latestblog_label.bind('<Button-1>', lambda event: self.openurl(domain, latest_blog_num))
        n46latestblog_label.grid(column=2, row=1, sticky=W)

    def s46latestblog(self, bg: str, fg: str, font: str):    
        html = bs(req.get('https://sakurazaka46.com/s/s46/diary/blog/list').content, 'html.parser')
        latest_blog = html.select('li.box > a')[0]['href']
        latest_blog_num = latest_blog[latest_blog.rfind('/')+1:latest_blog.rfind('?')]
        latest_blog_content = bs(req.get(f'https://sakurazaka46.com/s/s46/diary/detail/{latest_blog_num}').content, 'html.parser')
        member = latest_blog_content.select('div.blog-foot div.txt p.name')[0].text
        date = latest_blog_content.select('div.blog-foot div.txt p.date.wf-a')[0].text
        s46latestblog_label = Label(text=f'Latest Blog of 櫻坂46: {latest_blog_num} --- {member} {date} (GMT+9)', bg=bg, fg=fg, font=font, cursor='hand2')
        s46latestblog_label.bind('<Button-1>', lambda event: self.openurl('https://sakurazaka46.com/s/s46/diary/detail/', latest_blog_num))
        s46latestblog_label.grid(column=2, row=2, sticky=W)

    def h46latestblog(self, bg: str, fg: str, font: str):
        html = bs(req.get('https://www.hinatazaka46.com/s/official/diary/member').content, 'html.parser')
        latest_blog = html.select('a.p-blog-main__image')[0]['href']
        latest_blog_num = latest_blog[latest_blog.rfind('/')+1:latest_blog.rfind('?')]
        member = html.select('div.c-blog-main__name')[0].text
        date = html.select('time.c-blog-main__date')[0].text
        h46latestblog_label = Label(text=f'Latest Blog of 日向坂46: {latest_blog_num} --- {member.strip()} {date.replace(".", "/")} (GMT+9)',\
                                    bg=bg, fg=fg, font=font, cursor='hand2')
        h46latestblog_label.bind('<Button-1>', lambda event: self.openurl('https://www.hinatazaka46.com/s/official/diary/detail/', latest_blog_num))
        h46latestblog_label.grid(column=2, row=3, sticky=W)

    def get_latest_blogs_num(self):
        try:
            t1 = threading.Thread(target=self.n46latestblog('#121212', '#e3e3e3', '"Microsoft JhengHei" 14'))
            t2 = threading.Thread(target=self.s46latestblog('#121212', '#e3e3e3', '"Microsoft JhengHei" 14'))
            t3 = threading.Thread(target=self.h46latestblog('#121212', '#e3e3e3', '"Microsoft JhengHei" 14'))
            t1.start()
            t2.start()
            t3.start()
            t1.join()
        except Exception as e:
            pwtm.logging.error(f'{e} occurred while getting latest blogs.')
        finally:
            self.start_latest_blogs_num_timer()
    
    def start_latest_blogs_num_timer(self):
        self.latest_blog_timer = threading.Timer(600, self.get_latest_blogs_num)
        self.latest_blog_timer.start()
        pwtm.logging.info('Latest blogs are updated successfully.')

    def stop_latest_blogs_num_timer(self):
        if self.latest_blog_timer is not None:
            self.latest_blog_timer.cancel()

    def create_output_detail_box(self):
        outputbox = Text(self.win, width=92, height=27, border=2, state='disabled', cursor='arrow', wrap='word')
        outputbox.place(x=620, y=340)
        bar = Scrollbar(outputbox)
        bar.place(x=630, y=0, relheight=1)
        bar.config(command=outputbox.yview)
        outputbox.config(yscrollcommand=bar.set)
        return outputbox

    def clear_previous_mode_items(self):
        items = []
        try:
            items.extend(self.win.grid_slaves(column=0,row=11))
            items.extend(self.win.grid_slaves(column=0,row=12))
            items.extend(self.win.grid_slaves(column=1,row=12))
            items.extend(self.win.grid_slaves(column=0,row=13))
            items.extend(self.win.grid_slaves(column=0,row=14))
            items.extend(self.win.grid_slaves(column=0,row=15))            
        except:
            pass
        for i in items:
            i.destroy()
    modes = {
        'Mode 0': 'mode0',
        'Mode 1': 'mode1',
        'Mode 2': 'mode2',
        'Mode 3': 'mode3',
        'Mode 4': 'mode4',
        'Mode 5': 'mode5',
        'Mode 6': 'mode6',
        'Mode 7': 'mode7'        
    }

    def execute_mode(self, mode):
        self.clear_previous_mode_items()
        outputbox = self.create_output_detail_box()
        path_label, pathbtn = self.get_directory()
        getattr(pwtm.modes, mode)(outputbox, self.win, path_label, pathbtn)

    def menu_add_modes(self):
        for k, v in self.modes.items():
            self.modemenu.add_radiobutton(label=k, value=v, command= lambda mode=v: self.execute_mode(mode))
      
    def quit_ui(self):
        if messagebox.askokcancel('Exit', 'Are you sure to exit this program?\nThis will end all current tasks!'):
            self.stop_latest_blogs_num_timer()
            self.win.destroy()

def start_ui():
    window = Tk()
    ui = App(window)
    ui.app_initialize()
    window.mainloop()

start_ui()