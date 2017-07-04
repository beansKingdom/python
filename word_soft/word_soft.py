# -*- coding: UTF-8 -*-

from Tkinter import *
import ttk
import main_frame as main_fm
import wordlist_frame as wdlist_fm

class Mywordsoft:
    def __init__(self, parent=None):
        self.root = parent
        self.config = {
            'gui_width' : 440,
            'gui_height' : 430,
        }
        self.root.title(" word_soft ")
        self.root.resizable(0, 0)                                                               # disable resizing the gui
        self.center_window(self.config['gui_width'], self.config['gui_height'])                 # make the gui in the screen's center

        # create tab_page widgets
        tabControl = ttk.Notebook(self.root)
        self.main_frame_tab = ttk.Frame(tabControl)
        tabControl.add(self.main_frame_tab, text='main function')
        self.word_list_tab = ttk.Frame(tabControl)
        tabControl.add(self.word_list_tab, text='word list')
        tabControl.grid()

        main_fm.display_widgets(self.root, self.main_frame_tab, self.config)
        wdlist_fm.display_widgets(self.word_list_tab, self.config)

    def center_window(self, width, height):
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
        self.root.geometry(size)

#=========================================================
# begin the word_soft
root = Tk()
myapp = Mywordsoft(root)
root.mainloop()
