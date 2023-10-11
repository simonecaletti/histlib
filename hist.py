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
import numpy as np 


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
        self.ncol = self.get_ncols()

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
        new_array = np.hstack((self.get_array(), newcol))
        if newcolname is not None: self.keys.append(newcolname)
        else: self.automatic_colnames()
        self.data = self.get_dict()
        return new_array

    def get_dict(self):
        array = self.get_array()
        self.automatic_colnames()
        if self.check_ncols():
            self.data = utils.array2dict(array, self.keys)
            return self.data
        else:
            return None

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
    def __init__(self, obj, output_path="."):
        self.obj = obj
        self.itstype = self.get_type()
        self.nlayer = self.get_layer()
        self.output_path = output_path
        
    def get_type(self):
        if type(self.obj) == dict:
            return "dict"
        else:
            print("Error: obj is not a dict. Use get_dict() method on DataFile or Collections before plotting.")
            return None

    def get_layer(self):

        ilayer = 0
        if self.itstype == "dict":
            isDict = True
            test = self.obj[list(self.obj.keys())[0]]
            while isDict:
                if isinstance(test, dict): 
                    test = test[list(test.keys())[0]]
                    ilayer += 1
                elif isinstance(test, np.ndarray):
                    isDict = False
                else: 
                    print("Error: nested object are not dict or list.")
                    break
                       
            return ilayer

        else:
            print("Error: obj is not a dict. Use get_dict() method on DataFile or Collections before plotting.")
            return None

    def gen_plots(self):

        return None
        
    def get_pdf(self):

        return pdf

    def add_ratioplot(self, keynum, keyden):

        return None

    def add_legend(self):

        return None

    
        

