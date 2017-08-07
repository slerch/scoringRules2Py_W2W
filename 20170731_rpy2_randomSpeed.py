# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 15:22:53 2017

@author: manuel
"""

import scoringtools as st
import matplotlib.pyplot as plt
import numpy as np
import time

d = 5
N = [50,500,5000]
loop_speed = np.empty(len(N))
loop_speed[:] = 0
vec_speed = np.empty(len(N))
vec_speed[:] = 0
k = 0
n = 50

for n in N:
    y  =  np.random.rand(d, n)
    dat = np.random.rand(d, 50,n)
    
    # Speed of loop
    start = time.time()
    crps = 0
    escr = 0
    vscr = 0
    for i in range(0,n):
        crps += st.crps_sample(y[0,i], dat[0,:,i])
        escr += st.es_sample(y[:,i], dat[:,:,i])
        vscr += st.vs_sample(y[:,i], dat[:,:,i])
    crps = crps/n
    vscr = vscr/n
    escr = escr/n
    end = time.time()
    loop_speed[k] = round(end-start,2)
    
    # Speed of vectorized version
    start = time.time()
    crps_v = st.crps_sample_vec(y[0,:],dat[0,:,:])
    escr_v = st.es_sample_vec(y, dat)
    vscr_v = st.vs_sample_vec(y,dat)
    end = time.time()
    vec_speed[k] =  round(end-start,2)
    k += 1
    
# Check
round(abs(crps - crps_v.mean()) + abs(escr - escr_v.mean()) + abs(vscr - vscr_v.mean()), 5)

# Plot
plt.plot(N,loop_speed, 'r', N,vec_speed, 'b')
plt.ylabel('Time [s]')
plt.xlabel('N')
plt.show()