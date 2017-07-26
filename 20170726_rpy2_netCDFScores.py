# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 16:19:47 2017

@author: manuel
"""
import xarray as xr
import rpy2
import rpy2.robjects.numpy2ri as np2ri
from rpy2.robjects.packages import importr
srl = importr('scoringRules')

ob_file = "/home/manuel/Dokumente/Studium/Karlsruhe/1516WS/Praktikum/ensembleScore/Input/Observation/ECMWF_20131001-31date_06int_uv10m_wind_MSLP_ECMWF_analysis.nc"
fc_file = "/home/manuel/Dokumente/Studium/Karlsruhe/1516WS/Praktikum/ensembleScore/Input/Forecast/ECMWF_okt2013/EPS_uv10m_MSLP_6h_5day_20131001.nc"

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

# Compute Scores
N = obs_vec.shape[1]
escr = 0
vscr = 0
for i in range(0,N - 1):
    ## Part which (more or less) could be put into a wrapper around the functions ###
    # - convert to rpy2 format
    y_vec = rpy2.robjects.FloatVector(obs_vec[:,i])
    dat_mat = np2ri.py2ri(forc_vec[:,:,i])
    # - calculate scores
    escr = escr + srl.es_sample(y_vec, dat_mat)[0]
    vscr = vscr + srl.vs_sample(y_vec, dat_mat)[0]
    ### ------------------------------------------------------------------------- ###
vscr = vscr/N
escr = escr/N
print('Energy Score')
print(escr)
print('Variogram Score')
print(vscr)
