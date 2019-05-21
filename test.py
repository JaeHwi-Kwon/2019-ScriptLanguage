from tkinter import *
from tkinter import ttk
import tkinter.messagebox


class App:

    def __init__(self):
        win = Tk()
        win.geometry("800x600")
        win.resizable(False, False)


        Tap = ttk.Notebook(win, width=500,height=600)
        Tap.pack(side=RIGHT)
        frameLeft = Frame(win)
        frameLeft.pack(side=LEFT, fill=BOTH, padx=5, pady=5)
        frameSearch = Frame(frameLeft,borderwidth=5, relief=RIDGE)
        frameList = Frame(frameLeft,borderwidth=5, relief=RIDGE)
        frameSearch.pack(side=TOP, fill=BOTH)
        frameList.pack(side=BOTTOM)
        frameMap = Frame(win, borderwidth=5, relief=RIDGE)
        framePlase = Frame(win, borderwidth=5, relief=RIDGE)
        frameTime = Frame(win, borderwidth=5, relief=RIDGE)
        Tap.add(frameMap, text='    지도    ')
        Tap.add(framePlase, text='  주변검색  ')
        Tap.add(frameTime, text='   시간표   ')




        self.input = Entry(frameSearch, width=30)
        self.input.pack(side=LEFT)
        Button(frameSearch,text='검색',command=self.Search).pack()
        scrollbar = Scrollbar(win)
        self.txtBox = Text(frameList, width=40,yscrollcommand=scrollbar.set)
        self.txtBox.pack(fill=BOTH)
        scrollbar.config(command=self.txtBox.yview)
        #scrollbar.grid(row=2,column=1)

        win.mainloop()

    def Search(self):
        pass

App()