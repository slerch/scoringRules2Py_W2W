# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import readline
import rpy2.robjects as robjects

robjects.r
print(robjects.r)

pi = robjects.r.pi
letters = robjects.r.letters

plot = robjects.r.plot
dir = robjects.r.dir

print(robjects.r('1+2'))
sqr = robjects.r('function(x) x^2')

print(sqr(2))

x = robjects.r.rnorm(100)
robjects.r('hist(%s, xlab="x", main="hist(x)")' %x.r_repr())

from rpy2.robjects.packages import importr

base = importr('base')
stats = importr('stats')
graphics = importr('graphics')

scoringRules = importr('scoringRules')
crps = scoringRules.crps
print(crps(2, family = "normal", mean = 0, sd = 1))