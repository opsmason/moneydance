# Program to display the current progress within specific budget categories
# Will report month-to-date and year-to-date.
# Author: Mason Turner, 2012
# Special thanks to Ric Werme for his networth.py at http://moneydance.com/dev/RM-NetWorth/networth.py

# Configuration variables, ** set these before you run this program. **

watchCategories = ( 'Miscellaneous:Mason' , 'Miscellaneous:Miriam' , 'Groceries' )

# This program doesn't have ready access to displaying data on screen, so
# we create text and HTML files.
textfile = '/tmp/allowance.txt'
htmlfile = '/tmp/allowance.html'

# Set verbose to 1 to enable some diagnostic printing.
verbose = 0

# [End of configuration variables.]

import time
from java.util import Vector
from java.util import Date

# Inspired by http://code.activestate.com/recipes/476197-first-last-day-of-the-month/
# Moneydance Python doesn't have the calendar plugin, so we have to fake it
# We can always add 31 days to the first day of this month to find a day in next month
# We then renormalize to the first of next month, and then subtract one second to find
# the last day of this month.
def mkLastOfMonth(inTime):
    dTime         = time.localtime(inTime)
    first         = time.mktime((dTime[0],dTime[1],1,0,0,0)) # What is the first of the current month?
    nextFirst     = first + (60*60*24*31)                    # Add 31 days to this first of this month to get a day from next month
    nTime         = time.localtime(nextFirst)
    realNextFirst = time.mktime((nTime[0],nTime[1],1,0,0,0)) # What is the real first day of next month
    theLastDay    = realNextFirst - 1                        # One second before that time is the last second of this month
    return theLastDay

# Let's generate the date strings for range we care about: this month and this year
now = time.time()
lt = time.localtime(now)

startOfMonth = int(time.mktime((lt[0],lt[1],1,0,0,0)))
endOfMonth   = int(mkLastOfMonth(now))
sM = time.localtime(startOfMonth)
sMf = int('%04d%02d%02d' % (sM[0] , sM[1] , sM[2] ))
eM = time.localtime(endOfMonth)
eMf = int('%04d%02d%02d' % (eM[0] , eM[1] , eM[2] ))

startOfYear = time.mktime((lt[0],1,1,0,0,0))
endOfYear   = time.mktime((lt[0],12,31,0,0,0))
sY = time.localtime(startOfYear)
sYf = int('%04d%02d%02d' % (sY[0] , sY[1] , sY[2] ))
eY = time.localtime(endOfYear)
eYf = int('%04d%02d%02d' % (eY[0] , eY[1] , eY[2] ))

rootAccount   = moneydance.getRootAccount()
budgets       = rootAccount.getBudgetList()  
currentBudget = budgets.findCurrentBudget()

monthCal = currentBudget.calculate(sMf , eMf , 0, 0)
yearCal  = currentBudget.calculate(sYf , eYf , 0, 0)

fo = open(textfile, 'w')

fo.write( "\n# %-28s %8s   %8s   %8s\n" % ('Month To Date' , 'Budget' , 'Actual' , 'Delta') )
for i in monthCal.getItemList():
  cat = ':'.join(i.getCategory().getAllAccountNames())
  b = i.getBudgetedAmounts()[0] / 100
  a = i.getActualAmounts()[0] / 100
  r = b - a
  if cat in watchCategories:
  	fo.write( "%-30s %8.2f - %8.2f = %8.2f\n" % (cat , b , a , r))

fo.write( "\n# %-28s %8s   %8s   %8s\n" % ('Year To Date' , 'Budget' , 'Actual' , 'Delta') )
for i in yearCal.getItemList():
  cat = ':'.join(i.getCategory().getAllAccountNames())
  b = i.getBudgetedAmounts()[0] / 100
  a = i.getActualAmounts()[0] / 100
  r = b - a
  if cat in watchCategories:
  	fo.write( "%-30s %8.2f - %8.2f = %8.2f\n" % (cat , b , a , r))

fo.close()
