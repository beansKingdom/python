# -*- coding: UTF-8 -*-

from Tkinter import *
import pymysql
import tkMessageBox
import re
import toolstips as tltp
from mysql_func import ConnectMysql

class InsFrame:
    def __init__(self, parent):
        self.root = parent
        self.lb_conf = { 'width':12, "anchor": W, "font": 15, "justify": LEFT }

    def connect_mysql(self):
        myconn = ConnectMysql()
        myconn.connect_mysql()
        self.conn = myconn.conn
        self.cursor = self.conn.cursor()

    def close_mysql(self):
        self.cursor.close()
        self.conn.close()

    def show(self):
        # add label control
        Label(self.root, text="word : ", **self.lb_conf).grid(row=0)
        Label(self.root, text="meaning :", **self.lb_conf).grid(row=1)

        # add entry control
        self.meaning_var = StringVar()
        self.word_var = StringVar()
        self.wd_entry = Entry(self.root, textvariable=self.word_var, bd=1)
        self.wd_entry.bind('<FocusOut>', self.check_word_is_exsited)
        self.mean_entry = Entry(self.root, textvariable=self.meaning_var, bd=1)
        self.wd_entry.grid(row=0, column=1, sticky=W)
        self.mean_entry.bind('<Return>', self.insert)
        self.mean_entry.grid(row=1, column=1, sticky=W)

        # add button widget, and bind return key
        insert_bt = Button(self.root, text="insert", command=self.insert, width=12)
        insert_bt.bind('<Return>', self.insert)
        insert_bt.grid(row=0, column=3, rowspan=2, sticky=W)

        # Add a Tooltip to the ScrolledText widget
        tltp.createToolTip(insert_bt, 'Stored the word in database.')

    def check_entry_val(self, type):
        if type == "word":
            value = self.word_val

            # check the word entry input not contain digit and special symbol
            pat = re.compile('^[A-Za-z][A-Za-z\s]*$')
            if len(value) !=0 and len(pat.findall(value)) == 0:
                tkMessageBox.showerror("ERROR INFO", "Words can only contain letters or spaces")
                raise Exception("ERROR INFO, Words can only contain letters or spaces")
        else:
            value = self.mean_val

        # check the entry value is not null
        if len(value) == 0:
            tkMessageBox.showerror("ERROR INFO", "%s can't be null..." % type)
            raise Exception("ERROR INFO :%s can't be null..." % type)

        # check the entry value isn't too long
        if len(value) > 100:
            tkMessageBox.showerror("ERROR INFO", "Max length is 50,%s data is too long..." % type)
            raise Exception("ERROR INFO, Max length is 100,%s data is too long..." % type)

    def check_word_is_exsited(self, event=None):
        self.connect_mysql()
        word_value = self.wd_entry.get()
        self.cursor.execute("select count(0) from word_db where word = '%s'" % word_value)
        result = self.cursor.fetchone()
        self.close_mysql()
        if result[0] == 1:
            self.wd_entry['fg'] = 'red'
            return 1
        else:
            self.wd_entry['fg'] = 'black'
        return 0

    def insert(self, event=None):
        # get the entry input
        self.word_val = self.wd_entry.get().strip()
        self.mean_val = self.mean_entry.get().encode('utf-8')

        # check input is not null 、too big and word format
        self.check_entry_val("word")
        self.check_entry_val("meaning")

        if self.check_word_is_exsited() != 0:
            self.clean_insert_entry()
            tkMessageBox.showerror("Error", "This word is existed...")
            raise  Exception("Error, this word is existed...")
        else:
            self.connect_mysql()
            # get the insert query id
            self.query_id = self.generate_query_id() + 1
            sql_query = "insert into word_db (id, word, meaning, ins_time, review_time) values \
                    (%d, '%s', '%s', CURDATE() + 0, CURDATE() + 0)" % (self.query_id, self.word_val, self.mean_val)
            self.cursor.execute(sql_query)
            self.conn.commit()
            self.close_mysql()

        self.clean_insert_entry()

    def clean_insert_entry(self):
        self.word_var.set("")
        self.meaning_var.set("")
        self.wd_entry.focus()

    def generate_query_id(self):
        try:
            self.cursor.execute("select id from word_db order by id desc limit 1;")
        except pymysql.Error as err:
            tkMessageBox.showerror("ERROR INFO", "Mysql Error %d: %s" % (err.args[0], err.args[1]))
            raise Exception("ERROR INFO : Mysql Error %d: %s" % (err.args[0], err.args[1]))
        data = self.cursor.fetchone()

        return data[0]

#=======================================
def display_widgets(parent):
    ins = InsFrame(parent)
    ins.show()

