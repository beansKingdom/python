# -*- coding: UTF-8 -*-

from Tkinter import *
import insert_widgets as ins
import query_widgets as qry
import review_widgets as rev
import menu_bar
import ttk
from mysql_func import ConnectMysql
import pymysql
import tkMessageBox

class Main_frame:
    def __init__(self, grandparent, parent, parent_config):
        self.super_root = grandparent
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
        self.lb_frame = LabelFrame(self.root, bd=0, width=self.config['gui_width'], height=self.config['gui_height'])
        self.lb_frame.grid()
        self.lb_frame.grid_propagate(0)

        menu_bar.display_menubar(self.super_root)

        # create a child label frame, and put the insert_widgets in the frame
        self.child_ins_frame =  LabelFrame(self.lb_frame, text="insert", bd=2, width=self.config['gui_width']-10, height=100)
        self.child_ins_frame.grid(row=0)
        self.child_ins_frame.grid_propagate(0)
        ins.display_widgets(self.child_ins_frame)
        for child in self.child_ins_frame.winfo_children():                 # Change the padding which widgets in the label frame
            child.grid_configure(padx=8, pady=5)

        # create a child label frame, and put the query_widgets in the frame
        self.child_qry_frame =  LabelFrame(self.lb_frame, bd=2, text="query", width=self.config['gui_width']-10, height=62)
        self.child_qry_frame.grid(row=1)
        self.child_qry_frame.grid_propagate(0)
        qry.display_widgets(self.child_qry_frame)
        for child in self.child_qry_frame.winfo_children():                 # Change the padding which widgets in the label frame
            child.grid_configure(padx=8, pady=5)

        # create a child label frame, and put the review_widgets in the frame
        self.child_rev_frame =  LabelFrame(self.lb_frame, bd=2, text="review", width=self.config['gui_width']-10, height=210)
        self.child_rev_frame.grid(row=2)
        self.child_rev_frame.grid_propagate(0)
        rev.display_widgets(self.child_rev_frame)
        for child in self.child_rev_frame.winfo_children():                 # Change the padding which widgets in the label frame
            child.grid_configure(padx=8, pady=5)

#=======================================
def display_widgets(grandparent, parent, parent_config):
    mainframe = Main_frame(grandparent, parent, parent_config)
    mainframe.show()