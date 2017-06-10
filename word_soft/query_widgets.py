# -*- coding: UTF-8 -*-

from Tkinter import *
import search_func
import ScrolledText as tkst
import toolstips as tltp

class QueryFrame:
    def __init__(self, parent):
        self.root = parent
        self.create_top = 0  # 0 : not create toplevel 1: otherwise

    def show(self):
        # add a search function
        # add a input entry
        text = StringVar()
        self.se_entry = Entry(self.root, width=37, textvariable=text)
        text.set("a")
        self.se_entry.bind('<Return>', self.search)
        self.se_entry.grid(row=0)

        # add a search button
        se_bt = Button(self.root,  text="serach", width=12, command=self.search)
        se_bt.bind('<Return>', self.search)
        se_bt.grid(row=0, column=1, sticky=W)

        # Add a Tooltip to the ScrolledText widget
        tltp.createToolTip(se_bt, 'Search the word by internet')

    def search(self, event = None):
        self.se_res = []
        search_func.get_html_content(self.se_entry.get(), self.se_res)
        if self.create_top == 0:
            self.win = Toplevel()
            self.create_top = 1
            self.meaning_scrolledtext = tkst.ScrolledText(master = self.win, bg='beige', width=50, height=5 )
            self.meaning_scrolledtext.grid(column=0, columnspan=2, sticky=W)


        self.display_res()

    def display_res(self):
        self.meaning_scrolledtext['state'] = 'normal'
        self.meaning_scrolledtext.delete('1.0', END)
        for key in self.se_res:
            if key != None:
                self.meaning_scrolledtext.insert('insert', key)
                self.meaning_scrolledtext.insert('insert', "\n")

        self.meaning_scrolledtext['state'] = 'disabled'
#=======================================
def display_widgets(parent):
    ins = QueryFrame(parent)

    ins.show()
