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
import matplotlib.pyplot as plt
import plot
import matplotlib.gridspec as gridspec

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

    def get_col(self, colkey):
        return self.data[colkey] 

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
    def __init__(self, datafile, w=1., h=1., outname="plot"):
        self.datafile = datafile 
        self.outname = outname
        self.width = w 
        self.height = h 
        self.canvas = self.get_canvas()
        self.nsubplot = 1 
    
    def get_canvas(self, nrows=1, ncols=1):
        f, ax = plt.subplots(nrows, ncols, sharex=True, figsize=(self.width , self.height), dpi=100)
        return (f, ax)

    def set_size(self, w, h):
        self.width = w 
        self.height = h
        self.canvas = self.get_canvas()
        return None 

    def get_size(self):
        return self.width, self.height

    def get_hist(self, weightskey, centerkey="center", edgeskey="edges", histtype="step"):
        return plt.hist(self.datafile[centerkey], self.datafile[edgeskey], weights=self.datafile[weightskey], histtype=histtype) 

    def print(self, format="pdf"):
        plt.savefig(self.outname, format=format)
        plt.close()
        return None

    def title(self, title):
        plt.title(title)
        return None

    def xaxis(self, xinfo, logscale=False, ifshow=True): #xinfo = [start, end, step]
        if logscale:
            plot.set_logx_axis(self.canvas[1], xinfo[0], xinfo[1], if_show=ifshow) #xinfo=[start, end]
        else:
            plot.set_x_axis(self.canvas[1], xinfo, if_show=ifshow)
        return None

    def yaxis(self, yinfo, ifshow=True):
        plot.set_y_axis(self.canvas[1], yinfo, if_show=ifshow)
        return None

    def ratioplot(self, keynum, keyden, relative_height):  #not working
        self.nsubplot += 1 
        self.canvas = self.get_canvas(nrows=self.nsubplot, ncols=1)
        gs = gridspec.GridSpec(1, self.nsubplot, height_ratios=relative_height)
        gs.update(wspace=0.0, hspace=0.0)
        return None

        self.canvas[1] = [plt.subplot(gs[0,0])]
        for i in range(self.nsubplot):
            self.canvas[1] += [plt.subplot(gs[i+1, 0])]

        return None

    def grid(self):
        self.canvas[1].grid(True, which="major")
        return None

    def add_legend(self):

        return None

    
        

