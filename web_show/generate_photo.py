#/usr/bin/python
# encoding:utf-8


import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
import os,sys

script_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = script_dir +  "/static"
file_name = sys.argv[1] + ".csv"
file_path = script_dir + "/data_photo/" + file_name 
print (file_path)

data = np.loadtxt(file_path, delimiter=';', usecols=range(3))

plt.figure(figsize=(4,3))
plt.subplot(111)

plt.semilogx(data[:,0], data[:,1], 'red', basex=2)
plt.semilogx(data[:,0], data[:,2], 'green', basex=2)

plt.title('semilogx')
plt.grid(True)

print (file_name, type(file_name))
plt.savefig(img_dir + "/" + sys.argv[1])
