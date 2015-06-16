########################################################################################################################
# Program: stat01.py
# Project: Python Training
# Author: Josh Taylor, Greylock Mckinnon Associates
# Last Edited: 6/16/15
########################################################################################################################

from __future__ import division
import pandas as pd
import numpy as np
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import timeit


#path to this file: "C:\Users\jtaylor\Projects\Training\Python\Code\stat01.py"


# Import census data
pums = pd.read_table("C:\Users\jtaylor\Projects\Training\Python\Data\ds_test_final.txt")

#clean the data
pums['twoWorkers'] = (pums['fes'] == 1) + 0
pums['black'] = (pums['rac1p'] == 2) + 0
pums['otherRace'] = (pums['rac1p'] > 2) + 0
pums['male'] = (pums['sex'] == 1) + 0
pums['dis'].replace(2,0,inplace = True)
pums['hicov'].replace(2,0,inplace = True)
pums['fs'].replace(2,0, inplace = True)
for i in range(len(pums['hincp'])):
    if pums.loc[i,'hincp'] < 1 or pums.loc[i,'hincp'] == np.nan:
        pums.loc[i, 'hincp'] = 1


#create a linear model that describes logIncome
pums['logIncome'] = np.log(pums['hincp'])

startOLS = timeit.default_timer()
incomeOLS = sm.ols(formula = 'logIncome ~ agep + dis + wif + C(st) + fs + noc +  pap + black + otherRace + male + wkhp',
                data = pums, missing='drop').fit()
stopOLS = timeit.default_timer()
timeOLS = stopOLS - startOLS
print "Run time to fit this model: %s" % timeOLS
incomeOLS.summary()


#Create a logit model that describes the likelihood of being insured
print
print "Testing out the logit function in python"
print
startLogit = timeit.default_timer()
insureLogit = sm.logit(formula = 'hicov ~ agep + dis + fs + black + otherRace + male  + hincp',
                       data=pums, missing='drop').fit()
stopLogit = timeit.default_timer()
print "Run time to fit this model is: %s" % (stopLogit - startLogit)
insureLogit.summary()


