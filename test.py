#!/bin/python3

import hist
import matplotlib.pyplot as plt 
import numpy as np 

path = "./combined/Final/"
filenames = ["LO.pt_had.dat", "LO.xit_hadZ.dat", "NLO.pt_had.dat", "NLO.xit_hadZ.dat"]
pdfnames = ["LO.pt_had.pdf", "LO.xit_hadZ.pdf", "NLO.pt_had.pdf", "NLO.xit_hadZ.pdf"]

for fn, pdf in zip(filenames, pdfnames):

    df = hist.DataFile(path + fn)
    keys = ["left", "center", "right", "value05", "err05", "value1", "err1", "value2", "err2"]
    df.update_colnames(keys)
    #df.add_bincenter("zd", "zu")
    df.add_alledges("left", "right")
    t = hist.Plot(df.data, filename = pdf)
    t.print("value1")
