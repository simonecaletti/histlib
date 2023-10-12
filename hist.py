#### Library with utilities for plotting histograms
#### author: Simone Caletti
####: email: scaletti@phys.ethz.ch
#### last update: October 2023

#### File base on an earlier version written by Gregory Soyez
#### and another one previously written by Gavin Salam.

#import numpy as np 
#import pandas as pd 
#import io, sys
#import re
#import string

import utils
import plot
import numpy as np
import matplotlib.pyplot as plt


######################################################################



default_encoding='utf-8'


######################################################################



#Dataframe class to read .dat files with histograms
class DataFile:
    def __init__(self, file_path, separator=' ', fortran=False, dtype=float, ncol=0, colnames=None, skip=[0, 0]):
        self.file_path = file_path
        self.separator = separator
        self.fortran = fortran 
        self.keys = colnames if colnames is not None else []  # Use an empty list if column_names is not provided
        self.skip = skip
        self.data = self.get_dict()
        self.array = self.get_array()
        self.ncols = self.get_ncols()

    def get_array(self):
        return utils.get_array(self.file_path, fortran=self.fortran, skip=self.skip, separator=self.separator)

        
    def get_ncols(self):
        array = self.get_array()
        return len(array[0,:])

    def check_ncols(self):
        if self.get_ncols() != len(self.keys) and self.keys != []: 
            print("Error: ncols and number of column's names should be the same.")
            return False
        elif self.keys == []:
            self.automatic_colnames()
            return True
        else:
            return True

    def automatic_colnames(self):
        if self.keys == []:
            for colname in ["col{}".format(icol) for icol in range(self.get_ncols())]: self.keys.append(colname)
        return None

    def get_colnames(self):
        return self.keys

    def update_colnames(self, keys):
        self.keys = keys
        self.data = self.get_dict()
        if not self.check_ncols(): print("Set new colnames.")
        return None

    def append_column(self, newcol, newcolname=None):
        new_array = np.column_stack((self.get_array(), newcol))
        if newcolname is not None: self.keys.append(newcolname)
        else: self.automatic_colnames()
        #self.ncols += 1
        self.array = new_array
        self.data[newcolname] = np.array(newcol)
        return None

    def get_bincenter(self, leftcolname, rightcolname):
        return utils.get_bincenter(self.data[leftcolname], self.data[rightcolname])

    def add_bincenter(self, leftcolname, rightcolname, newcolname="center"):
        center = self.get_bincenter(leftcolname, rightcolname)
        self.append_column(center, newcolname)
        return None

    def get_alledges(self, leftcolname, rightcolname):
        return utils.all_edges(self.data[leftcolname], self.data[rightcolname])

    def add_alledges(self, leftcolname, rightcolname, newcolname="edges"):
        edges = self.get_alledges(leftcolname, rightcolname)
        self.data[newcolname] = edges
        return None

    def get_dict(self):
        array = self.get_array()
        self.automatic_colnames()
        self.data = utils.array2dict(array, self.keys)
        return self.data

#Collection class, to collect different DataFile with common feature in a smart way
class Collection:
    def __init__(self, objects, features):
        self.objects = objects
        self.features = features
        self.data = self.get_dict()

    def get_dict(self):
        return utils.obj2collect(self.objects, self.features)

    def get_feature(self):
        return self.features



#Plot class, to make plots out of a collection of (collections of) DataFiles
class Plot:
    def __init__(self, datafile, output_path="./", filename="testplot"):
        self.datafile = datafile
        self.output_path = output_path
        self.filename = filename
        

    def get_hist(self, weightskey, centerkey="center", edgeskey="edges", histtype="step"):
        return plot.get_hist(self.datafile, weightskey, centerkey=centerkey, edgeskey=edgeskey, histtype=histtype)

    def print(self, weightskey, centerkey="center", edgeskey="edges", histtype="step", format="pdf"):
        self.get_hist(weightskey, centerkey=centerkey, edgeskey=edgeskey, histtype=histtype)
        plt.savefig(self.filename, format=format)
        plt.close()
        return None

    def ratioplot(self, keynum, keyden):
        ratio = np.ndarray([num/den for num, den in zip(self.datafile[keynum], self.datafile[keyden])])
        
        return None

    def add_legend(self):

        return None

    
        

