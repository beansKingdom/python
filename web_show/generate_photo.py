# /usr/bin/python
# encoding:utf-8

import matplotlib
matplotlib.use('Agg')
import numpy as np
import os, sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

class GeneratePng():
    def __init__(self, filename, linetype):
        self.filename = filename
        self.linetype = linetype
        self.data_filename = filename + ".csv"
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.script_name = os.path.basename(os.path.abspath(__file__))
        self.lines_color_list = ['red', 'black', 'green', 'blue', 'cyan']

    def get_lines_name(self):
        with open(self.data_filepath, 'r') as file:
            for line in file:
                line = line[:-1]
                if (line[0] != '#'):
                    raise Exception("Error, Not get the lines' name, data file the first line must be #names")
                else:
                    line = str(line[1:-1])
                    self.lines_name_list = line.split(';')
                if len(self.lines_name_list) > 5:
                    raise Exception("Error, Too many columns data in %s, the max columns is 5", self.data_filename)
                break

    def generate_png_info(self):
        self.image_dir = self.script_dir + "/static"
        self.data_filepath = self.script_dir + "/data_photo/" + self.data_filename

    def get_data_from_datafile(self):
        self.data = np.loadtxt(self.data_filepath, delimiter=';', usecols=range(len(self.lines_name_list)+1), skiprows=1)
        if len(self.data) != (len(self.lines_name_list)+1):
            raise Exception("Error, data columns isn't equal to lines name")

    def generate_png(self):
        plt.subplot(111)
        for i in range(len(self.lines_name_list)):
            if self.linetype == 'linear':
                print ("linear")
                plt.plot(self.data[:, 0], self.data[:, i+1], self.lines_color_list[i])
            elif self.linetype == 'logarithm':
                print ("log")
                plt.semilogx(self.data[:, 0], self.data[:, i+1], self.lines_color_list[i], basex=2)
            else:
                print ("other")
                pass
        
        self.sign_lines()
        plt.xlabel('thread_nums')
        plt.ylabel('qps')
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
        self.generate_png_info()
        self.get_lines_name()
        self.get_data_from_datafile()
        self.generate_png()

##########################################

if (len(sys.argv) < 3):
    script_name = os.path.basename(os.path.abspath(__file__))
    raise Exception("Error, error input arguments, example: %s test.csv(datafilename) linear/logarithm/exponent(linetype)" % script_name)
else:
    filename = sys.argv[1]
    linetype = sys.argv[2]
    

gen_png = GeneratePng(filename, linetype)
gen_png.main()

