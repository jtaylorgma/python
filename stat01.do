********************************************************************************
*Program: stat01.do
*Project: Python Training
*Author: Josh Taylor, Greylock McKinnnon Associates
*Last Edited: 6/17/15
********************************************************************************
capture log close
log using "C:\Users\jtaylor\Projects\Training\Python\Code\Log\stat01Log.smcl", append
set more off 
cd "C:\Users\jtaylor\Projects\Training\Python\Charts and Tables"

timer clear

import delimited C:\Users\jtaylor\Projects\Training\Python\Data\ds_test_final.txt, clear 
gen black = rac1p == 2
gen otherRace = rac1p > 2
gen male = sex == 1
replace dis = 0 if dis == 2
replace hicov = 0 if hicov == 2
replace fs = 0 if fs == 2
replace hincp = 1 if hincp < 1
gen logIncome = log(hincp)


timer on 1
reg logIncome agep dis wif fs noc pap black otherRace male wkhp i.st
timer off 1
qui timer list
local time1 = r(t1)
outreg2 using "Stata, Income OLS.rtf", replace ctitle("OLS", "`time1' S") ///
		keep(agep dis wif fs noc pap black otherRace male wkhp)

 
timer on 2
reg logIncome agep dis wif fs noc pap black otherRace male wkhp i.st, robust
timer off 2
qui timer list
local time2 = r(t2)
outreg2 using "Stata, Income OLS.rtf",  ctitle("OLS, Robust SE", "`time2' S") ///
			keep(agep dis wif fs noc pap black otherRace male wkhp)

timer on 3
logit hicov agep dis fs black otherRace male hincp
timer off 3
qui timer list
local time3 = r(t3)
outreg2 using "Stata, Insure Logit.rtf", replace ctitle("Logit", "`time3' s")



log close














log close
