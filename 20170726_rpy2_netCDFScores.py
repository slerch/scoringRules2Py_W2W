# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 09:10:04 2017

@author: manuel
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 16:19:47 2017

@author: manuel
"""
import xarray as xr
import numpy as np
import time
import rpy2
import rpy2.robjects.numpy2ri as np2ri
from rpy2.robjects.packages import importr
srl = importr('scoringRules')

ob_file = "/home/sebastian/Dropbox/Manuel_HIWI/code/ECMWF_20131001-31date_06int_uv10m_wind_MSLP_ECMWF_analysis.nc"
fc_file = "/home/sebastian/Dropbox/Manuel_HIWI/code/EPS_uv10m_MSLP_6h_5day_20131001.nc"

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
    
# Read File
obs = xr.open_dataset(ob_file)
forc = xr.open_dataset(fc_file)

# Subset relevant data
print(obs.time.values[4])
# - select analysis of the date 2013-10-02
obs_sb = obs[dict(time=[4])]
# - select forcast valid at 2013-10-02 (initialized at 2013-10-01)
forc_sb = forc[dict(time=[4])]

# Reshape
# - merge all variables (namely msl, u10 and v10) to one variable of 3 dimensions
obs_arr = obs_sb.to_array()
# - drop the dimensions time, longitude and latitude and extract the numpy array
obs_vec = obs_arr.stack(m = ('time', 'longitude', 'latitude')).values

forc_arr = forc_sb.to_array()
forc_vec = forc_arr.stack(m = ('time', 'longitude', 'latitude')).values

# Compute Scores, in a loop
loop_start = time.time()
N = obs_vec.shape[1]
crps = 0
escr = 0
vscr = 0
for i in range(0,N):
    y = obs_vec[0,i] # crps computed only for mslp    
    dat = forc_vec[0,:,i]
    crps += crps_sample(y, dat)
    
    y_vec = obs_vec[:,i]
    dat_mat = forc_vec[:,:,i]
    escr += es_sample(y_vec, dat_mat)
    vscr += vs_sample(y_vec, dat_mat)
crps = crps/N
vscr = vscr/N
escr = escr/N
loop_end = time.time()
print('CRPS')
print(crps)
print('Energy Score')
print(escr)
print('Variogram Score')
print(vscr)
print('Time needed [s]')
print(round(loop_end - loop_start,4))

# additional example: crps for all variables
# compute crps for all 3 variables
crps2 = np.zeros([3,N])
for i in range(0,N):
    for j in range(0,obs_vec.shape[0]):
        y = obs_vec[j,i]
        dat = forc_vec[j,:,i]
        crps2[j,i] = crps_sample(y, dat)

# compute column-wise mean        
np.mean(crps2, axis=1)

# Compute Scores, no loop via apply (faster)
vec_start = time.time()
crps_v = crps_sample_vec(obs_vec[0,:], forc_vec[0,:,:]) # crps computed only for mslp 
escr_v = es_sample_vec(obs_vec, forc_vec)
vscr_v = vs_sample_vec(obs_vec, forc_vec)
vec_end = time.time()

print('CRPS')
print(crps_v)
print('Energy Score')
print(escr_v)
print('Variogram Score')
print(vscr_v)
print('Time needed [s]')
print(round(vec_end - vec_start,4))