#coding:utf-8

from Tkinter import *
import ttk
#import search_func as swd
import search_func
import ScrolledText as tkst

class main_frame:
    def __init__(self, parent=None):
        self.root = parent
        self.root.title("Word_soft")
        self.root.resizable(0, 0)                       # Forbid resizing completely
        self.center_window(400, 500)            # make the form in the screen's center
        self.show()

    def show(self):
        self.label_frame = LabelFrame(self.root, bd=2, width=400, height=300)
        self.label_frame.grid(row=0)
        self.label_frame.grid_propagate(0)

        # add a search function
        # add a input entry
        text = StringVar()
        self.se_entry = Entry(self.label_frame, width=40, textvariable=text)
        self.se_entry.focus()
        text.set("a")
        self.se_entry.grid(row=0)

        # add a search button
        Button(self.label_frame,  text="serach", width=10, command=self.search).grid(row=0, column=1)


    def search(self):
        self.se_res = []
        search_func.get_html_content(self.se_entry.get(), self.se_res)
        self.display_res()
        
    def display_res(self):
        edit_space = tkst.ScrolledText(master = self.label_frame, bg='beige', width=50, height=5 )   
        for key in self.se_res:
            edit_space.insert('insert', key)
            edit_space.insert('insert', "\n")
        edit_space.grid(row=1, column=0, columnspan=2, sticky=W)

        
        

        
        
    def center_window(self, width, height):     
        screenwidth = self.root.winfo_screenwidth() 
        screenheight = self.root.winfo_screenheight() 
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2) 
        self.root.geometry(size)

if __name__ == "__main__":
    root = Tk()
    app = main_frame(root)

    root.mainloop()
