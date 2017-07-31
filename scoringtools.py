# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 15:03:54 2017

@author: manuel
"""

import numpy as np
import rpy2
import rpy2.robjects.numpy2ri as np2ri
from rpy2.robjects.packages import importr
srl = importr('scoringRules')

# Define Wrapper
def es_sample(y, dat):
    # Names like srl, np2ri have to be set by the ensembletools package
    # in order to avoid imports in each function call
    try:
        y = np.array(y)
        dat = np.array(dat)
        y_r = rpy2.robjects.FloatVector(y)
        dat_r = np2ri.py2ri(dat)
    except:
        print('Input has wrong format.')
        
    return srl.es_sample(y_r, dat_r)[0]
    
def es_sample_vec(y_mat, dat_mat):
    try:
        y_mat = np.array(y_mat)
        y_mat = np.expand_dims(y_mat, 1)
        dat_mat = np.array(dat_mat)
    except:
        print('Input has wrong format.')
    else:
        if ( 
             len(y_mat.shape) != 3 or 
             len(dat_mat.shape) != 3 or 
             y_mat.shape[0] != dat_mat.shape[0] or
             y_mat.shape[2] != dat_mat.shape[2]
        ):
            raise ValueError('Parameters have wrong dimension.')

    df = np.concatenate((y_mat,dat_mat),axis = 1)
    df_r = np2ri.py2ri(df)
    rpy2.robjects.globalenv['df'] =  df_r
    
    return rpy2.robjects.r('mean(apply(df, c(3), function(x) es_sample(x[,1], x[,-1])))')[0]
    
def vs_sample(y, dat):
    try:
        y = np.array(y)
        dat = np.array(dat)
        y_r = rpy2.robjects.FloatVector(y)
        dat_r = np2ri.py2ri(dat)
    except:
        print('Input has wrong format.')

    return srl.vs_sample(y_r, dat_r)[0]
    
def vs_sample_vec(y_mat, dat_mat):
    try:
        y_mat = np.array(y_mat)
        y_mat = np.expand_dims(y_mat, 1)
        dat_mat = np.array(dat_mat)
    except:
        print('Input has wrong format.')
    else:
        if ( 
             len(y_mat.shape) != 3 or 
             len(dat_mat.shape) != 3 or 
             y_mat.shape[0] != dat_mat.shape[0] or
             y_mat.shape[2] != dat_mat.shape[2]
        ):
            raise ValueError('Parameters have wrong dimension.')

    df = np.concatenate((y_mat,dat_mat),axis = 1)
    df_r = np2ri.py2ri(df)
    rpy2.robjects.globalenv['df'] =  df_r
    
    return rpy2.robjects.r('mean(apply(df, c(3), function(x) vs_sample(x[,1], x[,-1])))')[0]
    
def crps_sample(y, dat):
    try:
        y_r = float(y)
        dat = np.array(dat)
        dat_r = rpy2.robjects.FloatVector(dat)
    except:
        print('Input has wrong format.')
        
    return srl.crps_sample(y_r, dat_r)[0]
    
def crps_sample_vec(y_vec, dat_mat):
    try:
        y_vec = np.array(y_vec)
        dat_mat = np.array(dat_mat)
        y_r = rpy2.robjects.FloatVector(y_vec)
        dat_r = np2ri.py2ri(dat_mat)
    except:
        print('Input has wrong format.')
    else:
        if len(y_vec.shape) != 1 or len(dat_mat.shape) != 2 or y_vec.shape[0] != dat_mat.shape[1]:
            raise ValueError('Parameters have wrong dimension.')

    rpy2.robjects.globalenv['obs'] =  y_r
    rpy2.robjects.globalenv['forc'] =  dat_r
    
    return rpy2.robjects.r('mean(apply(rbind(obs,forc), 2, function(x) crps_sample(x[1], x[-1])))')[0]
