# -*- coding: UTF-8 -*-

from Tkinter import *
import pymysql
import tkMessageBox
import time
import random
import re

class open_commit_frame():
    def __init__(self, original, label_conf, conn, button_conf):
        """Constructor"""
        self.root = original
        self.lb_conf = label_conf       
        self.bt_conf = button_conf      
        self.conn = conn         
        self.cursor = self.conn.cursor()

        # add labelframe contrl
        self.commit_frame = LabelFrame(original, text="insert and query",bd=1, height=400, width=500)
        self.commit_frame.grid(row=0, column=0, sticky=W + N, ipadx=10, ipady=10)

        # word label: show the numbers of word
        # word_nums = get_word_nums(db) get the numbers of word from database
        self.word_nums = self.get_word_nums()
        self.nums_var = StringVar()
        self.nums_label = Label(self.commit_frame, textvariable=self.nums_var, **self.lb_conf)
        self.nums_var.set("nums : " + str(self.word_nums))
        self.nums_label.grid(row=0, column=0, sticky=E)

        # label and entry control
        self.label_name = ["word", "meaning"]
        self.entry_name = []
        self.entry_var = []
        rowline = 1
        
        # add mysql connect control
        for key in self.label_name:
            lbname = key + "Lable"
            entryname = key + "Entry"
            entryvar = key + "Var"

            lbname = Label(self.commit_frame, text=key + " :", **self.lb_conf)
            lbname.grid(row=rowline, column=0, columnspan=1, sticky=E)

            entryvar = StringVar()
            entryname = Entry(self.commit_frame, textvariable=entryvar, font=15)
            entryname.grid(row=rowline, rowspan=1, column=1, columnspan=1, sticky=W, padx=5, pady=2)
            self.entry_name.append(entryname)
            self.entry_var.append(entryvar)
            rowline += 1
            
        # add commit button and query button
        commit_bt = Button(self.commit_frame, text="commit", command=self.commit, **self.bt_conf)
        commit_bt.bind('<Return>', self.commit)
        commit_bt.grid(row=rowline + 1, column=0, pady=5)
        query_bt = Button(self.commit_frame, text="query", command=self.query, **self.bt_conf)
        query_bt.bind('<Return>', self.query)
        query_bt.grid(row=rowline + 1, column=1, pady=5)

    def check_entry_val(self, entry_list):
        for key in entry_list:
            # check the entry value is not null
            if len(key) == 0:
                tkMessageBox.showinfo("ERROR INFO", "word or meaning can't be null...")
                raise Exception("ERROR INFO : word or meaning can't be null...")
                
        # check the word entry input not contain digit and special symbol
        pat = re.compile('^[A-Za-z][A-Za-z\s]*$')
        if len(pat.findall(entry_list[0])) == 0:
            tkMessageBox.showinfo("ERROR INFO", "Words can only contain letters or spaces")
            raise Exception("ERROR INFO, Words can only contain letters or spaces")        
            
                
    def commit(self, event=None):
        # get the entry input
        self.word_val = self.entry_name[0].get().strip()
        self.mean_val = self.entry_name[1].get().encode('utf-8')
    
        # check input is not null
        self.check_entry_val([self.word_val, self.mean_val])
 
        # check the word is existed??
        check_query = "select count(0) from word_db where word = '%s'" % self.word_val
        self.cursor.execute(check_query)
        data = self.cursor.fetchone()
        if data[0] != 0:
            tkMessageBox.showinfo("ERROR INFO", "This word is existed...")
            raise Exception("ERROR INFO, This word is existed...")

        sql_query = "insert into word_db (id, word, meaning, ins_time) values \
                    (%d, '%s', '%s', CURDATE() + 0)" % (self.word_nums+1, self.word_val, self.mean_val)
        self.cursor.execute(sql_query)
        self.conn.commit()

        # get total words num
        self.word_nums += 1
        self.nums_var.set("nums : " + str(self.word_nums))

        # clean the entry data
        for key in self.entry_var:
            key.set("")

        self.entry_name[0].focus()    
        
        
    def query(self, event=None):
        pass
        
    def get_word_nums(self):
        self.cursor.execute("select count(0) from word_db")
        data = self.cursor.fetchone()
        return data[0]
        
class open_review_frame():
    def __init__(self, original, label_conf):
        """Constructor"""
        self.root = original
        self.review_frame = LabelFrame(original, text="review", bd=1, height=400, width=500)
        self.review_frame.grid(row=0, column=1, sticky=E)

class MyApp():
    def __init__(self, parent=None):
        self.root = parent
        self.root.resizable(0, 0)       # Forbid resizing completely
        self.frame = LabelFrame(parent, text="main_frame", bd=1, height=400, width=500)
        self.frame.grid(row=0, column=0, sticky=E, ipadx=10, ipady=2, padx=10, pady=5)

        # self.lb_conf: the label common config
        self.lb_conf = {
            "width": 10,
            "anchor": W,
            "font": 15,
            "justify": LEFT,
            "padx": 10,
            "pady": 2
        }
        
        # self.bt_conf: the bt common config
        self.bt_conf = {
            "width"  : 10, 
            "height" : 1, 
            "padx"   : 5,
            "pady"   : 5
        }

        self.label_name = ["mysql_ip", "username", "password", "port", "dbname"]
        self.text_value = ["127.0.0.1", "action", "action", 3306, "word_soft"]
        self.entry_name = []
        rowline = 0

        # add mysql connect control
        for key in self.label_name:
            lbname = key + "Lable"
            entryname = key + "Entry"
            entry_var = key + "Var"

            lbname = Label(self.frame, text=key + " :", **self.lb_conf)
            lbname.grid(row=rowline, column=0, columnspan=1, sticky=E)

            entry_var = StringVar()
            entryname = Entry(self.frame, textvariable=entry_var, font=15)
            entry_var.set(self.text_value[rowline])
            entryname.grid(row=rowline, rowspan=1, column=1, columnspan=1, sticky=W, padx=5, pady=2)
            self.entry_name.append(entryname)
            rowline += 1

        connect_bt = Button(self.frame, text="connect", command=self.connect, **self.bt_conf)
        connect_bt.bind('<Return>', self.connect)       # bind connect button on return key
        connect_bt.grid(row=rowline + 1, column=0, pady=5, sticky=W)
            
    def connect(self, event=None):
        # get mysql config and try to connect
        self.mysql_dict_value = []
        for key in self.entry_name:
            self.mysql_dict_value.append(key.get())

        # conbine mysql_key and mysql_key_value
        self.mysql_dict = dict(zip(self.label_name, self.mysql_dict_value))
        
        for (k,v) in  self.mysql_dict.items():
            if len(v) == 0:
                tkMessageBox.showinfo("ERROR INFO", "%s value can't be null.." % k)
                raise Exception("ERROR INFO :%s value can't be null.." % k)

        try:
            # self.conn   : the connect of mysql
            self.conn = pymysql.connect(self.mysql_dict['mysql_ip'], self.mysql_dict['username'], self.mysql_dict['password'], self.mysql_dict['dbname'],
                                      int(self.mysql_dict['port']), charset='utf8')
        except pymysql.Error as err:
            tkMessageBox.showinfo("ERROR INFO", "Mysql Error %d: %s" % (err.args[0], err.args[1]))
            raise Exception("ERROR INFO : Mysql Error %d: %s" % (err.args[0], err.args[1]))

        # hide the connect frame
        self.frame.grid_remove()

        # add new frame,is used commit and review
        commit_frame = open_commit_frame(original=self.root, label_conf=self.lb_conf, conn=self.conn, button_conf=self.bt_conf)
        review_frame = open_review_frame(original=self.root, label_conf=self.lb_conf)

    def show(self):
        """"""
        self.root.update()
        self.root.deiconify()

if __name__ == "__main__":
    root = Tk()
    root.update_idletasks()

    app = MyApp(parent=root)
    root.mainloop()
