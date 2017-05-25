# -*- coding: UTF-8 -*-
# design use random.sample to generate more words

from Tkinter import *
import pymysql
import tkMessageBox
import time
import random

def mainFrame():
    #main frame init
    root.title("Word_soft")
    root.geometry('500x300')
    
    labelName = ["mysql_ip", "username", "password", "port", "dbname"]
    textValue = ["10.186.24.45", "action", "action", 3306, "word_soft"]
    entryName = []
    rowline = 0
    
    # add mysql connect control
    for key in labelName:
        lbname = key + "Lable"
        entryname = key + "Entry"
        entry_var = key + "Var"

        lbname = Label(root, text=key + " :", width=10, anchor=W, justify=LEFT)
        lbname.grid(row=rowline, padx=5, pady=2)

        entry_var = StringVar()
        entryname = Entry(root, textvariable=entry_var)
        entry_var.set(textValue[rowline])
        entryname.grid(row=rowline, column=1)
        entryName.append(entryname)
        rowline += 1

    connectButton = Button(text="connect", command=lambda: connect(entryName, root), width=10, height=2)
    connectButton.grid(row=1, column=2, columnspan=2, rowspan=2, padx=20, pady=5)

# the button in mainFrame
def connect(entrylist, root):
    # hide the connect frame
    root.withdraw()
    
    # get mysql config and try to connect 
    mysql_dict = {
        "mysql_ip": entrylist[0].get(),
        "username": entrylist[1].get(),
        "passwd": entrylist[2].get(),
        "port": entrylist[3].get(),
        "dbname": entrylist[4].get()
    }
    try:
        db = pymysql.connect(mysql_dict['mysql_ip'], mysql_dict['username'], mysql_dict['passwd'], mysql_dict['dbname'],
                             int(mysql_dict['port']), charset='utf8')
    except:
        tkMessageBox.showinfo("ERROR INFO", "connect to mysql failed...")

    # add child_frame, this frame is used to commit and review 
    child_frame(root, db)

def child_frame(root, db):
    window = Toplevel(root)
    window.geometry('800x300')
    
    # word label: show the numbers of word 
    word_nums = get_word_nums(db)   # get the numbers of word from database
    nums_var = StringVar()
    nums_label = Label(window, textvariable=nums_var, width=10, anchor=W, justify=LEFT)
    nums_var.set("nums : " + str(word_nums))
    nums_label.grid(row=0, pady=2)
    nums_list = [ nums_var, nums_label]

    # the entry be used to input word and meaning
    word_list = ["word", "meaning"]
    word_entry = []
    word_var = []
    rowline = 1

    for key in word_list:
        var_name = key + "_var"
        label_name = key + "_label"
        entry_name = key + "_entry"

        var_name = StringVar()
        label_name = Label(window, text=key + ":", width=10, anchor=W, justify=LEFT)
        entry_name = Entry(window, textvariable=var_name, width=20, font=12)
        label_name.grid(row=rowline, pady=2, padx=10)
        entry_name.grid(row=rowline, column=1, pady=2, padx=10)
        word_entry.append(entry_name)
        word_var.append(var_name)
        rowline += 1

    rowline += 1
    
    '''
    commitButton : commit the word into database
    reviewButton : begin to review word and the word display under the button
    quitButton   : quit the program
    '''
    commitButton = Button(window, text="commit", command=lambda: commit(word_entry, word_var, db, nums_list), width=10, height=1, pady=5)
    reviewButton = Button(window, text="review", command=lambda: review(db, window), width=10, height=1, pady=5)
    quit_bt = Button(window, text="quit", command=lambda:quit(window, root), width=10, height=1, pady=5)
        
    commitButton.grid(row=rowline, column=0, pady=4, padx=10)
    reviewButton.grid(row=rowline, column=1, pady=4, padx=10)
    quit_bt.grid(row=rowline, column=2, pady=4, padx=10)

def quit(window, root):
    window.destroy()
    root.destroy()

def check_input(list):
    for key in list:
        if len(key) == 0:
            tkMessageBox.showinfo("ERROR INFO", "word or meaning can't be null...")
            raise Exception("ERROR INFO : word or meaning can't be null...")
    
def commit(word_entry, word_var, db, nums_list):
    # get the entry input
    word_val = word_entry[0].get().strip()
    mean_val = word_entry[1].get().encode('utf-8')
    
    # check input is not null
    check_input([word_val, mean_val])

    # get total words num
    word_nums = get_word_nums(db) + 1
    nums_list[0].set("nums : " + str(word_nums))
 
    # check the word is existed??
    cursor = db.cursor()
    check_query = "select count(0) from word_db where word = '%s'" % word_val
    cursor.execute(check_query)
    data = cursor.fetchone()
    if data[0] != 0:
        tkMessageBox.showinfo("ERROR INFO", "This word is existed...")
        cursor.close()
        raise Exception("ERROR INFO, This word is existed...")

    sql_query = "insert into word_db (id, word, word_mean, ins_time, review_sign, indistinct) values (%d, '%s', '%s', CURDATE() + 0, 0, 1)" % (word_nums, word_val, mean_val)
    cursor.execute(sql_query)
    db.commit()
    cursor.close()

    # clean the entry data
    word_var[1].set("")
    word_var[0].set("")
    
def review(db, window):
    # get the id which word is indistinct or oblivious order by insert time.
    cursor = db.cursor()
    cursor.execute("select id, word, word_mean from (select * from word_db order by ins_time) as temp where remember != 1 limit 50;")
    word_res = list(cursor.fetchall())
    print word_res
    length = len(word_res)
    rowline = 5
    
    # get the word id
    id_list = []
    for key in word_res:
        id_list.append(key[0])
        
    print id_list
    
    if length == 0:
        tkMessageBox.showinfo("ERROR INFO", "No words need to review")
        raise Exception("ERROR INFO : No words need to review")
    
    # generate random id to review
    randnum_list = random.sample(id_list, len(word_res))
    rand_index = []
    rand_index.append(id_list.index(randnum_list[0]))

    # last button use the bak_index to display the last word
    bak_index = []    
    
    # review label control
    word_name = StringVar()
    mean_name = StringVar()
    word_name.set("word :" + word_res[rand_index[0]][1])
    mean_name.set("")
    Label(window, textvariable=word_name, width=30, anchor=W, justify=LEFT).grid(row=rowline, column=0, pady=4, padx=10)
    Label(window, textvariable=mean_name, width=30, anchor=W, justify=LEFT).grid(row=rowline, column=1, pady=4, padx=10)
    word_re_list = [word_name, mean_name]
 
    # review button control
    last_bt = Button(window, text="last", command=lambda: last(db, bak_index, word_res, word_re_list, randnum_list, id_list), width=10, height=1, padx=10, pady=5)
    last_bt.grid(row=rowline+2)
    
    next_bt = Button(window, text="next", command=lambda: next(db, word_res, bak_index, word_re_list, next_bt, randnum_list, id_list, rand_index), width=10, height=1, padx=10, pady=5, state='disable')
    next_bt.grid(row=rowline+2, column=1)
                 
    rem_bt = Button(window, text="remember", command=lambda: remember(db, word_res, rand_index, next_bt, word_re_list), width=10, height=1, padx=10, pady=5)
    rem_bt.grid(row=rowline+1, column=0)
    
    ind_bt = Button(window, text="indistinct", command=lambda: indistinct(db, word_res, rand_index, next_bt, word_re_list), width=10, height=1, padx=10, pady=5)
    ind_bt.grid(row=rowline+1, column=1)
    
    obl_bt = Button(window, text="oblivious", command=lambda: oblivious(db, word_res, rand_index, next_bt, word_re_list), width=10, height=1, padx=10, pady=5)
    obl_bt.grid(row=rowline+1, column=2)    
        
    cursor.close()
    
def next(db, word_res, bak_index, word_re_list, next_bt, randnum_list, id_list, rand_index):
    # delete the review word id in randnum_list and add it in bak_index
    bak_index.append(randnum_list[0])
    randnum_list.pop(0)
    if len(randnum_list) == 0:
        tkMessageBox.showinfo("ERROR INFO", "No words need to review")
        raise Exception("ERROR INFO : No words need to review")
        
    rand_index[0] = id_list.index(randnum_list[0])
    word_re_list[0].set("word :" + word_res[rand_index[0]][1])
    word_re_list[1].set("")
    next_bt['state'] = 'disable'
       
def last(db, bak_index, word_res, word_re_list, randnum_list, id_list):
    if len(bak_index) == 0:
        tkMessageBox.showinfo("ERROR INFO", "This is the first word")
        raise Exception("ERROR INFO : This is the first word")
      
    id = id_list.index(bak_index[-1])
    word_re_list[0].set("word :" + word_res[id][1])
    word_re_list[1].set("meaning :" + word_res[id][2])
    
    # delete the review word id in bak_index and add it in randnum_list
    randnum_list.insert(0, bak_index[-1])
    bak_index.pop()
       
def remember(db, word_res, rand_index, next_bt, word_re_list):
    # id : the id of query   
    id = word_res[rand_index[0]][0]
    cursor = db.cursor()
    sql_query = "update word_db set remember=1,indistinct=0,oblivious=0 where id = " + str(id)
    print (sql_query, rand_index[0])
    cursor.execute(sql_query)
    db.commit()
    cursor.close()   
    word_re_list[1].set("meaning: " + word_res[rand_index[0]][2])
    next_bt['state'] = 'normal'
    
def indistinct(db, word_res, rand_index, next_bt, word_re_list):
    # id : the id of query
    id = word_res[rand_index[0]][0]
    cursor = db.cursor()
    sql_query = "update word_db set remember=0,indistinct=1,oblivious=0 where id = " + str(id)
    cursor.execute(sql_query)
    db.commit()
    cursor.close()
    
    word_re_list[1].set("meaning: " + word_res[rand_index[0]][2])
    next_bt['state'] = 'normal'

def oblivious(db, word_res, rand_index, next_bt, word_re_list):
    # id : the id of query
    id = word_res[rand_index[0]][0]    
    cursor = db.cursor()
    sql_query = "update word_db set remember=0,indistinct=0,oblivious=1 where id = " + str(id)
    cursor.execute(sql_query)
    db.commit()
    cursor.close()
    word_re_list[1].set("meaning: " + word_res[rand_index[0]][2])
    next_bt['state'] = 'normal'
    
def get_word_nums(db):
    cursor = db.cursor()
    cursor.execute("select count(0) from word_db")
    data = cursor.fetchone()
    total_num = data[0]
    cursor.close
    return total_num
    
root = Tk()
mainFrame()
root.mainloop()
