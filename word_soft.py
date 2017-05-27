# -*- coding: UTF-8 -*-

from Tkinter import *
import pymysql
import tkMessageBox
import time
import random
import re
import ttk

class open_insert_frame():
    def __init__(self, original, label_conf, conn, button_conf, grid_conf):
        self.root = original
        self.lb_conf = label_conf       
        self.bt_conf = button_conf
        self.grid_conf = grid_conf
        self.conn = conn         
        self.cursor = self.conn.cursor()

        # add labelframe contrl
        self.insert_frame = LabelFrame(original, text="insert",bd=1)
        self.insert_frame.grid(row=0, column=0, sticky=W + N, ipadx=10, ipady=10)

        # word label: show the numbers of word
        # word_nums = get_word_nums(db) get the numbers of word from database
        self.word_nums = self.get_word_nums()
        self.nums_var = StringVar()
        self.nums_label = Label(self.insert_frame, textvariable=self.nums_var, **self.lb_conf)
        self.nums_var.set("nums : " + str(self.word_nums))
        self.nums_label.grid(row=0, column=0, **self.grid_conf)

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

            lbname = Label(self.insert_frame, text=key + " :", **self.lb_conf)
            lbname.grid(row=rowline, column=0, columnspan=1, **self.grid_conf)

            entryvar = StringVar()
            entryname = Entry(self.insert_frame, textvariable=entryvar, font=15)
            entryname.grid(row=rowline, rowspan=1, column=1, columnspan=1, **self.grid_conf)
            self.entry_name.append(entryname)
            self.entry_var.append(entryvar)
            rowline += 1
            
        self.entry_dict = dict(zip(self.label_name, self.entry_name))
        
        # add insert button and query button
        insert_bt = Button(self.insert_frame, text="insert", command=self.insert, **self.bt_conf)
        insert_bt.grid(row=rowline + 1, column=1, **self.grid_conf)

    def check_entry_val(self, type):       
        value = self.entry_dict[type]
        # check the entry value is not null
        if len(value.get()) == 0:
            tkMessageBox.showinfo("ERROR INFO", "%s can't be null..." % type)
            raise Exception("ERROR INFO :%s can't be null..." % type)
            
        # check the entry value isn't too long
        if len(value.get()) > 50:
            tkMessageBox.showinfo("ERROR INFO", "Max length is 50,%s data is too long..." % type)
            raise Exception("ERROR INFO, Max length is 50,%s data is too long..." % type)            
                                 
        # check the word entry input not contain digit and special symbol
        if type == "word":
            pat = re.compile('^[A-Za-z][A-Za-z\s]*$')
            if len(pat.findall(value.get())) == 0:
                tkMessageBox.showinfo("ERROR INFO", "Words can only contain letters or spaces")
                raise Exception("ERROR INFO, Words can only contain letters or spaces") 
   
    def insert(self, event=None):
        # get the entry input
        self.word_val = self.entry_name[0].get().strip()
        self.mean_val = self.entry_name[1].get().encode('utf-8')
    
        # check input is not null
        self.check_entry_val("word")
        self.check_entry_val("meaning")
 
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
                
    def get_word_nums(self):
        self.cursor.execute("select count(0) from word_db")
        data = self.cursor.fetchone()
        return data[0]

class open_query_frame():
    def __init__(self, original, label_conf, conn, button_conf, grid_conf):
        self.root = original
        self.lb_conf = label_conf       
        self.bt_conf = button_conf      
        self.conn = conn         
        self.grid_conf = grid_conf
        self.cursor = self.conn.cursor()

        # add labelframe contrl
        self.query_frame = LabelFrame(original, text="query",bd=1)
        self.query_frame.grid(row=1, column=0, sticky=W + N, ipadx=10, ipady=10)

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

            lbname = Label(self.query_frame, text=key + " :", **self.lb_conf)
            lbname.grid(row=rowline, column=0, columnspan=1, **self.grid_conf)

            entryvar = StringVar()
            entryname = Entry(self.query_frame, textvariable=entryvar, font=15)
            entryname.grid(row=rowline, rowspan=1, column=1, columnspan=1, **self.grid_conf)
            self.entry_name.append(entryname)
            self.entry_var.append(entryvar)
            rowline += 1
        
        self.entry_name[1]['state'] = 'readonly'
        self.entry_dict = dict(zip(self.label_name, self.entry_name))
        
        # query button
        query_bt = Button(self.query_frame, text="query", command=self.query, **self.bt_conf)
        query_bt.bind('<Return>', self.query)
        query_bt.grid(row=rowline + 1, **self.grid_conf)

    def check_entry_val(self):       
        value = self.entry_dict['word']
        # check the word entry value is not null
        if len(value.get()) == 0:
            tkMessageBox.showinfo("ERROR INFO", "word can't be null..." )
            raise Exception("ERROR INFO :word can't be null...")
            
        # check the entry value isn't too long
        if len(value.get()) > 50:
            tkMessageBox.showinfo("ERROR INFO", "Max length is 50,word data too long...")
            raise Exception("ERROR INFO :Max length is 50, word data too long...")            
                                 
        # check the word entry input not contain digit and special symbol
        pat = re.compile('^[A-Za-z][A-Za-z\s]*$')
        if len(pat.findall(value.get())) == 0:
            tkMessageBox.showinfo("ERROR INFO", "Words can only contain letters or spaces")
            raise Exception("ERROR INFO, Words can only contain letters or spaces") 
   
    def query(self, event=None):
        self.word_val = self.entry_name[0].get().strip()
        self.check_entry_val()
        
        # check the word is existed....
        check_query = "select count(0) from  word_db where word = '%s'" % self.word_val
        self.cursor.execute(check_query)
        self.conn.commit()
        data = self.cursor.fetchone()  
        if data[0] == 0:
            tkMessageBox.showinfo("ERROR INFO", "This word not found...")
            raise Exception("ERROR INFO, This word not found...")  
            
        sql_query = "select meaning from  word_db where word = '%s'" % self.word_val
        self.cursor.execute(sql_query)
        self.conn.commit()
        data = self.cursor.fetchone()
        
        self.entry_var[1].set(data[0])
               
class open_review_frame():
    def __init__(self, original, label_conf, conn, button_conf, grid_conf):
        """Constructor"""
        self.root = original
        self.lb_conf = label_conf       
        self.bt_conf = button_conf      
        self.conn = conn         
        self.grid_conf = grid_conf
        self.cursor = self.conn.cursor()
                
        self.review_frame = LabelFrame(original, text="review", bd=1, height=400, width=500)
        self.review_frame.grid(row=0, column=1, sticky=W + N, ipadx=10, ipady=10)
        self.rowline = 0
        
        # the numbers of vocabulary you want to review , default 50
        self.review_nums = Label(self.review_frame, text="review_nums:", **self.lb_conf)
        self.review_nums.grid(row=self.rowline, **self.grid_conf)
        self.nums_entry_val = StringVar()
        self.nums_entry_val.set("50")
        self.nums_entry = Entry(self.review_frame, textvariable=self.nums_entry_val, font=15)
        self.nums_entry.grid(row=self.rowline, rowspan=1, column=1, columnspan=1, **self.grid_conf)
        
        # the review types : english - chinese or chinese - english or mix
        #self.review_type_val = StringVar()  
        self.review_type = ttk.Combobox(self.review_frame, width=15, text = "", state='readonly')
        #self.review_type = ttk.Combobox(self.review_frame, width=12, textvariable=self.review_type_val, state='readonly')
        self.review_type['values'] = ("review_type", "english-chinese", "chinese-english", "mix")
        self.review_type.current(0) 
        self.review_type.grid(row=self.rowline, column=2, **self.grid_conf)
        
        # the review start button
        self.start_bt = Button(self.review_frame, text="start", command=self.start, **self.bt_conf)
        self.start_bt.grid(row=self.rowline, rowspan=1,column=3, **self.grid_conf)

    # display review control
    def start(self):
        pass
 
class MyApp():
    def __init__(self, parent=None):
        self.root = parent
        self.root.title("Word_soft")
        self.root.resizable(0, 0)       # Forbid resizing completely
        self.center_window(900, 400)
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
            "padx"   : 5,
            "pady"   : 5
        }
        
        # self.grid_conf: the control grid common config 
        self.grid_conf = {
            "padx":5, 
            "pady":5 ,
            "sticky":W+N
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
            lbname.grid(row=rowline, column=0, columnspan=1, **self.grid_conf)

            entry_var = StringVar()
            entryname = Entry(self.frame, textvariable=entry_var, font=15)
            entry_var.set(self.text_value[rowline])
            entryname.grid(row=rowline, rowspan=1, column=1, columnspan=1, **self.grid_conf)
            self.entry_name.append(entryname)
            rowline += 1

        connect_bt = Button(self.frame, text="connect", command=self.connect, **self.bt_conf)
        connect_bt.bind('<Return>', self.connect)       # bind connect button on return key
        connect_bt.grid(row=rowline + 1, column=1, **self.grid_conf)
    
    def center_window(self, width, height):     
        screenwidth = self.root.winfo_screenwidth() 
        screenheight = self.root.winfo_screenheight() 
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2) 
        self.root.geometry(size) 
        
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

        # add new frame,is used insert and review
        insert_frame = open_insert_frame(original=self.root, label_conf=self.lb_conf, conn=self.conn, button_conf=self.bt_conf, grid_conf=self.grid_conf)
        review_frame = open_review_frame(original=self.root, label_conf=self.lb_conf, conn=self.conn, button_conf=self.bt_conf, grid_conf=self.grid_conf)
        #query_frame = open_query_frame(original=self.root, label_conf=self.lb_conf, conn=self.conn, button_conf=self.bt_conf, grid_conf=self.grid_conf)

    def show(self):
        """"""
        self.root.update()
        self.root.deiconify()

# def get_screen_size(window): 
    # return window.winfo_screenwidth(),window.winfo_screenheight() 

# def get_window_size(window): 
    # return window.winfo_reqwidth(),window.winfo_reqheight() 
      
if __name__ == "__main__":
    root = Tk()


    app = MyApp(parent=root)
    root.mainloop()
