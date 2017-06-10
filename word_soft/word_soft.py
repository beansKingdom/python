# -*- coding: UTF-8 -*-

from Tkinter import *
import insert_widgets as ins
import query_widgets as qry
import review_widgets as rev
import menu_bar

class MainFrame:
    def __init__(self, parent=None):
        self.root = parent
        self.gui_width = 400
        self.gui_height = 403

        self.root.title(" word_soft ")
        self.root.resizable(0, 0)                                           # disable resizing the gui
        self.center_window(self.gui_width, self.gui_height)                 # make the gui in the screen's center
        self.root.iconbitmap(r'E:\software\python\DLLs\pyc.ico')            # Change the main windows icon

        # add a labelframe widget
        self.lb_frame = LabelFrame(self.root, bd=5, width=self.gui_width, height=self.gui_height)
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


    def center_window(self, width, height):
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
        self.root.geometry(size)

#==========================================================
# begin the word_soft
root = Tk()
myapp = MainFrame(root)
root.mainloop()
