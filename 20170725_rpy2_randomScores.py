# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 10:27:39 2017

@author: manuel
"""
import rpy2
import numpy as np
import rpy2.robjects.numpy2ri as np2ri

from rpy2.robjects.packages import importr
srl = importr('scoringRules')

### 1-Dimensional Case
y = 5
dat = rpy2.robjects.FloatVector([1,2,3,4])
crps = srl.crps_sample(y,dat)
print(crps)

### d-Dimensional Case
d = 5
n = 50
y_vec  =  rpy2.robjects.FloatVector(np.random.rand(d, 1))
dat_mat = np2ri.py2ri(np.random.rand(d, n))

escr = srl.es_sample(y_vec, dat_mat)
print(escr)
vscr = srl.vs_sample(y_vec, dat_mat)
print(vscr)