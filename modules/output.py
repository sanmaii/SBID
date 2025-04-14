from customtkinter import *

def output(outputbox: CTkTextbox, msg: str):
    outputbox.configure(state='normal')
    outputbox.insert(END, msg)
    outputbox.see(END)
    outputbox.configure(state='disabled')
    outputbox.update()