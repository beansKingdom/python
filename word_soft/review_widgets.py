# -*- coding: UTF-8 -*-

from Tkinter import *
import tkMessageBox
import ScrolledText as tkst
import toolstips as tltp
import ttk

class ReviewFrame:
    def __init__(self, parent):
        self.root = parent

    def show(self):
        # add label widget
        nums_lb = Label(self.root, text="nums : ")
        nums_lb.grid(row=0)
        tltp.createToolTip(nums_lb, 'The max number of review words')           # Add a Tooltip to the label widget

        # add entry widget
        num_val = StringVar()
        num_entry = Entry(self.root, textvariable=num_val, width=6)
        num_val.set("50")
        num_entry.grid(row=0, column=1, sticky=W)

        # add combobox widget
        # the review types : english - chinese or chinese - english or mix
        self.review_type = ttk.Combobox(self.root, width=10, text = "", state='readonly')
        self.review_type['values'] = ("review_type", "eng-chin", "chin-eng", "mix")
        self.review_type.current(0)
        self.review_type.grid(row=0, column=2, sticky=W)

        # add a start button
        start_bt = Button(self.root,  text="start", width=12, command=self.start)
        start_bt.grid(row=0, column=3, sticky=W)

        # add last and next button
        self.last_bt = Button(self.root, text="last", command=self.last_wd)
        self.next_bt = Button(self.root, text="next", command=self.next_wd)
        self.rem_bt = Button(self.root, text="remember", command=self.last_wd, width=10)
        self.obl_bt = Button(self.root, text="oblivious", command=self.next_wd, width=10)
        self.last_bt.grid(row=4)
        self.rem_bt.grid(row=5, column=1)
        self.obl_bt.grid(row=5, column=2, sticky=E)
        self.next_bt.grid(row=4, column=3, sticky=W)

        self.check_bt = Button(self.root, text="check_word", width=12, state='disabled')
        self.check_bt.grid(row=3, column=3, sticky=W)

        # add word_label and mean_text widget
        self.word_var = StringVar()
        self.word_lb = Entry(self.root, textvariable=self.word_var, width=27)
        self.word_lb.grid(row=3, column=1, columnspan=2, sticky=W)

        self.edit_space = tkst.ScrolledText(master=self.root, bg='beige', width=25, height=4)
        self.edit_space.grid(row=4, column=1, columnspan=2, sticky=W)

    def next_wd(self):
        pass

    def last_wd(self):
        pass

    def start(self):
        re_type = self.review_type.current()
        if re_type == 0 or re_type == 1:
            self.check_bt.configure(state='disabled')
        else:
            self.check_bt.configure(state='normal')
        # add

#=======================================
def display_widgets(parent):
    rev = ReviewFrame(parent)

    rev.show()