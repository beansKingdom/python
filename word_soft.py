# -*- coding: UTF-8 -*-

from Tkinter import *
import pymysql
import tkMessageBox
import time
import random
import re
import ttk
import os

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
        insert_bt.bind('<Return>', self.insert)
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
        rowline = 1
        
        # add mysql connect control
        for key in self.label_name:
            lbname = key + "Lable"
            lbname = Label(self.query_frame, text=key + " :", **self.lb_conf)
            lbname.grid(row=rowline, column=0, columnspan=1, **self.grid_conf)
            rowline += 1

        # add word entry
        self.word_entry_val = StringVar()
        self.word_entry = Entry(self.query_frame, textvariable=self.word_entry_val, font=15)
        self.word_entry.grid(row=1, rowspan=1, column=1, columnspan=1, **self.grid_conf)
        
        # add meaning text
        self.meaning_text = Text(self.query_frame, width=23, height=3, state='disabled')
        self.meaning_text.grid(row=2, column=1, **self.grid_conf)
        
        self.entry_dict = dict(zip(self.label_name, [self.word_entry, self.meaning_text]))
        
        # query button
        query_bt = Button(self.query_frame, text="query", command=self.query, **self.bt_conf)
        query_bt.bind('<Return>', self.query)
        query_bt.grid(row=rowline + 2, column=1, **self.grid_conf)

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
        self.meaning_text.delete('1.0', END)
        self.word_val = self.word_entry.get().strip()
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
        
        self.meaning_text['state'] = 'normal'
        self.meaning_text.delete('1.0', END)
        self.meaning_text.insert(INSERT, data[0])
        self.meaning_text['state'] = 'disabled'
               
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
        self.review_frame.grid(row=0, column=1, rowspan=2,sticky=E+N, ipadx=10, ipady=10)
        self.rowline = 0
        
        # the numbers of vocabulary you want to review , default 50
        self.review_nums = Label(self.review_frame, text="review_nums:", **self.lb_conf)
        self.review_nums.grid(row=self.rowline, **self.grid_conf)
        self.nums_entry_val = StringVar()
        self.nums_entry_val.set("50")
        self.nums_entry = Entry(self.review_frame, textvariable=self.nums_entry_val, font=15)
        self.nums_entry.grid(row=self.rowline, rowspan=1, column=1, columnspan=1, **self.grid_conf)
        
        # the review types : english - chinese or chinese - english or mix
        self.review_type = ttk.Combobox(self.review_frame, width=15, text = "", state='readonly')
        self.review_type['values'] = ("review_type", "english-chinese", "chinese-english", "mix")
        self.review_type.current(0) 
        self.review_type.grid(row=self.rowline, column=2, **self.grid_conf)
        
        # the review start button
        self.start_bt = Button(self.review_frame, text="start", command=self.start, **self.bt_conf)
        self.start_bt.grid(row=self.rowline, rowspan=1,column=3, **self.grid_conf)

    # display review control
    def start(self):
        # get the listbox index
        #self.review_type_val = self.review_type['values'].index(self.review_type.get())
        
        # get words from database  
        # self.nums_entry.get() : get the max nums of review words 
        self.cursor.execute("select id, word, meaning from (select * from word_db order by ins_time) \
                            as temp where word_type != 1 or (ins_time - CURDATE() + 0)>=3 limit " + self.nums_entry.get())
        self.word_res = list(self.cursor.fetchall())     # the result of slef.cursor.fetchall is tuple, now change it to list 
        self.length = len(self.word_res)
        
        # generate list by words' id
        self.id_list = []
        for key in self.word_res:
            self.id_list.append(key[0])
            
        # check how many nums of words need to review 
        if len(self.id_list) == 0:
            tkMessageBox.showinfo("ERROR INFO", "No words need to review")
            raise Exception("ERROR INFO : No words need to review")            
                
        self.rand_list = random.sample(self.id_list, self.length)      #generate random review id_list
        # get the index from rand_list, because the rand_list's element just is word's id, 
        # but we need the id's index in id_list(word_res) 
        self.index_list = []
        for key in self.rand_list:
            self.index_list.append(self.id_list.index(key))
        
        self.back_index_list = []
        self.obl_list = []        
        self.en_ch_review()
        
        # add review buttons
        self.last_bt = Button(self.review_frame, text="last", command=self.last, **self.bt_conf)
        self.last_bt.grid(row=self.rowline+4, column=1, **self.grid_conf)
    
        self.next_bt = Button(self.review_frame, text="next", command=self.next, state='disabled', **self.bt_conf)
        self.next_bt.grid(row=self.rowline+4, column=2, **self.grid_conf)
                 
        self.remember_bt = Button(self.review_frame, text="remember", command=self.remember, **self.bt_conf)
        self.remember_bt.grid(row=self.rowline+3, column=1, **self.grid_conf)
       
        self.oblivious_bt = Button(self.review_frame, text="oblivious", command=self.oblivious, **self.bt_conf)
        self.oblivious_bt.grid(row=self.rowline+3, column=2, **self.grid_conf)          
        pass
        
    def next(self):
        self.back_index_list.append(self.index_list[0])
        self.rand_list.pop(0)
        self.index_list.pop(0)
        
        print (" rand_list %s\n index_list %s\n obl_list %s\n" % (self.rand_list, self.index_list, self.obl_list))
        self.cursor.execute(self.sql_query)
        self.conn.commit()            
        # make sure all oblivious words reviewed
        if len(self.rand_list) == 0:
            if len(self.obl_list) == 0:
                tkMessageBox.showinfo("ERROR INFO", "No words need to review")
                raise Exception("ERROR INFO : No words need to review") 
            else:
                self.rand_list = random.sample(self.obl_list, len(self.obl_list))
                for key in self.rand_list:
                    self.index_list.append(self.obl_list.index(key))
                    
        self.en_word_entry_val.set(self.word_res[self.index_list[0]][1])
        self.en_meaning_text['state'] = 'normal'
        self.en_meaning_text.delete('1.0', END)
        self.en_meaning_text['state'] = 'disabled'
        self.next_bt['state'] = 'disabled'
               
    def en_ch_review(self):
        # add review word and meaning label
        self.en_re_word = Label(self.review_frame, text="word : ", **self.lb_conf)
        self.en_re_word.grid(row=self.rowline+1, **self.grid_conf)
        
        self.en_re_meaning = Label(self.review_frame, text="meaning : ", **self.lb_conf)
        self.en_re_meaning.grid(row=self.rowline+2, **self.grid_conf)
        
        # add word entry
        self.en_word_entry_val = StringVar()
        self.en_word_entry = Entry(self.review_frame, textvariable=self.en_word_entry_val, font=15, state='readonly')
        self.en_word_entry.grid(row=self.rowline+1, column=1, **self.grid_conf)                                 
        self.en_word_entry_val.set(self.word_res[self.index_list[0]][1])
        
        # add meaning text
        self.en_meaning_text = Text(self.review_frame, width=23, height=3, state='disabled')
        self.en_meaning_text.grid(row=self.rowline+2, column=1, **self.grid_conf)
                                      
    def ch_en_review(self):
        pass
 
    def last(self):
        pass
             
    def remember(self):
        # id : the id of query   
        self.id = self.rand_list[0]  
        print ("remember" +  str(self.id))
        self.sql_query = "update word_db set word_type = 1,review_count = review_count+1 where id = " + str(self.id)
        self.rem_obl_common()
 
    def oblivious(self):
        self.id = self.rand_list[0]   
        print ("oblivious" +  str(self.id))        
        self.sql_query = "update word_db set word_type = 0,review_count = review_count+1 where id = " + str(self.id)
        self.rem_obl_common()
        self.obl_list.append(self.id)
        
    def rem_obl_common(self):      
        self.en_meaning_text['state'] = 'normal'
        self.en_meaning_text.delete('1.0', END)
        self.en_meaning_text.insert(INSERT, self.word_res[self.id_list.index(self.id)][2])
        self.en_meaning_text['state'] = 'disabled'
        self.next_bt['state'] = 'normal'   
        
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
        self.text_value = ["10.186.24.45", "action", "action", 3306, "word_soft"]
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
        query_frame = open_query_frame(original=self.root, label_conf=self.lb_conf, conn=self.conn, button_conf=self.bt_conf, grid_conf=self.grid_conf)
        menu_bar = show_menubar(original=self.root, mysql_info = self.mysql_dict, conn=self.conn)

    def show(self):
        """"""
        self.root.update()
        self.root.deiconify()

class show_menubar():
    def __init__(self, conn, original=None, mysql_info=None):
        self.root = original
        self.mysql_dict = mysql_info
        self.conn = conn
        self.cursor = self.conn.cursor()
        
        # get the script's directory 
        self.script_dir = os.path.split(os.path.realpath(__file__))[0]
        self.directory = self.script_dir + "\data.txt"
        
        # create menu bar function
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # create a menu item which called operation, and add functions
        oper_menu = Menu(menubar)
        menubar.add_cascade(label="operation", menu=oper_menu)
        oper_menu.add_command(label="import words", command=self.import_data)
        oper_menu.add_command(label="export words", command=self.export_data)        
        oper_menu.add_command(label="exit", command=self.quit)
        
        # create a menu item which called help, and add functions
        help_menu = Menu(menubar)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="about")
        
    def quit(self):
        self.root.quit()
        self.root.destroy()
        exit()
        
    def import_data(self):
        print self.directory
        #os.system("mysql -u%s -p%s -h%s -P%s %s < %s" % (self.mysql_dict['username'], self.mysql_dict['password'], \
        #self.mysql_dict['mysql_ip'], self.mysql_dict['port'], self.mysql_dict['dbname'], self.directory))
        os.system("mysql -u%s -p%s -h127.0.0.1 -P%s %s < %s" % (self.mysql_dict['username'], self.mysql_dict['password'], \
        self.mysql_dict['port'], self.mysql_dict['dbname'], self.directory)) 
        
    def export_data(self):
        os.system("mysqldump -u%s -p%s -h%s -P%s %s word_db --lock-all-tables > %s" % \
        (self.mysql_dict['username'], self.mysql_dict['password'], self.mysql_dict['mysql_ip'], self.mysql_dict['port'],\
        self.mysql_dict['dbname'], self.directory))       
              
# def get_screen_size(window): 
    # return window.winfo_screenwidth(),window.winfo_screenheight() 

# def get_window_size(window): 
    # return window.winfo_reqwidth(),window.winfo_reqheight() 
      
if __name__ == "__main__":
    root = Tk()

    app = MyApp(parent=root)
    root.mainloop()
