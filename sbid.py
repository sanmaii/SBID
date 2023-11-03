import requests as req
import sbid_modes as pwtm
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from datetime import datetime
from bs4 import BeautifulSoup as bs

class app:
    def __init__(self, win):
        self.win = win
        self.win.title('Initializing...')
        self.win.config(bg='#121212')
        self.win.resizable(0,0)
        self.win.iconbitmap(r'resources\138.ico')
        self.menu = Menu(win)
        self.win.config(menu=self.menu)
        self.modemenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='Modes', menu=self.modemenu)
        self.menu_add_modes()
        self.center_window(1280, 720)
        self.des('#121212', '#e3e3e3', 'left', 0, 0)
        self.now()
        self.get_directory()
        self.outputdetail()
        self.n46latestblog('#121212', '#e3e3e3', '"Microsoft JhengHei" 14')
        self.s46latestblog('#121212', '#e3e3e3', '"Microsoft JhengHei" 14')
        self.h46latestblog('#121212', '#e3e3e3', '"Microsoft JhengHei" 14')

    def center_window(self, w, h):
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        win.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def des(self, bg: str, fg: str, justify: str, column: int, row: int):
        description_title = Label(text='Description:', font='"Yu Gothic" 20', justify=justify, bg=bg, fg=fg)
        description_title.grid(column=column, row=row, sticky=W)
        mode0des = Label(text='Mode 0: Create folders.',font='Meiryo 12', justify=justify, bg=bg, fg=fg)
        mode0des.grid(column=column, row=row+1, sticky=W)
        mode1des = Label(text='Mode 1: Download the image from the url of it directly.',font='Meiryo 12', justify=justify, bg=bg, fg=fg)
        mode1des.grid(column=column, row=row+2, sticky=W)
        mode2des = Label(text='Mode 2: Download all images from one blog. (乃木坂46)',font='Meiryo 12', justify=justify, bg=bg, fg=fg)
        mode2des.grid(column=column, row=row+3, sticky=W)
        mode3des = Label(text='Mode 3: Download all images from blogs continuously. (乃木坂46)',font='Meiryo 12', justify=justify, bg=bg, fg=fg)
        mode3des.grid(column=column, row=row+4, sticky=W)
        mode4des = Label(text='Mode 4: Download all images from one member only. (乃木坂46)',font='Meiryo 12', justify=justify, bg=bg, fg=fg)
        mode4des.grid(column=column, row=row+5, sticky=W)
        mode5des = Label(text='Mode 5: Download all images from one member only. (日向坂46)',font='Meiryo 12', justify=justify, bg=bg, fg=fg)
        mode5des.grid(column=column, row=row+6, sticky=W)
        mode6des = Label(text='Mode 6: Download all images from one member only. (櫻坂46)',font='Meiryo 12', justify=justify, bg=bg, fg=fg)
        mode6des.grid(column=column, row=row+7, sticky=W)
        mode7des = Label(text='Mode 7: Download all images from one member only. (欅坂46)',font='Meiryo 12', justify=justify, bg=bg, fg=fg)
        mode7des.grid(column=column, row=row+8, sticky=W)

    def get_directory(self):
        def savepath():
            path = askdirectory()
            path_label.config(text=path)
        blank = Label(text='', bg='#121212')
        blank.grid(column=0, row=9)
        path = ''
        path_label = Label(text=path, width=65, relief=SUNKEN)
        path_label.grid(column=0, row=10, sticky=W)
        pathbtn = Button(text='Save Directory', command=savepath, bg='#bb86fc')
        pathbtn.grid(column=1, row=10)
        return path_label, pathbtn

    def now(self):
        time_label = Label(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), font='"Segoe UI" 14', bg='#121212', fg='#e3e3e3')
        time_label.place(relx=0.86, rely=0)
        time_label.after(1000, self.now)

    def n46latestblog(self, bg: str, fg: str, font: str):
        domain = 'https://www.nogizaka46.com/s/n46/diary/detail/'
        bid = 102049
        url = domain + str(bid)
        searching = True
        while searching:
            url = domain + str(bid)
            response = req.head(url)
            if response.status_code == 200:
                bid +=1
            else:
                searching = False
        url = domain + str(bid-1)
        latest_blog_num = url[url.rfind('/')+1:]
        member_get = bs(req.get(url).content, 'html.parser')
        member = member_get.select('p.bd--prof__name.f--head')[0].text
        date_get = bs(req.get(url).content, 'html.parser')
        date = date_get.select('p.bd--hd__date.a--tx.js-tdi')[0].text
        n46latestblog_label = Label(text=f'Latest Blog of 乃木坂46: {latest_blog_num} --- {member} {date.replace(".", "/")} (GMT+9)', bg=bg, fg=fg, font=font)
        n46latestblog_label.grid(column=2, row=1, sticky=W)

    def s46latestblog(self, bg: str, fg: str, font: str):    
        html = bs(req.get('https://sakurazaka46.com/s/s46/diary/blog/list').content, 'html.parser')
        latest_blog = html.select('li.box > a')[0]['href']
        latest_blog_num = latest_blog[latest_blog.rfind('/')+1:latest_blog.rfind('?')]
        member = html.select('p.name')[0].text
        date = html.select('p.date.wf-a')[0].text
        s46latestblog_label = Label(text=f'Latest Blog of 櫻坂46: {latest_blog_num} --- {member} {date}', bg=bg, fg=fg, font=font)
        s46latestblog_label.grid(column=2, row=2, sticky=W)

    def h46latestblog(self, bg: str, fg: str, font: str):
        html = bs(req.get('https://www.hinatazaka46.com/s/official/diary/member').content, 'html.parser')
        latest_blog = html.select('a.p-blog-main__image')[0]['href']
        latest_blog_num = latest_blog[latest_blog.rfind('/')+1:latest_blog.rfind('?')]
        member = html.select('div.c-blog-main__name')[0].text
        date = html.select('time.c-blog-main__date')[0].text
        s46latestblog_label = Label(text=f'Latest Blog of 日向坂46: {latest_blog_num} --- {member.strip()} {date.replace(".", "/")} (GMT+9)', bg=bg, fg=fg, font=font)
        s46latestblog_label.grid(column=2, row=3, sticky=W)

    def outputdetail(self):
        outputbox = Text(win, width=92, height=27, border=2, state='disabled')
        outputbox.place(x=620, y=340)
        bar = Scrollbar(outputbox)
        bar.place(x=630, y=0, relheight=1)
        bar.config(command=outputbox.yview)
        outputbox.config(yscrollcommand=bar.set)
        return outputbox

    def clear_previous_mode_items(self):
        items = []
        try:
            items.extend(win.grid_slaves(column=0,row=11))
            items.extend(win.grid_slaves(column=0,row=12))
            items.extend(win.grid_slaves(column=1,row=12))
            items.extend(win.grid_slaves(column=0,row=13))
            items.extend(win.grid_slaves(column=0,row=14))
            items.extend(win.grid_slaves(column=0,row=15))            
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
        outputbox = self.outputdetail()
        path_label, pathbtn = self.get_directory()
        getattr(pwtm.modes, mode)(outputbox, win, path_label, pathbtn)

    def menu_add_modes(self):
        for k, v in self.modes.items():
            self.modemenu.add_radiobutton(label=k, value=v, command= lambda mode=v: self.execute_mode(mode))
      
def quit():
    if messagebox.askokcancel('Exit', 'Are you sure to exit this program?\nThis will end all current tasks!'):
        win.destroy()

win = Tk()
size = app.center_window(app, 1280, 720)
run = app(win)
win.title('SBID')
win.protocol('WM_DELETE_WINDOW', quit)
win.mainloop()
