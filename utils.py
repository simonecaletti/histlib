#### Library with utilities for plotting histograms
#### author: Simone Caletti
####: email: scaletti@phys.ethz.ch
#### last update: October 2023

#### File base on an earlier version written by Gregory Soyez
#### and another one previously written by Gavin Salam.

import numpy as np 
import pandas as pd 
import io, sys, os
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
    ncol = len(array[0, :])
    if ncol != len(keys): print("Error: different number of keys and columns.")
    #otherwise fill the dict
    else: 
        for key, icol in zip(keys, range(ncol)):
            dict[key] = array[:, icol]
    
    return dict

def all_edges(left, right):
    edges = left.copy()
    edges = np.append(edges, right[-1])
    return edges

def get_bincenter(left, right):
    center = []
    for l, r in zip(left, right):
        center.append((l+r)/2)
    return np.array(center)

#######################################################################
#Function for the Collection class 

def obj2collect(obj_list, features):
    dict = {}
    if len(obj_list) == len(features):
        for obj, feat in zip(obj_list, features):
            dict[feat] = obj
    else:
        print("Error: different number of objects and features.")

    return dict

#########################################################################
#Functions for the final script

def get_filenames_from(path):
    if path[-1] != "/": path += "/"
    filenames = [f for f in os.listdir(path) if os.path.isfile(path + f)]
    return filenames 

def automatic_output_names(filenames, format="pdf"):
    outnames = []
    for name in filenames:
        newname = name[:-3]
        newname += format
        outnames.append(newname)
    return outnames 

