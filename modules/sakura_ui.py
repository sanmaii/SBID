import configparser
import sakura
import webbrowser
from customtkinter import *

def sakura_ui(lang: str):
    # Basic properties
    sakura_window = CTkToplevel()
    sakura_window.title("Sakurazaka46")
    w_mon = sakura_window.winfo_screenwidth()
    h_mon = sakura_window.winfo_screenheight()
    w_size = int(w_mon/2.5)
    h_size = int(h_mon/2.2)
    sakura_window.geometry('%dx%d' % (w_size, h_size))
    sakura_window.resizable(0,0)
    sakura_window.configure(padx=20, pady=20)

    # Language config
    langconfig_file = f'languages/locales/{lang}.ini'
    langconfig = configparser.ConfigParser()
    langconfig.read(langconfig_file, encoding='utf-8')
    
    def setup_ui(win: CTkToplevel):
        # Set up the user interface
        win.grid_rowconfigure(0, weight=1)
        win.grid_columnconfigure(0, weight=1)
        
        #Set up frame
        frame = CTkFrame(win)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        frame.grid_columnconfigure(1, weight=1)

        # Latest blog
        latest_blog_text = CTkLabel(frame, text=langconfig['DL']['latest_blog'])
        latest_blog_text.grid(row=0, column=0, padx=10, pady=10)
        latest_blog_label = CTkLabel(frame, text=sakura.get_latest_blog()[1], font=CTkFont(size=20), fg_color=('gray60', 'gray40'),
                                     width=w_size-120, cursor='hand2', corner_radius=10)
        latest_blog_label.grid(row=0, column=1, padx=10, pady=10)
        latest_blog_label.bind('<Button-1>', lambda x: webbrowser.open(f'https://sakurazaka46.com/s/s46/diary/detail/{sakura.get_latest_blog()[0]}'))

        # Member selection
        member_select_text = CTkLabel(frame, text=langconfig['DL']['select_member'])
        member_select_text.grid(row=1, column=0, padx=10, pady=10)
        member_menu = CTkOptionMenu(frame, width=120)
        member_menu.set('-')
        member_menu.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        member_menu.configure(values=sakura.get_members(), command=lambda x: sakura.get_blogs(member_menu.get(), blog_menu, lang, langconfig, dir_label, image_num_entry))

        # Blog selection
        blog_select_text = CTkLabel(frame, text=langconfig['DL']['select_blog'])
        blog_select_text.grid(row=2, column=0, padx=10, pady=10)
        blog_menu = CTkOptionMenu(frame, width=120, state='disabled')
        blog_menu.set('-')
        blog_menu.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        # Blog entry
        enter_blog_text = CTkLabel(frame, text=langconfig['DL']['enter_blog'])
        enter_blog_text.grid(row=3, column=0, padx=10, pady=10)
        blog_entry = CTkEntry(frame, width=100, corner_radius=10, placeholder_text=langconfig['DL']['blog_entry_placeholder'])
        blog_entry.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        # Directory selection
        dir_select_text = CTkLabel(frame, text=langconfig['DL']['select_dir'])
        dir_select_text.grid(row=4, column=0, padx=10, pady=10)
        dir_label = CTkLabel(frame, text='', font=CTkFont(size=20), fg_color=('gray60', 'gray40'), width=w_size-120, corner_radius=10)
        dir_label.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        # Directory related buttons
        select_dir_btn = CTkButton(frame, text=langconfig['DL']['select'], command=lambda: sakura.select_dir(dir_label), cursor='hand2', width=60)
        select_dir_btn.grid(row=5, column=1, padx=10, pady=10, sticky='w')
        open_dir_btn = CTkButton(frame, text=langconfig['DL']['open'], command=lambda: sakura.open_dir(dir_label.cget('text')), cursor='hand2', width=60)
        open_dir_btn.grid(row=5, column=1, padx=80, pady=10, sticky='w')

        # Image number entry
        image_num_text = CTkLabel(frame, text=langconfig['DL']['img_num'])
        image_num_text.grid(row=6, column=0, padx=10, pady=10)
        image_num_entry = CTkEntry(frame, width=100, corner_radius=10, placeholder_text=langconfig['DL']['img_num_entry_placeholder'])
        image_num_entry.grid(row=6, column=1, padx=10, pady=10, sticky='w')

        # Download
        dl_text = CTkLabel(frame, text=langconfig['DL']['dl'])
        dl_text.grid(row=7, column=0, padx=10, pady=10)
        dl_single_btn = CTkButton(frame, width=120, fg_color='#910c14', text=langconfig['DL']['dl_single'], hover_color='#6e0b12',
                                command=lambda: sakura.download(member_menu.get(), lang, member_menu, blog_menu, blog_entry, select_dir_btn,
                                open_dir_btn,image_num_entry, dl_single_btn, dl_latest_btn, dir_label, 'single'))
        dl_single_btn.grid(row=7, column=1, sticky='w', padx=10, pady=10)       
        dl_latest_btn = CTkButton(frame, width=120, fg_color='#910c14', text=langconfig['DL']['dl_latest'], hover_color='#6e0b12',
                                  command=lambda: sakura.download(member_menu.get(), lang, member_menu, blog_menu, blog_entry, select_dir_btn,
                                open_dir_btn,image_num_entry, dl_single_btn, dl_latest_btn, dir_label, 'latest'))
        dl_latest_btn.grid(row=7, column=1, sticky='w', padx=160, pady=10)   

    setup_ui(sakura_window)