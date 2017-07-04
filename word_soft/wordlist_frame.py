# -*- coding: UTF-8 -*-

from Tkinter import *
import menu_bar
import ttk
from mysql_func import ConnectMysql
import pymysql
import tkMessageBox

class Wordlist_frame:
    def __init__(self, parent, parent_config):
        self.root = parent
        self.config = parent_config
        self.connect_mysql()

    def connect_mysql(self):
        myconn = ConnectMysql()
        myconn.connect_mysql()
        self.conn = myconn.conn
        self.cursor = self.conn.cursor()


    def show(self):
        # add a labelframe widget
        self.word_list_frame = LabelFrame(self.root,bd=0,  width=self.config['gui_width'], height=self.config['gui_height'])
        self.word_list_frame.pack()
        self.word_list_frame.pack_propagate(0)

        self.show_button_frame()
        self.show_display_data_frame()
        self.check_table_status()

    def show_display_data_frame(self):
        self.display_data_frame = LabelFrame(self.word_list_frame,bd=0, width=self.config['gui_width'], height=self.config['gui_height']-100)
        self.display_data_frame.pack()
        self.display_data_frame.pack_propagate(0)

        scrollBar = Scrollbar(self.display_data_frame)
        scrollBar.pack(side=RIGHT, fill=Y)
        tree_view_columnname = ('c0', 'c1', 'c2')
        tree_view_columntext = (' ', 'word', 'meaning')

        self.word_treeview = ttk.Treeview(self.display_data_frame, columns=tree_view_columnname, \
                                          show="headings", yscrollcommand=scrollBar.set)

        for (column_name, column_text) in zip(tree_view_columnname, tree_view_columntext):
            self.word_treeview.heading(column_name, text=column_text)

        self.word_treeview.column('c0', width=int(self.config['gui_width']*0.075), anchor='center')
        self.word_treeview.column('c1', width=int(self.config['gui_width']*0.25), anchor='center')
        self.word_treeview.column('c2', width=int(self.config['gui_width']*0.65), anchor='center')
        self.word_treeview.pack(side=LEFT, fill=Y)
        self.word_treeview.bind('<ButtonRelease-1>',  self.get_word_info_in_treeview)
        self.each_page_show_words_num = 0
        self.current_page = 1

        scrollBar.config(command=self.word_treeview.yview)

    def show_button_frame(self):
        self.button_frame = LabelFrame(self.word_list_frame, bd=1, width=self.config['gui_width'], height=30)
        self.button_frame.pack()
        self.button_frame.pack_propagate(0)

        self.page_nums = StringVar()
        self.down_page_bt = Button(self.button_frame, text="down", command=self.down_page, width=4)
        self.up_page_bt = Button(self.button_frame, text="up", command=self.up_page, width=4)
        self.word_entry = Entry(self.button_frame, textvariable=self.page_nums, width=16)
        self.search_word_bt = Button(self.button_frame, text="search", command=self.search_word)
        self.delete_word_bt = Button(self.button_frame, text="delete", command=self.delete_word)
        self.refresh_word_bt = Button(self.button_frame, text="refresh", command=self.refresh_word)
        self.word_entry.bind('<Return>', self.search_word)
        self.search_word_bt.bind('<Return>', self.search_word)

        self.down_page_bt.pack(padx=3, pady=1, side=RIGHT)
        self.up_page_bt.pack(padx=3, pady=1, side=RIGHT)
        self.word_entry.pack(padx=3, pady=1, side=LEFT)
        self.search_word_bt.pack(padx=3, pady=1, side=LEFT)
        self.delete_word_bt.pack(padx=3, pady=1, side=LEFT)
        self.refresh_word_bt.pack(padx=3, pady=1, side=LEFT)

    def check_table_status(self):
        self.cursor.execute("show tables")
        data = self.cursor.fetchall()
        for tbname in data:
            if tbname[0] == unicode("word_db"):
                self.get_data_from_database()
                self.word_treeview_show_data()
                return 0

        tkMessageBox.showerror("Error", "Error Not found table 'word_db', you can import data or create table 'word_db' in database")

    def word_treeview_show_data(self):
        self.delete_treeview_data()
        if self.totall_words_nums < (self.current_page * 30 ):
            page_max_words_num = self.totall_words_nums
        else:
            page_max_words_num = self.current_page * 30

        while (self.each_page_show_words_num < page_max_words_num ):
            id = self.each_page_show_words_num
            self.word_treeview.insert('', 'end', text="", values=(id+1 , self.word_list[id][1], self.word_list[id][2]))
            self.each_page_show_words_num += 1

    def get_data_from_database(self):
        self.cursor.execute("select id,word,meaning from word_db order by id desc")
        self.conn.commit()
        self.word_list = list(self.cursor.fetchall())
        self.totall_words_nums = len(self.word_list)

    def delete_treeview_data(self):
        for word in self.word_treeview.get_children():
            self.word_treeview.delete(word)

    def down_page(self):
        if self.totall_words_nums < (self.current_page * 30 ):
            tkMessageBox.showerror("ERROR INFO", "This is the last page.")
            return 0

        self.current_page += 1
        self.word_treeview_show_data()

    def up_page(self):
        if self.each_page_show_words_num < 30 or self.current_page == 1:
            tkMessageBox.showerror("ERROR INFO", "This is the first page.")
            return 0

        self.each_page_show_words_num = (30 * (self.current_page-2))
        self.current_page -= 1
        self.word_treeview_show_data()

    def search_word(self, event=None):
        for word in self.word_list:
            if word[1] == unicode(self.word_entry.get()):
                self.word_index = self.word_list.index(word)
                self.delete_treeview_data()
                self.word_treeview.insert('', 'end', text="",values=(self.word_index+1, self.word_list[self.word_index][1], \
                                                                     self.word_list[self.word_index][2]))
                return 0

        tkMessageBox.showerror("ERROR INFO", " Not find the word in word_list")
        raise Exception("ERROR INFO : Not find the word in word_list")

    def get_word_info_in_treeview(self, event=None):
        curitem = self.word_treeview.focus()
        self.word_info = self.word_treeview.item(curitem)['values']

    def update_word(self):
        pass

    def delete_word(self):
        self.get_word_info_in_treeview()
        if self.word_info == "":
            tkMessageBox.showerror("ERROR INFO", "Haven't choose one word")
            raise Exception("ERROR INFO , Haven't choose one word")

        delete_word = self.word_treeview.selection()[0]
        self.word_treeview.delete(delete_word)
        try:
            self.cursor.execute("delete from word_db where word = '%s'" % self.word_info[1])
            self.conn.commit()
        except pymysql.Error as err:
            tkMessageBox.showerror("ERROR INFO", "Mysql Error %d: %s" % (err.args[0], err.args[1]))
            raise Exception("ERROR INFO : Mysql Error %d: %s" % (err.args[0], err.args[1]))
        finally:
            tkMessageBox.showinfo("Info", "deleted word success")
        self.refresh_word()

    def refresh_word(self):
        self.get_data_from_database()
        self.each_page_show_words_num = 0
        self.current_page = 1
        self.word_treeview_show_data()

#=======================================
def display_widgets(parent, parent_config):
    mainframe = Wordlist_frame(parent, parent_config)
    mainframe.show()