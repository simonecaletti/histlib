#!/bin/python3

import utils, hist
import matplotlib.pyplot as plt 
import numpy as np 

path = "./combined/Final/"
#filenames = utils.get_filenames_from(path) #consider also LO.cross.dat file which has a different structure
#filenames = utils.remove_crossfiles(filenames)
#pdfnames = utils.automatic_output_names(filenames)

filenames = ["LO.xit_hadZ.dat"]
pdfnames = ["LO.xit_hadZ.pdf"]

keys = ["left", "center", "right", "value05", "err05", "value1", "err05", "value2", "err2"]

for fn, pdf in zip(filenames, pdfnames):

    #upload data and build datafile objects
    df = hist.DataFile(path + fn)
    df.update_colnames(keys)
    df.add_alledges("left", "right")
    #df.add_bincenter("left", "right")

    #Eventually collect datafiles in Collections
    #project = hist.Collection([list of dfs], [list of feature])

    #create plot object 
    t = hist.Plot(df.data, outname = pdf)
    t.set_size(1, 1)

    #Add histogram to the plot 
    t.get_hist("value1")
    t.get_hist("value2")
    t.get_hist("value05")

    #customize the plot
    t.title(fn)
    t.xaxis([0, 5, 0.5]) # [start, end, step]

    #print the plot
    t.print()
