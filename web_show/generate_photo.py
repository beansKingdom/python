#/usr/bin/python
# encoding:utf-8


import matplotlib
matplotlib.use('Agg')

import numpy as np
import os,sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines


script_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = script_dir +  "/static"
file_name = sys.argv[1] + ".csv"
file_path = script_dir + "/data_photo/" + file_name 
print (file_path)

data = np.loadtxt(file_path, delimiter=';', usecols=range(3))

plt.subplot(111)

plt.semilogx(data[:,0], data[:,1], 'red', basex=2)
plt.semilogx(data[:,0], data[:,2], 'black', basex=2)

plt.xlabel('thread_nums')
plt.ylabel('qps')

#blue_line = mlines.Line2D([], [], color='blue', marker='*',
 #                 markersize=15, label='MYSQL')
blue_line = mpatches.Patch(color='black', label='MYSQL')
red_line = mpatches.Patch(color='red', label='MYCAT')

lines = [blue_line, red_line]
labels = [line.get_label() for line in lines]
plt.legend(lines, labels)

plt.grid(True)

print (file_name, type(file_name))
plt.savefig(img_dir + "/" + sys.argv[1])
