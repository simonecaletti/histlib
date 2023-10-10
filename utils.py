#### Library with utilities for plotting histograms
#### author: Simone Caletti
####: email: scaletti@phys.ethz.ch
#### last update: October 2023

#### File base on an earlier version written by Gregory Soyez
#### and another one previously written by Gavin Salam.

import numpy as np 
import pandas as pd 
import io, sys
import re
import string
from builtins import range


######################################################################



default_encoding='utf-8'


######################################################################
#Functions for the DataFrame class 

class Error(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, msg):
      self.msg = msg

def open_any(filename, mode=None):
    """Return either a gzipped file or a normal file, based on the extension"""
    if (len(filename)>3 and filename[-3:] == '.gz'):
        import gzip
        return gzip.GzipFile(filename, mode)
    else:
        return open(filename, mode)

def decode(line):
    if (isinstance(line,bytes)): return line.decode(default_encoding)
    else: return line


def get_array(file, regexp=None, fortran=False, skip=[0,0], separator=' '):

  if (isinstance(file,str)) : file = open_any(file, 'r')
  if (regexp != None)       : search(file,regexp)

  # handle case where we numbers such as 0.4d3 (just replace d -> e)
  fortranRegex = re.compile(r'd', re.IGNORECASE)
  
  lines = []    # temporary store of lines, before conversion to array
  started = False

  nlines = len(file.readlines())
  file.seek(0)

  while True:
    line = decode(file.readline()) 
    if(not line)               : break        # empty line = end-of-file
    line = line.rstrip()                       # strips trailing blanks, \n
    line = line.lstrip()                       # strips leading blanks
    if (not line) :
      if (started) : break                     # empty line = end-of-block
      else         : continue                  
    if (not re.match('[-0-9]', line)) : continue
    if (fortran): line = re.sub(fortranRegex,'e',line) # handle fortran double-prec
    lines.append(line)                         # collect the line
    started = True

  # do some basic error checking
  if (len(lines) < 1):
    raise Error("Block in get_array had 0 useful lines.")

  #keep only the lines you want according to skip 
  goodlines = []
  iline = 0
  for line in lines:
    if iline in range(skip[0], nlines-skip[1]): goodlines.append(line)
    iline += 1

  # now we know the size, transfer the information to a numpy ndarray
  ncol = len(' '.join([s.strip() for s in goodlines[0].split(separator)]).split())                
  num_array = np.empty( (len(goodlines), ncol) )
  for i in range(len(goodlines)):
    cleaned = ' '.join([s.strip() for s in goodlines[i].split(separator)]).split()
    num_array[i, :] = cleaned
  return num_array

def array2dict(array, keys):

    dict = {}
    #check
    ncol = len(array[1, :])
    if ncol != len(keys): print("Error: different number of keys and columns.")
    #otherwise fill the dict
    else: 
        for key, icol in zip(keys, range(ncol)):
            dict[key] = array[:, icol]
    
    return dict

#######################################################################
#Function for the Collection class 

def df2collect(df_list, features):
    dict = {}
    if len(df_list) == len(features):
        for df, feat in zip(df_list, features):
            dict[feat] = df
    else:
        print("Error: different number of DataFrames and features.")

    return dict
