# encoding : utf-8

import toolstips as tltp

try :   #for python2
    from  Tkinter  import *
    import ttk
    import ScrolledText as sltt
    import tkMessageBox
except ImportError:    # for python3
    from tkinter import *
    import tkinter.scrolledtext as tkst

class MyApp:
    def __init__(self, parent = None):
        self.gui_width = 800
        self.gui_height = 500
        self.root = parent
        self.root.title(" gui_test ")
        self.root.resizable(0, 0)                                           # disable resizing the gui
        self.center_window(self.gui_width, self.gui_height)                 # make the gui in the screen's center
        self.root.iconbitmap(r'E:\software\python\DLLs\pyc.ico')            # Change the main windows icon

        # add a labelframe widget
        self.lb_frame = LabelFrame(self.root, text="label_frame", bd=2, width=self.gui_width, height=self.gui_height)
        self.lb_frame.grid()
        self.lb_frame.grid_propagate(0)

        self.display_widgets()

    def display_widgets(self):
        # add a label widget
        lb_str = StringVar()
        self.lb_name = Label(self.lb_frame, textvariable=lb_str, fg='white', bg='black')
        lb_str.set("hello world, helingyun")
        self.lb_name.grid(row=0)
        Label(self.lb_frame, text="select a number", fg='white', bg='black').grid(row=0, column=1)

        # add a button widget
        self.bt_name = Button(self.lb_frame, text="click me", command=self.click_me, width=14)
        self.bt_name.grid(row=1, column=2)

        # add a entry widget
        entry_str = StringVar()
        self.en_name = Entry(self.lb_frame, textvariable=entry_str, width=14)
        self.en_name.grid(row=1)
        self.en_name.focus()
        lb_str.set("Entry your name")

        # add a combobox widget
        self.combo_str = StringVar()
        self.cb_name = ttk.Combobox(self.lb_frame, textvariable=self.combo_str, width=12)
        self.cb_name['values'] = (1, 2, 3, 4)
        self.cb_name.current(0)
        self.cb_name.grid(row=1, column=1)

        # Creating a checkbuttons
        chVarDis = IntVar()
        self.check_one = Checkbutton(self.lb_frame, text="Disabled", variable=chVarDis, state='disabled')
        self.check_one.select()
        self.check_one.grid(column=0, row=4, sticky=W)

        # add a scrolledtext widget
        self.sctext_name = sltt.ScrolledText(self.lb_frame, wrap='word', width=36, height=2)
        self.sctext_name.grid(row=5, column=0, columnspan=3, sticky=W)

        # Add a Tooltip to the ScrolledText widget
        tltp.createToolTip(self.sctext_name, 'This is a ScrolledText widget.')

        # add a label_frame within the label_frame
        # then add three labels in the label_frame
        child_frame = LabelFrame(self.lb_frame, bd=2, width=300, height=200)
        child_frame.grid(row=6, columnspan=3, sticky=W)

        Label(child_frame, text="Label 1").grid(row=0)
        Label(child_frame, text="Label 2").grid(row=0, column=1)
        Label(child_frame, text="Label 3").grid(row=0, column=2)

        for child in self.lb_frame.winfo_children():
            child.grid_configure(padx=8, pady=4)

        # add a menu bar
        menuBar = Menu(self.root)  # create a menubar instance
        self.root.config(menu=menuBar)

        # add menubar's child menu
        fileMenu = Menu(menuBar,  tearoff=0)  # 2
        menuBar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="New")
        fileMenu.add_separator()  # 4
        fileMenu.add_command(label="Exit", command=self.quit)

        helpMenu = Menu(menuBar, tearoff=0)  # 6
        helpMenu.add_command(label="About", command=self.help_about)
        menuBar.add_cascade(label="Help", menu=helpMenu)

    def quit(self):
        self.root.quit()
        self.root.destroy()
        exit()

    def help_about(self):
        tkMessageBox.showinfo("HELP INFO", "The software is used to remember words")

    def click_me(self):
        self.bt_name.configure(text="hello ~ %s %s!!" % (self.en_name.get(), self.cb_name.get()), state='disabled')
        self.check2.select()



    def center_window(self, width, height):
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
        self.root.geometry(size)

root = Tk()
myapp = MyApp(root)
root.mainloop()


