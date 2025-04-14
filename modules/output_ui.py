import output
from customtkinter import *

def output_ui():
    # Basic properties
    output_window = CTkToplevel()
    output_window.title("Output")
    w_mon = output_window.winfo_screenwidth()
    h_mon = output_window.winfo_screenheight()
    w_size = int(w_mon/2.4)
    h_size = int(h_mon/2.8)
    output_window.geometry('%dx%d' % (w_size, h_size))
    output_window.resizable(0,0)
    output_window.configure(padx=20, pady=20)


    def setup_ui(win: CTkToplevel):
        # Set up the user interface
        win.grid_rowconfigure(0, weight=1)
        win.grid_columnconfigure(0, weight=1)

        # Textbox for output
        global outputbox
        outputbox = CTkTextbox(win, wrap='word', state='disabled')
        outputbox.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

    setup_ui(output_window)

def insert_msg(msg: str):
    output.output(outputbox, msg)