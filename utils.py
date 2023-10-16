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
from itertools import product

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

def find_fnpattern(filenames, pattern):
    same = []
    for name in filenames:
        if name.find(pattern) != -1: #unfortunaltely NLO (NNLO) contains the pattern LO (NLO, LO) so we have to remove them manually
            if pattern == "LO" and name.find("NLO") == -1: same.append(name)
            elif pattern == "NLO" and name.find("NNLO") == -1: same.append(name)
            elif pattern != "LO" and pattern != "NLO": same.append(name)
    return same

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def full_intersection(list_of_lists):
    nlist = len(list_of_lists)
    temp = list_of_lists[0].copy()
    for i in range(1, nlist):
        temp = intersection(temp, list_of_lists[i])
    return temp 

def product(ar_list):
    if not ar_list:
        yield ()
    else:
        for a in ar_list[0]:
            for prod in product(ar_list[1:]):
                yield (a,)+prod 

def get_pairings_from(filenames, patterns): #patterns = [[feat1.1, feat1.2, ...], [feat2.1, feat2.2, ...], ...]
    pairings = []
    i = 0
    combs = list(product(patterns))
    print(combs)
    nlayer = len(combs[0])
    for c in combs:
        file = full_intersection([find_fnpattern(filenames, p) for p in c])  #now we have a file associated to a combo
        pairings.append((file, c))
    return pairings 
        
def pairings2collect(pairings):

    return None



    for p in patterns: # [["pt_had", "xit_hadZ"], ["LO", "NLO"]]
        temp.append(find_fnpattern(filenames, p[i]))
    file = full_intersection(temp)



    return collection 

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

def remove_crossfiles(filenames):
    newfilenames = []
    for name in filenames:
        if name.find("cross") == -1:
            newfilenames.append(name)
    return newfilenames 
