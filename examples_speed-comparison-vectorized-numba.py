# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 15:54:57 2018

@author: sebastian
"""

# compare implementation speed of scoringtools and properscoring package
import scoringtools as st
import numpy as np
import time
import properscoring as psr
import numba

## test influence of number of observations, write to csv file

m = 50
N = np.concatenate(([50,500,1000], np.arange(5000, 100000, 5000)), axis=0)
d = 1 

st_time = np.empty(len(N))
st_meancrps = np.empty(len(N))
psr_time = np.empty(len(N))
psr_meancrps = np.empty(len(N))

k = 0
for n in N:
    print(n)
    y  =  np.random.rand(d, n)
    dat = np.random.rand(d, m, n)       

    start = time.time()
    crps_v = st.crps_sample_vec(y[0,:],dat[0,:,:])
    st_meancrps[k] = crps_v.mean()
    end = time.time()
    st_time[k] =  end-start
    
    start = time.time()
    crps_v_psr = psr.crps_ensemble(y[0,:], dat[0,:,:], axis=0)
    psr_meancrps[k] = crps_v_psr.mean()
    end = time.time()
    psr_time[k] = end-start

    k += 1

import csv
ofile  = open('computation_times_obssize_numba.csv', "w")
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

writer.writerow(psr_time) 
writer.writerow(st_time) 
writer.writerow(N)   
ofile.close()
    
    
## test influence of ensemble size, write to csv file
   
M = np.concatenate(([10,50,100], np.arange(250, 2000, 125)), axis=0)
n = 50
d = 1 

st_time = np.empty(len(M))
st_meancrps = np.empty(len(M))
psr_time = np.empty(len(M))
psr_meancrps = np.empty(len(M))

k = 0
for m in M:
    print(m)
    y  =  np.random.rand(d, n)
    dat = np.random.rand(d, m, n)       

    start = time.time()
    crps_v = st.crps_sample_vec(y[0,:],dat[0,:,:])
    st_meancrps[k] = crps_v.mean()
    end = time.time()
    st_time[k] =  end-start
    
    start = time.time()
    crps_v_psr = psr.crps_ensemble(y[0,:], dat[0,:,:], axis=0)
    psr_meancrps[k] = crps_v_psr.mean()
    end = time.time()
    psr_time[k] = end-start

    k += 1
  
     
import csv
ofile  = open('computation_times_enssize_numba.csv', "w")
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

writer.writerow(psr_time) 
writer.writerow(st_time) 
writer.writerow(M) 
ofile.close()