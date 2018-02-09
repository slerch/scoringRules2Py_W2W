# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 14:49:51 2017

@author: sebastian
"""

# compare implementation speed of scoringtools and properscoring package
import scoringtools as st
import numpy as np
import time
import properscoring as psr

d = 1 
N = [50,500,1000,5000,10000,20000,50000,100000]
st_speed = np.empty(len(N))
st_speed[:] = 0
st_meancrps = np.empty(len(N))
st_meancrps[:] = 0
psr_speed = np.empty(len(N))
psr_speed[:] = 0
psr_meancrps = np.empty(len(N))
psr_meancrps[:] = 0

stnonvec_speed = np.empty(len(N))
stnonvec_speed[:] = 0
stnonvec_meancrps = np.empty(len(N))
stnonvec_meancrps[:] = 0
k = 0

for n in N:
    y  =  np.random.rand(d, n)
    dat = np.random.rand(d, 50,n)
       
    # speed of scoringtools implementation
    start = time.time()
    crps_v = st.crps_sample_vec(y[0,:],dat[0,:,:])
    st_meancrps[k] = crps_v.mean()
    end = time.time()
    st_speed[k] =  round(end-start,3)
    
    # speed of non-vectorized scoringtools implementation
    start = time.time()
    crps = 0
    for i in range(0,n):
        crps += st.crps_sample(y[0,i], dat[0,:,i])
    stnonvec_meancrps[k] = crps/n
    end = time.time()
    stnonvec_speed[k] = round(end-start,3)

    # speed of properscoring implementation
    start = time.time()
    crps = 0
    for i in range(0,n):
        crps += psr.crps_ensemble(y[0,i], dat[0,:,i])
    psr_meancrps[k] = crps/n
    end = time.time()
    psr_speed[k] = round(end-start,3)

    k += 1

st_meancrps
stnonvec_meancrps
psr_meancrps

psr_speed - st_speed
psr_speed - stnonvec_speed