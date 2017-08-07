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
import scoringtools as st
import xarray as xr
import numpy as np
import time

ob_file = "/home/manuel/Dokumente/Ausbildung_Studium/Karlsruhe/1516WS/Praktikum/ensembleScore/Input/Observation/ECMWF_20131001-31date_06int_uv10m_wind_MSLP_ECMWF_analysis.nc"
fc_file = "/home/manuel/Dokumente/Ausbildung_Studium/Karlsruhe/1516WS/Praktikum/ensembleScore/Input/Forecast/ECMWF_okt2013/EPS_uv10m_MSLP_6h_5day_20131001.nc"
#ob_file = "/home/sebastian/Dropbox/Manuel_HIWI/code/ECMWF_20131001-31date_06int_uv10m_wind_MSLP_ECMWF_analysis.nc"
#fc_file = "/home/sebastian/Dropbox/Manuel_HIWI/code/EPS_uv10m_MSLP_6h_5day_20131001.nc"
    
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
    crps += st.crps_sample(y, dat)
    
    y_vec = obs_vec[:,i]
    dat_mat = forc_vec[:,:,i]
    escr += st.es_sample(y_vec, dat_mat)
    vscr += st.vs_sample(y_vec, dat_mat)
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
        crps2[j,i] = st.crps_sample(y, dat)

# compute column-wise mean        
np.mean(crps2, axis=1)

# Compute Scores, no loop via apply (faster)
vec_start = time.time()
crps_v = st.crps_sample_vec(obs_vec[0,:], forc_vec[0,:,:]) # crps computed only for mslp 
escr_v = st.es_sample_vec(obs_vec, forc_vec)
vscr_v = st.vs_sample_vec(obs_vec, forc_vec)
vec_end = time.time()

print('CRPS')
print(crps_v.mean())
print('Energy Score')
print(escr_v.mean())
print('Variogram Score')
print(vscr_v.mean())
print('Time needed [s]')
print(round(vec_end - vec_start,4))