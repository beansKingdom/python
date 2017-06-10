# -*- coding: UTF-8 -*-

from Tkinter import *
import get_conf as gcf
import pymysql
import os
import tkMessageBox

class show_menubar():
    def __init__(self, original=None, mysql_info=None):
        self.root = original
        self.mysql_dict = {}
        self.get_mysql_conf()
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
        oper_menu.add_command(label="import words", command=self.import_data)
        oper_menu.add_command(label="export words", command=self.export_data)
        oper_menu.add_command(label="exit", command=self.quit)

        # create a menu item which called help, and add functions
        help_menu = Menu(menubar)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="about")

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

    def quit(self):
        self.root.quit()
        self.root.destroy()
        exit()

    def import_data(self):
        self.cursor.execute("show tables")
        table_list = list(self.cursor.fetchall())
        for key in table_list:
            if key[0] == unicode("word_db"):
                tkMessageBox.showwarning("ERROR INFO", "The word_db table is exiest, can't import...")
                raise Exception("ERROR INFO : The word_db table is exiest, can't import...")

        try:
            os.system("mysql -u%s -p%s -h%s -P%s %s < %s" % (self.mysql_dict['my_user'], self.mysql_dict['my_passwd'], self.mysql_dict['my_host'], \
                   int(self.mysql_dict['my_port']),self.mysql_dict['my_dbname'], self.directory))
        except pymysql.Error as err:
            tkMessageBox.showerror("ERROR INFO", "Mysql Error %d: %s" % (err.args[0], err.args[1]))
            raise Exception("ERROR INFO : Mysql Error %d: %s" % (err.args[0], err.args[1]))
        finally:
            tkMessageBox.showinfo("Info", "Import data sucessed")

        return 0

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