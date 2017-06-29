# -*- coding: UTF-8 -*-

from Tkinter import *
import pymysql
import os
import tkMessageBox
from mysql_func import ConnectMysql

class show_menubar():
    def __init__(self, original=None, mysql_info=None):
        self.root = original
        self.connect_mysql()

        # get the script's directory
        self.script_dir = os.path.split(os.path.realpath(__file__))[0]
        self.directory = self.script_dir + "\data.txt"

        # create menu bar function
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # create a menu item which called operation, and add functions
        oper_menu = Menu(menubar)
        menubar.add_cascade(label="operation", menu=oper_menu)
        oper_menu.add_command(label="import words", command=self.import_data_pre)
        oper_menu.add_command(label="export words", command=self.export_data)
        oper_menu.add_command(label="exit", command=self.quit)

        # create a menu item which called help, and add functions
        help_menu = Menu(menubar)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="about")
        
    def connect_mysql(self):
        myconn = ConnectMysql()
        myconn.connect_mysql()
        self.conn = myconn.conn
        self.cursor = self.conn.cursor()
        self.mysql_dict = myconn.mysql_dict
        
    def quit(self):
        self.root.quit()
        self.root.destroy()
        exit()

    def import_data_pre(self):
        self.cursor.execute("show tables")
        table_list = list(self.cursor.fetchall())
        if len(table_list) != 0:
            for tbname in table_list:
                if tbname[0] == unicode("word_db"):
                    self.show_import_warn_info()
                    break
        else:
            self.import_data()

        return 0
     
    def show_import_warn_info(self):
        self.message_win = Toplevel()
        self.import_value = 0
        warn_label = Label(self.message_win, text="table 'word_db' is existed, click confirm button cover the table's data or cancel to quit")
        confirm_bt = Button(self.message_win, text="confirm", command=self.confirm, width=10)
        cancel_bt = Button(self.message_win, text="cancel", command=self.cancel, width=10)
        warn_label.grid(row=0, padx=8, pady=5, columnspan=2)
        confirm_bt.grid(row=1, padx=8, pady=5 , sticky = W)
        cancel_bt.grid(row=1, column=1, padx=8, pady=5 , sticky = W)
        
    def import_data(self):
        try:
            os.system("mysql -u%s -p%s -h%s -P%s %s < %s" % (self.mysql_dict['my_user'], self.mysql_dict['my_passwd'], self.mysql_dict['my_host'], \
                   int(self.mysql_dict['my_port']),self.mysql_dict['my_dbname'], self.directory))
        except pymysql.Error as err:
            tkMessageBox.showerror("ERROR INFO", "Mysql Error %d: %s" % (err.args[0], err.args[1]))
            raise Exception("ERROR INFO : Mysql Error %d: %s" % (err.args[0], err.args[1]))
        finally:
            tkMessageBox.showinfo("Info", "Import data sucessed")

    def confirm(self):
        self.import_data()
        self.message_win.destroy()

    def cancel(self):
        self.message_win.destroy()

    def export_data(self):
        try:
            os.system("mysqldump -u%s -p%s -h%s -P%s %s word_db --lock-all-tables > %s" % \
                  (self.mysql_dict['my_user'], self.mysql_dict['my_passwd'], self.mysql_dict['my_host'], \
                   int(self.mysql_dict['my_port']),self.mysql_dict['my_dbname'], self.directory))
        except pymysql.Error as err:
            tkMessageBox.showerror("ERROR INFO", "Mysql Error %d: %s" % (err.args[0], err.args[1]))
            raise Exception("ERROR INFO : Mysql Error %d: %s" % (err.args[0], err.args[1]))
        finally:
            tkMessageBox.showinfo("Info", "Export data sucessed")
        return 0


#=======================================
def display_menubar(parent):
    menu = show_menubar(parent)