# encoding:utf-8

from flask import Flask
from flask import render_template
import time
import os

app = Flask(__name__)

@app.route("/")
def index():

    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    img_dir = script_dir +  "/static"
    file_names = []
    list = os.listdir(img_dir)
     
    for line in list:
        name = os.path.basename(line)
        if os.path.isdir(name):#如果filepath是目录
            continue
        else:
            file_names.append(name)


    return render_template('hello.html', name='hly', file_name=file_names)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
