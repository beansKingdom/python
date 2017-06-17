# -*- coding: UTF-8 -*-

from Tkinter import *
import tkMessageBox
import ScrolledText as tkst
import toolstips as tltp
import ttk
import pymysql
import get_conf as gcf
import random
import unicodedata

class ReviewFrame():
    def __init__(self, parent):
        self.root = parent
        self.mysql_dict = {}
        self.get_mysql_conf()
        self.connect_mysql()
        self.show()

    def get_mysql_conf(self):
        gcf.get_config(self.mysql_dict)

    def connect_mysql(self):
        try:
            # self.conn   : the connect of mysql
            self.conn = pymysql.connect(self.mysql_dict['my_host'], self.mysql_dict['my_user'], self.mysql_dict['my_passwd'],
                                        self.mysql_dict['my_dbname'],int(self.mysql_dict['my_port']), charset='utf8')
        except pymysql.Error as err:
            tkMessageBox.showerror("ERROR INFO", "Mysql Error %d: %s" % (err.args[0], err.args[1]))
            raise Exception("ERROR INFO : Mysql Error %d: %s" % (err.args[0], err.args[1]))
        self.cursor = self.conn.cursor()

    def show(self):
        num_lb = Label(self.root, text="nums : ")
        num_lb.grid(row=0)
        tltp.createToolTip(num_lb, 'The max number of review words\' numbers ')

        num_value = StringVar()
        self.num_entry = Entry(self.root, textvariable=num_value, width=6)
        num_value.set("5")
        self.num_entry.grid(row=0, column=1, sticky=W)

        # the review types : english - chinese or chinese - english or mix
        self.review_type_combobox = ttk.Combobox(self.root, width=10, text = "", state='readonly')
        self.review_type_combobox['values'] = ("review_type", "eng-chin", "chin-eng")
        self.review_type_combobox.current(0)
        self.review_type_combobox.grid(row=0, column=2, sticky=W)

        start_bt = Button(self.root,  text="start", width=12, command=self.start)
        start_bt.grid(row=0, column=3, sticky=W)

        self.last_bt = Button(self.root, text="last", command=self.last_word)
        self.remember_bt = Button(self.root, text="remember", command=self.is_remember_word, width=10)
        self.oblivious_bt = Button(self.root, text="oblivious", command=self.is_oblivious_word, width=10)
        self.show_meaning_bt = Button(self.root, text="show_meaning", command=self.show_meaning, width=12, state='disabled')
        self.last_bt.grid(row=4)
        self.show_meaning_bt.grid(row=4, column=3)
        self.remember_bt.grid(row=5, column=1)
        self.oblivious_bt.grid(row=5, column=2, sticky=E)

        self.verify_word_bt = Button(self.root, text="Verify", command=self.verify_word, width=12, state='disabled')
        self.verify_word_bt.grid(row=3, column=3, sticky=W)

        # add word_label and mean_text widget
        self.word_var = StringVar()
        self.word_entry= Entry(self.root, textvariable=self.word_var, width=27)
        self.word_entry.bind('<Return>', self.verify_word)
        self.word_entry.grid(row=3, column=1, columnspan=2, sticky=W)

        self.meaning_scrolledtext = tkst.ScrolledText(master=self.root, bg='beige', width=25, height=4, state='disabled')
        self.meaning_scrolledtext.grid(row=4, column=1, columnspan=2, sticky=W)

    def start(self):
        self.generate_words()
        self.judge_review_type()
        if self.review_type == 1:
            self.remember_bt.configure(state='normal')
            self.oblivious_bt.configure(state='normal')
        else:
            self.remember_bt.configure(state='disabled')
            self.oblivious_bt.configure(state='disabled')

    def generate_words(self):
        self.cursor.execute("select id, word, meaning from (select * from word_db order by ins_time) \
                            as temp where word_type != 1 or (CURDATE() + 0 - review_time)>=3 limit " + self.num_entry.get())
        self.conn.commit()

        # the result of slef.cursor.fetchall is tuple, now change it to list
        self.review_words_list = list(self.cursor.fetchall())

        self.remaining_review_words_nums_check(self.review_words_list)
        self.random_review_words()

    def judge_review_type(self):
        self.review_type = self.review_type_combobox.current()

        if self.review_type == 0:
            tkMessageBox.showerror("ERROR INFO", "You should choose one item from review_type")
            return 0
        elif self.review_type == 1:
            self.verify_word_bt.configure(state='disabled')
            self.show_meaning_bt.configure(state='normal')
            self.eng_chi_review()
        elif self.review_type == 2:
            self.verify_word_bt.configure(state='normal')
            self.show_meaning_bt.configure(state='disabled')
            self.word_entry.configure(state='normal')
            self.chi_eng_review()
        else:
            pass

    def eng_chi_review(self):
        self.show_word_entry_value(self.random_words_index_list[0])
        self.clean_meanning_text_value()

    def chi_eng_review(self):
        self.show_meanning_text_value(self.random_words_index_list[0])
        self.clean_word_entry_value()

    def random_review_words(self):
        self.review_words_id_list = []
        for key in self.review_words_list:
            self.review_words_id_list.append(key[0])


        #######debug###################
        word_list = []
        word_id = []
        for word in self.review_words_list:
            word_list.append(word[1])
            word_id.append(word[0])
        print ("word is %s, word_id is %s" % (word_list, word_id))
        #############################

        self.random_words_id_list = random.sample(self.review_words_id_list, len(self.review_words_list))  # generate random review words_id_list

        # get the index from random_words_id_list, because the random_words_id_list's element just is word's id,
        # but we need the id's index in words_id_list
        self.random_words_index_list = []
        for key in self.random_words_id_list:
            self.random_words_index_list.append(self.review_words_id_list.index(key))

        print ("random_words_index_list is %s, random_word_id_list is %s" % (self.random_words_index_list, self.random_words_id_list))
        self.backup_index_list = []



    def is_remember_word(self):
        self.remember_oblivious_operate("remember")

    def is_oblivious_word(self):
        self.remember_oblivious_operate("oblivious")

    def last_word(self):
        if len(self.backup_index_list) == 0:
            tkMessageBox.showerror("ERROR INFO", "This is the first word")
            return 0

        self.current_word_index = self.backup_index_list[-1]
        self.backup_index_list.pop()

        #self.current_word_id = self.words_id_list[self.current_word_index]
        self.show_word_entry_value(self.current_word_index)
        self.show_meanning_text_value(self.current_word_index)

    def remember_oblivious_operate(self, word_type):
        self.current_word_index = self.random_words_index_list[0]
        self.current_word_id = self.review_words_id_list[self.random_words_index_list[0]]

        print ("current_word_index is %d , current_word_id is %d" % (self.current_word_index, self.current_word_id))

        self.change_word_type_in_database(word_type)

        #############debug
        print ("word type is %s, word is %s, query is %s" % (word_type, self.review_words_list[self.current_word_index][1], self.query))
        self.change_random_and_backup_list()

        self.remaining_review_words_nums_check(self.random_words_index_list)
        if self.review_type == 1:
            self.eng_chi_review()
        elif self.review_type == 2:
            self.chi_eng_review()

    def change_random_and_backup_list(self):
        self.backup_index_list.append(self.random_words_index_list[0])
        self.random_words_index_list.pop(0)

    def change_word_type_in_database(self, change_type):
        if change_type == "remember":
            self.query = "update word_db set word_type = 1,review_count = review_count+1, review_time = (CURDATE() + 0) where id = " + str(self.current_word_id)
        elif change_type == "oblivious":
            self.query = "update word_db set word_type = 0 where id = " + str(self.current_word_id)
        self.cursor.execute(self.query)
        self.conn.commit()

    def show_meaning(self):
        self.current_word_index = self.random_words_index_list[0]
        self.show_meanning_text_value(self.current_word_index)

    def check_word_type(self):
        if self.is_remember == 0 and self.is_oblivious == 0:
            tkMessageBox.showerror("ERROR INFO", "You must choose remember or oblivious button")
            return 0
        else:
            self.cursor.execute(self.query)
            self.conn.commit()

    def remaining_review_words_nums_check(self, checked_list):
        if len(checked_list) == 0:
            self.show_meaning_bt.configure(state='disabled')
            self.verify_word_bt.configure(state='disabled')
            self.remember_bt.configure(state='disabled')
            self.oblivious_bt.configure(state='disabled')
            tkMessageBox.showerror("ERROR INFO", "No words need to review, you can try get review words by start button. "
                                                 "If hint the error again, maybe you should input new words into the database")
            raise Exception("ERROR INFO, No words need to review")

########################################################

    def show_word_entry_value(self, index):
        if self.review_type == 1:
            self.word_entry.configure(state='normal')
            self.word_var.set(self.review_words_list[index][1])
            self.word_entry.configure(state='disabled')

    def clean_word_entry_value(self):
        if self.review_type == 1:
            self.word_entry.configure(state='normal')
            self.word_var.set("")
            self.word_entry.configure(state='disabled')
        elif self.review_type == 2:
            self.word_var.set("")

    def clean_meanning_text_value(self):
        self.meaning_scrolledtext.configure(state='normal')
        self.meaning_scrolledtext.delete('1.0', END)
        self.meaning_scrolledtext.configure(state='disabled')

    def show_meanning_text_value(self, index):
        self.meaning_scrolledtext.configure(state='normal')
        self.meaning_scrolledtext.delete('1.0', END)
        self.meaning_scrolledtext.insert('1.0', self.review_words_list[index][2])
        self.meaning_scrolledtext.configure(state='disabled')

    def verify_word(self, event=None):
        input_word_value = self.word_entry.get()
        input_word_value = unicode(input_word_value)

        if cmp(input_word_value, str(self.review_words_list[self.random_words_index_list[0]][1])) != 0:
            tkMessageBox.showerror("Error info", "word spelled wrong, answer is %s, your answer is %s." %\
                                   (self.review_words_list[self.random_words_index_list[0]][1], input_word_value))
            self.is_oblivious_word()
        else:
            self.is_remember_word()

#=======================================
def display_widgets(parent):
    rev = ReviewFrame(parent)
