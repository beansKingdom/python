#/usr/bin/python
# encoding:utf-8

import matplotlib
matplotlib.use('Agg')

import numpy as np
import os,sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

class GeneratePng():
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.script_name = os.path.basename(os.path.abspath(__file__))
        self.lines_color_list = ['red', 'black', 'green']

    def check_input_arguments(self):
        if (len(sys.argv) < 2):
            raise Exception("Error, error input arguments, example: %s filename", self.script_name)
        else:
            self.data_filename = sys.argv[1] + ".csv"
 
    def generate_png_info(self):
        self.image_dir = self.script_dir +  "/static"
        self.data_filepath = self.script_dir + "/data_photo/" + self.data_filename
        
    def get_lines_name(self):
        with open(self.data_filename , 'r') as file:
        for line in file:
            line = line[:-1]
            if (line[0] != '#'):
                return -1
                print ("Error, The first line not have lines_name")
            else:
                line = str(line[1:-1])
                self.lines_name_list=line.split(';')
            if len(self.lines_name_list) > 3: 
                raise Exception("Error, Too many columns data in %s, the max columns is 3", self.data_filename)
            break
            
    def get_data_from_datafile(self):
        self.data = np.loadtxt(self.data_filepath, delimiter=';', usecols=range(len(self.lines_name_list)), skiprows=1)
        
    def generate_png(self):
        plt.subplot(111)
        for i in range(len(self.lines_name_list)):
            
                
        
        
    def main(self):
        self.check_input_arguments()
        self.get_lines_name()
        self.generate_png_info()

plt.semilogx(data[:,0], data[:,1], 'red', basex=2)
plt.semilogx(data[:,0], data[:,2], 'black', basex=2)

plt.xlabel('thread_nums')
plt.ylabel('qps')

#blue_line = mlines.Line2D([], [], color='blue', marker='*',
 #                 markersize=15, label='MYSQL')
blue_line = mpatches.Patch(color='black', label='MYCAT')
red_line = mpatches.Patch(color='red', label='MYSQL')

lines = [blue_line, red_line]
labels = [line.get_label() for line in lines]
plt.legend(lines, labels)

plt.grid(True)

print (file_name, type(file_name))
plt.savefig(img_dir + "/" + sys.argv[1])
