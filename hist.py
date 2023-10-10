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
        self.data = {}
        self.ncol = self.get_ncols()

    def get_array(self):
        return utils.get_array(self.file_path, fortran=self.fortran, skip=self.skip, separator=self.separator)

        
    def get_ncols(self):
        array = self.get_array()
        return len(array[0,:])

    def check_ncols(self):
        if self.ncol != len(self.keys) and self.keys != []: 
            print("Error: ncols and number of column's names should be the same.")
            return False
        else:
            return True

    def automatic_colnames(self):
        if self.keys == []:
            for colname in ["col{}".format(icol) for icol in range(self.ncol)]: self.keys.append(colname)
        return None

    def get_colnames(self):
        return self.keys

    def update_colnames(self, keys):
        self.keys = keys
        if not self.check_ncols(): print("Set new colnames.")

    def get_dict(self):
        array = self.get_array()
        self.automatic_colnames()
        if self.check_ncols():
            return utils.array2dict(array, self.keys)
        else:
            return None

        
