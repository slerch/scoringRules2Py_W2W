# scoringRules2Py_W2W

Python interface for the scoringRules R package (https://github.com/FK83/scoringRules) for use within the 'Ensemble Tools' cross-cutting activity within the Transregional Collaborative Research Center 'Waves to Weather' (http://wavestoweather.de).

## Basic system requirements and installation: 
 * R 3.2+ (https://www.r-project.org/)
 * R-package scoringRules (version 0.9.2+), e.g. via calling `install.packages("scoringRules")` within R. 
 * Python 3.5+
 * Python-package rpy2, e.g. https://rpy2.bitbucket.io/ or via `pip3 install rpy2` (If installation of rpy2 fails try reinstalling R)

## Optional requirements
 * netCDF4 and Python-package netCDF4
 * Python-package xarray

## History:
August 2017: main code and documentation
July 2017: initial commits
June 2017: repository created