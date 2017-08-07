# -*- coding: utf-8 -*-
"""
Interface for some functionality of the R-package scoringRules.
It computes univariate and multivariate scores of the form *S(y, dat)*, 
where *S* is a proper scoring rule, *y* is a *d*-dimensional realization vector 
and *dat* is a simulated sample of forecasts. Available are the continuous
ranked probability score (CRPS), energy score and variogram score of order *p*.

"""

import numpy as np
import rpy2
import rpy2.robjects.numpy2ri as np2ri
from rpy2.robjects.packages import importr
srl = importr('scoringRules') 

def es_sample(y, dat):
    """Sample Energy Score

    Compute the energy score ES(*y*, *dat*), where *y* is a vector of a
    *d*-dimensional observation and dat is a multivariate ensemble
    forecast. 
    For details, see Gneiting, T., Stanberry, L.I., Grimit, E.P.,
    Held, L. and Johnson, N.A. (2008). Assessing probabilistic forecasts of 
    multivariate quantities, with an application to ensemble predictions of 
    surface winds. Test, 17, 211–235.

    Args:
        *y* (np.array): Realized values (numeric vector of length *d*).
        
        *dat* (np.array): Forecast sample of shape (*d*, *m*), where 
        *d* is the dimension of the realization and 
        *m* the number of sample members. Each of the *m* columns corresponds 
        to the *d*-dimensional forecast of one ensemble member.

    Returns:
        float: Energy score of the forecast-observation pair.

    """
    try:
        y = np.array(y)
        dat = np.array(dat)
        y_r = rpy2.robjects.FloatVector(y)
        dat_r = np2ri.py2ri(dat)
    except Exception:
        print('Input has wrong format.')
        
    return srl.es_sample(y_r, dat_r)[0]
    
def es_sample_vec(y_arr, dat_arr):
    """Sample Energy Score; vectorized version

    Compute the energy score ES(*y_arr*, *dat_arr*), where *y_arr* is a series of 
    *d*-dimensional observations and *dat_arr* is a series of 
    samples of multivariate forecasts.
    For details, see Gneiting, T., Stanberry, L.I., Grimit, E.P.,
    Held, L. and Johnson, N.A. (2008). Assessing probabilistic forecasts of 
    multivariate quantities, with an application to ensemble predictions of 
    surface winds. Test, 17, 211-235.

    Args:
        *y_arr* (np.array): Series of observations of 
        shape (*d*, *n*), where *d* is the dimension of the observations,
        and *n* the number of observation. Hence each column contains a single 
        *d*-dimensional realization.
        
        *dat_arr* (np.array): Forecast sample  
        of shape (*d*, *m*, *n*), where
        *d* is the dimension of the realized values, *m* the number of 
        samples, and *n* the number of realizations.

    Returns:
        np.array: Energy score of each forecast-observation pair.

    """
    try:
        y_arr = np.array(y_arr)
        y_arr = np.expand_dims(y_arr, 1)
        dat_arr = np.array(dat_arr)
    except Exception:
        print('Input has wrong format.')
    else:
        if (len(y_arr.shape) != 3 
            or len(dat_arr.shape) != 3
            or y_arr.shape[0] != dat_arr.shape[0]
            or y_arr.shape[2] != dat_arr.shape[2]
        ):
            raise ValueError('Parameters have wrong dimension.')

    df = np.concatenate((y_arr,dat_arr),axis = 1)
    df_r = np2ri.py2ri(df)
    rpy2.robjects.globalenv['df'] =  df_r
    
    escr_r = rpy2.robjects.r('apply(df, c(3), function(x) es_sample(x[,1], x[,-1]))')
    return np.array(escr_r)    
    
def vs_sample(y, dat, w=None, p=0.5):
    """Sample Variogram Score

    Compute the variogram score VS(*y*, *dat*) of order *p*, where *y* is a 
    *d*-dimensional observation and dat is a multivariate ensemble
    forecast. 
    For details, see Scheuerer, M. and Hamill, T.M. (2015). Variogram-based 
    proper scoring rules for probabilistic forecasts of multivariate quantities. 
    Monthly Weather Review, 143, 1321-1334.

    Args:
        *y* (np.array): Observation (numeric vector of length *d*).
        
        *dat* (np.array): Forecast sample of shape (*d*, *m*), where 
        *d* is the dimension of the realization and 
        *m* the number of sample members.
        
        *p* (float): Order of variogram score. Standard choices include *p* = 1 and
        *p* = 0.5 (default).
        
        *w* (np.array):  Numeric array of weights for *dat* used in the variogram
          score.  If no weights are specified, constant weights with *w*
          = 1 are used.


    Returns:
        float: Variogram score of the forecast-observation pair.

    """

    try:
        y = np.array(y)
        dat = np.array(dat)
        if w is None :
            w_r = rpy2.robjects.NULL
        else:
            w = np.array(w)
            w_r = np2ri.py2ri(w)
        p_r = float(p)
        y_r = rpy2.robjects.FloatVector(y)
        dat_r = np2ri.py2ri(dat)
    except Exception:
        print('Input has wrong format.')
    
    return srl.vs_sample(y = y_r, dat = dat_r, w = w_r, p = p_r)[0]

def vs_sample_vec(y_arr, dat_arr, w=None, p=0.5):
    """Sample Variogram Score; vectorized version

    Compute the variogram score VS(*y_arr*, *dat_arr*), where *y_arr* is a series of 
    *d*-dimensional observations and *dat_arr* is a series of 
    samples of multivariate forecasts.
    For details, see Scheuerer, M. and Hamill, T.M. (2015). Variogram-based 
    proper scoring rules for probabilistic forecasts of multivariate quantities. 
    Monthly Weather Review, 143, 1321-1334.

    Args:
        *y_arr* (np.array): Series of observations of 
        shape (*d*, *n*), where *d* is the dimension of the observations,
        and *n* the number of observation. Hence each column contains a single 
        *d*-dimensional realization.
        
        *dat_arr* (np.array): Forecast sample  
        of shape (*d*, *m*, *n*), where
        *d* is the dimension of the realized values, *m* the number of 
        samples, and *n* the number of realizations.
        
        *p* (float): Order of variogram score. Standard choices include *p* = 1 and
        *p* = 0.5 (default).
        
        *w* (np.array):  Numeric array of weights for *dat* used in the variogram
          score.  If no weights are specified, constant weights with *w*
          = 1 are used.

    Returns:
        *np.array*: Variogram score of each forecast-observation pair.

    """
    try:
        y_arr = np.array(y_arr)
        y_arr = np.expand_dims(y_arr, 1)
        dat_arr = np.array(dat_arr)
        p_r = float(p)
        if w is None :
            w_r = rpy2.robjects.NULL
        else:
            w = np.array(w)
            w_r = np2ri.py2ri(w)
    except Exception:
        print('Input has wrong format.')
    else:
        if (len(y_arr.shape) != 3
            or len(dat_arr.shape) != 3
            or y_arr.shape[0] != dat_arr.shape[0]
            or y_arr.shape[2] != dat_arr.shape[2]
        ):
            raise ValueError('Parameters have wrong dimension.')

    df = np.concatenate((y_arr,dat_arr),axis = 1)
    df_r = np2ri.py2ri(df)
    rpy2.robjects.globalenv['df'] =  df_r
    rpy2.robjects.globalenv['p'] =  p_r
    rpy2.robjects.globalenv['w'] =  w_r
    
    vscr_r = rpy2.robjects.r('apply(df, c(3), function(x) vs_sample(x[,1], x[,-1], w, p))')
    return np.array(vscr_r)
    
def crps_sample(y, dat):
    """Sample Continuous Ranked Probability Score (CRPS)

    Compute CRPS(*y*, *dat*), where *y* is a univariate
    observation and *dat* is an ensemble forecasts.
    For details, see Matheson, J.E. and Winkler, R.L. (1976). Scoring rules for
    continuous probability distributions. Management Science, 22, 1087-1096.
    
    Args:
        *y* (float): Observation.
        
        *dat* (np.array): Forecast ensemble of length *m*, where 
        *m* is the number of members.

    Returns:
        float: CRPS of the forecast-observation pair.

    """

    try:
        y_r = float(y)
        dat = np.array(dat)
        dat_r = rpy2.robjects.FloatVector(dat)
    except Exception:
        print('Input has wrong format.')
        
    return srl.crps_sample(y_r, dat_r)[0]
    
def crps_sample_vec(y_arr, dat_arr):
    """Sample Continuous Ranked Probability Score (CRPS); vectorized version

    Compute CRPS(*y_arr*, *dat_arr*), where *y_arr* is a series of 
    univariate observations and *dat_arr* is a series of
    ensemble forecasts.
    For details, see Matheson, J.E. and Winkler, R.L. (1976). Scoring rules for
    continuous probability distributions. Management Science, 22, 1087-1096.

    Args:
        *y_arr* (np.array): Series of observations of 
        length *n*, where *n* is the number of observations. 
        
        *dat_arr* (np.array): Ensemble forecasts  
        of shape (*m*, *n*), where *m* is the number of ensemble members, 
        and *n* the number of observation.

    Returns:
        np.array: CRPS of each forecast-observation pair.

    """
    try:
        y_arr = np.array(y_arr)
        dat_arr = np.array(dat_arr)
        y_r = rpy2.robjects.FloatVector(y_arr)
        dat_r = np2ri.py2ri(dat_arr)
    except Exception:
        print('Input has wrong format.')
    else:
        if (len(y_arr.shape) != 1 
            or len(dat_arr.shape) != 2 
            or y_arr.shape[0] != dat_arr.shape[1]
        ):
            raise ValueError('Parameters have wrong dimension.')

    rpy2.robjects.globalenv['obs'] =  y_r
    rpy2.robjects.globalenv['forc'] =  dat_r
    
    crps_r = rpy2.robjects.r('apply(rbind(obs,forc), 2, function(x) crps_sample(x[1], x[-1]))')
    return np.array(crps_r)