#!/usr/bin/python
# encoding:utf-8

import matplotlib
matplotlib.use('Agg')
import numpy as np
import re
import os, sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import linecache

class GeneratePng():
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.script_name = os.path.basename(os.path.abspath(__file__))
        self.lines_color_list = ['red', 'black', 'green', 'blue', 'cyan']
        
    def check_input_arguments(self):
        if (len(sys.argv) < 3):
            self.usage()
        else:
            print (len(sys.argv))
            self.filename = sys.argv[1]
            self.data_filename = self.filename + ".csv"
            self.linetype = sys.argv[2] 
            
        pattern = re.compile(r'^\d+$')
        if len(sys.argv) > 3:
            if pattern.match(sys.argv[3]):
                self.base_num = int(pattern.match(sys.argv[3]).group())
        else:
            self.base_num = 2        

    def usage(self):
        print ("Error, error input arguments")
        print ("example: %s test.csv(datafilename) linear/logarithm/exponent(linetype)" % self.script_name)
        print ("         if linetype is logarithm/exponent, you can input a base_num")
        print ("         %s test.csv(datafilename) logarithm/exponent base_num(default 2)" % self.script_name)
        sys.exit(1)

    def generate_png_info(self):
        self.image_dir = self.script_dir + "/static"
        self.data_filepath = self.script_dir + "/data_photo/" + self.data_filename
        
    def get_lines_name(self):
        with open(self.data_filepath, 'r') as file:
            line_data = linecache.getline(self.data_filepath, 1)
            line_data = line_data[:-1]
            if (line_data[0] != '#'):
                raise Exception("Error, Not get the lines' name, data file the first line must be #names")
            else:
                line_data = str(line_data[1:])
                self.lines_name_list = line_data.split(';')
                
            if len(self.lines_name_list) > 5:
                    raise Exception("Error, Too many columns data in %s, the max columns is 6", self.data_filename)

    def get_data_from_datafile(self):
        self.data = np.loadtxt(self.data_filepath, delimiter=';', usecols=range(len(self.lines_name_list)+1), skiprows=1)
        if len(self.data[0]) != (len(self.lines_name_list)+1):
            raise Exception("Error, data columns isn't equal to lines'name numbers")

    def check_data(self):
        for i in range(len(self.lines_name_list)):
            if len(self.data[:, 0]) != len(self.data[:, i+1]):
                raise Exception("Error, data's rows number isn't same")

    def generate_png(self):
        plt.subplot(111)
        self.check_data()
        for i in range(len(self.lines_name_list)):
            if self.linetype == 'linear':
                plt.plot(self.data[:, 0], self.data[:, i+1], self.lines_color_list[i])
            elif self.linetype == 'logarithm':
                plt.semilogx(self.data[:, 0], self.data[:, i+1], self.lines_color_list[i], basex=self.base_num)
            elif self.linetype == 'exponent':
                raise Exception("Error, Not complete... exit")
            else:
                self.usage()
                raise Exception("Error, error linetype arguments")
                
        self.sign_lines()
        #plt.xlabel('thread_nums')
        #plt.ylabel('qps')
        plt.grid(True)
        plt.show()
        plt.savefig(self.image_dir + "/" + self.filename)

    def sign_lines(self):
        lines = []
        for i in range(len(self.lines_name_list)):
            linename = self.lines_color_list[i] + "line"
            linename = mpatches.Patch(color=self.lines_color_list[i], label=self.lines_name_list[i])
            lines.append(linename)
            
        labels = [line.get_label() for line in lines]  
        plt.legend(lines, labels)
        
    def main(self):
        self.check_input_arguments()
        self.generate_png_info()
        self.get_lines_name()
        self.get_data_from_datafile()
        self.generate_png()

##########################################
gen_png = GeneratePng()
gen_png.main()