# -*- coding: UTF-8 -*-

from Tkinter import *
import insert_widgets as ins
import query_widgets as qry
import review_widgets as rev
import menu_bar
import ttk
import get_conf as gcf
import pymysql
import tkMessageBox

class MainFrame:
    def __init__(self, parent=None):
        self.root = parent
        self.gui_width = 400
        self.gui_height = 430

        self.root.title(" word_soft ")
        self.root.resizable(0, 0)                                           # disable resizing the gui
        self.center_window(self.gui_width, self.gui_height)                 # make the gui in the screen's center
        self.root.iconbitmap(r'E:\software\python\DLLs\pyc.ico')            # Change the main windows icon

        tabControl = ttk.Notebook(self.root)
        self.main_function_tab = ttk.Frame(tabControl)
        tabControl.add(self.main_function_tab, text='main function')
        self.word_list_tab = ttk.Frame(tabControl)
        tabControl.add(self.word_list_tab, text='word list')
        tabControl.grid()

        self.main_function_tab_show()
        self.word_list_tab_show()

    def main_function_tab_show(self):
        # add a labelframe widget
        self.lb_frame = LabelFrame(self.main_function_tab, bd=0, width=self.gui_width, height=self.gui_height)
        self.lb_frame.grid()
        self.lb_frame.grid_propagate(0)                                     # Prevent the frame size from changing with the control

        # create a child label frame, and put the insert_widgets in the frame
        self.child_ins_frame =  LabelFrame(self.lb_frame, text="insert", bd=2, width=390, height=100)
        self.child_ins_frame.grid(row=0)
        self.child_ins_frame.grid_propagate(0)
        ins.display_widgets(self.child_ins_frame)
        for child in self.child_ins_frame.winfo_children():                 # Change the padding which widgets in the label frame
            child.grid_configure(padx=8, pady=5)


        # create a child label frame, and put the query_widgets in the frame
        self.child_qry_frame =  LabelFrame(self.lb_frame, bd=2, text="query", width=390, height=62)
        self.child_qry_frame.grid(row=1)
        self.child_qry_frame.grid_propagate(0)
        qry.display_widgets(self.child_qry_frame)
        for child in self.child_qry_frame.winfo_children():                 # Change the padding which widgets in the label frame
            child.grid_configure(padx=8, pady=5)

        # create a child label frame, and put the review_widgets in the frame
        self.child_rev_frame =  LabelFrame(self.lb_frame, bd=2, text="review", width=390, height=210)
        self.child_rev_frame.grid(row=2)
        self.child_rev_frame.grid_propagate(0)
        rev.display_widgets(self.child_rev_frame)
        for child in self.child_rev_frame.winfo_children():                 # Change the padding which widgets in the label frame
            child.grid_configure(padx=8, pady=5)

        menu_bar.display_menubar(self.root)

    def word_list_tab_show(self):
        # add a labelframe widget
        self.word_list_frame = LabelFrame(self.word_list_tab,bd=0,  width=self.gui_width, height=self.gui_height)
        self.word_list_frame.pack()
        self.word_list_frame.pack_propagate(0)

        self.mysql_dict = {}
        self.get_mysql_conf()
        self.connect_mysql()
        self.get_data_from_database()
        self.show_button_frame()
        self.show_display_data_frame()

    def show_display_data_frame(self):
        self.display_data_frame = LabelFrame(self.word_list_frame,bd=0, width=self.gui_width, height=self.gui_height-100)
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

        self.word_treeview.column('c0', width=20, anchor='center')
        self.word_treeview.column('c1', width=100, anchor='center')
        self.word_treeview.column('c2', width=260, anchor='center')
        self.word_treeview.pack(side=LEFT, fill=Y)
        self.word_treeview.bind('<ButtonRelease-1>',  self.get_word_info_in_treeview)
        self.each_page_show_words_num = 0
        self.current_page = 1

        scrollBar.config(command=self.word_treeview.yview)
        self.word_treeview_show_data()

    def show_button_frame(self):
        self.button_frame = LabelFrame(self.word_list_frame, bd=1, width=self.gui_width, height=30)
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

    def center_window(self, width, height):
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
        self.root.geometry(size)

    def connect_mysql(self):
        try:
            # self.conn   : the connect of mysql
            self.conn = pymysql.connect(self.mysql_dict['my_host'], self.mysql_dict['my_user'], self.mysql_dict['my_passwd'],
                                        self.mysql_dict['my_dbname'],int(self.mysql_dict['my_port']), charset='utf8')
        except pymysql.Error as err:
            tkMessageBox.showerror("ERROR INFO", "Mysql Error %d: %s" % (err.args[0], err.args[1]))
            raise Exception("ERROR INFO : Mysql Error %d: %s" % (err.args[0], err.args[1]))
        self.cursor = self.conn.cursor()

    def get_mysql_conf(self):
        gcf.get_config(self.mysql_dict)

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

#=========================================================
# begin the word_soft
root = Tk()
myapp = MainFrame(root)
root.mainloop()
