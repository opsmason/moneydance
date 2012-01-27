# Program to display the current progress within specific budget categories
# Will report month-to-date and year-to-date.
# Author: Mason Turner, 2012
# Special thanks to Ric Werme for his networth.py at http://moneydance.com/dev/RM-NetWorth/networth.py

# Configuration variables, ** set these before you run this program. **

watch = [ 'Miscellaneous:Mason' , 'Miscellaneous:Miriam' , 'Groceries' ]

# This program doesn't have ready access to displaying data on screen, so
# we create text and HTML files.
textfile = '/tmp/allowance.txt'
htmlfile = '/tmp/allowance.html'

# Set verbose to 1 to enable some diagnostic printing.
verbose = 0

# [End of configuration variables.]

import time

# As the program scans each account computing net worth at the requested
# dates, it creates an account record for each.  Later it sorts and
# scans the records times to determine which accounts to print
# and to print the data.  Fields are:
#   .id: ID # for the account.  Not really needed.
#   .type: The accountType, used to summarize each type.  Not really needed.
#   .name: The name for the account or subaccount. _Not_ a multilevel name!
#   .subaccount: True (1) if this has a parent.
#   .printflag: True if we need to print (subaccount with a non-zero value
#               or parent of such a subaccount).
#   .values: List of values (in local currency) matching dates of interest.
# Records are kept in the accountRecs dictionary which is indexed by the
# full account name.
class accountRec:
    def __init__(self, id, name, type, subaccount):
        self.id = id
        self.name = name
        self.type = type
        self.subaccount = subaccount
        self.printflag = 0
        self.values = []

# Routine to scan accountRecs and decide what to print.  That is any
# subaccount with a non-zero value for some reporting data and its
# parent, plus any top level account with a non zero balance.
def checkPrint(accountRecs):
    keys = accountRecs.keys()
    keys.sort()
    for i in keys:
        rec = accountRecs[i]
        for value in rec.values:
            if value:
                rec.printflag = 1
                break
        if not rec.subaccount:	# Parent acct precedes subaccts
            parent = rec
        else:
            if rec.printflag:
                parent.printflag = 1

# Call this to make a text file of transactions.  The HTML file looks
# better.
def maketext(file, datestr, accountRecs, typeWorth, netWorth):
    fo = open(file, 'w')
    pass # First, we print the worth of each account for each date:
    fo.write('Type        Account                                 ')
    for date in datestr:
        fo.write(' %11s' % date)
    fo.write('\n')
    keys = accountRecs.keys()
    keys.sort()
    for key in keys:
        rec = accountRecs[key]
        if not rec.printflag:
            continue
        if rec.subaccount: tmp = '+'
        else: tmp = ''
        fo.write('%-11s %-40s' % (rec.type, tmp + rec.name))
        for val in rec.values:
            fo.write(' %11.2f' % (val / 100.0))
        fo.write('\n')
    pass # Next we print the worth of each account type for each date:
    fo.write('\nType       ')
    for date in datestr:
        fo.write(' %11s' % date)
    fo.write('\n')
    keys = typeWorth.keys()
    keys.sort()
    for key in keys:
        data = typeWorth[key]
        fo.write('%-11s' % key)
        for val in data:
            fo.write(' %11.2f' % (val / 100.0))
        fo.write('\n')
    pass # Finally we print the net worth for each date:
    fo.write('-----------')
    for val in netWorth:
        fo.write(' -----------')
    fo.write('\nTotal      ')
    for val in netWorth:
        fo.write(' %11.2f' % (val / 100.0))
    fo.write('\n')
    fo.close()

# HTML support routines for makehtml():

# Routine to display one cell of simple data.
def easy_cell(fo, val):
    if val == None: val = '&nbsp;'
    fo.write('  <td align=left>%s</td>\n' % val)

# Routine to display one cell of numeric data.
def easy_number(fo, fmt, val):
    if not val:
        fo.write('  <td>&nbsp;</td>\n')
    else:
        fo.write('  <td>%s</td>\n' % (fmt % val))

# Routine to create a HTML file with a table of each security.  Call with
# filename to create and the transactions dictionary.
def makehtml(file, datestr, accountRecs, typeWorth, netWorth):
    fo = open(file, 'w')
    fo.write('''<HTML>\n<HEAD>\n<TITLE>Net Worth</TITLE>\n</HEAD>\n''')
    fo.write('''<BODY">\n\n''')
    fo.write('''<center><font size=+3>Net Worth</font></center>\n''')
    pass # First, we print the worth of each account for each date:
    fo.write('''<p>\n<table border="1" bordercolordark="#000000" bordercolorlight="#000000" cellpadding=2 cellspacing=2>\n''')
    fo.write(''' <tr bgcolor="#e0e0e0">\n  <th>Type</th>\n  <th>Account</th>\n''')
    for date in datestr:
        fo.write('  <th>%s</th>\n' % date)
    fo.write(' </tr>\n')
    bgcolor = ("#b0ffb0", "#e0e0e0") # To alternate backgrounds
    bgselect = 1
    keys = accountRecs.keys()
    keys.sort()
    for key in keys:
        rec = accountRecs[key]
        if not rec.printflag:
            continue
        if not rec.subaccount:
            bgselect = not bgselect
        fo.write(' <tr bgcolor="%s" align=right>\n' % bgcolor[bgselect])
        easy_number(fo, '%-11s', rec.type)
        if rec.subaccount:
            easy_cell(fo, rec.name)
        else:
            easy_cell(fo, '<b>%s</b>' % rec.name)
        for val in rec.values:
            easy_number(fo, '%10.2f', val / 100.0)
        fo.write(' </tr>\n')
    fo.write('</table>\n\n')
    pass # Next we print the worth of each account type for each date:
    fo.write('<p>\n<table border="1" bordercolordark="#000000" bordercolorlight="#000000" cellpadding=2 cellspacing=2>\n')
    fo.write(' <tr bgcolor="#e0e0e0">\n  <th>Type</th>\n')
    for date in datestr:
        fo.write('  <th>%s</th>\n' % date)
    fo.write(' </tr>\n')
    bgselect = 0
    keys = typeWorth.keys()
    keys.sort()
    for key in keys:
        data = typeWorth[key]
        fo.write(' <tr bgcolor="%s" align=right>\n' % bgcolor[bgselect])
        bgselect = not bgselect
        easy_cell(fo, key)
        for val in data:
            easy_number(fo, '%10.2f', val / 100.0)
        fo.write(' </tr>\n')
    fo.write(' <tr></tr>\n <tr bgcolor="%s" align=right>\n' % bgcolor[bgselect])
    pass # Finally we print the net worth for each date:
    easy_cell(fo, 'Total')
    for val in netWorth:
        easy_number(fo, '%10.2f', val / 100.0)
    fo.write(' </tr>\n</table>\n\n')
    lt = time.localtime(time.time())
    date = '%d-%02d-%02d' % (lt[0], lt[1], lt[2])
    fo.write('''\n<p>Page generated on %s.\n\n</BODY>\n</HTML>\n''' % date)
    fo.close()

# Return a list of account balances for an account for a list of requested
# dates.  We have to scan all transactions for the account which we get as an
# unsorted list.  We derive a list of changes in the account from one date to
# the next to the current balance.  Each transacation is matched with the
# appropriate time period and its value is accumulated as a change that will
# let use quickly compute the balances just before we return the list of
# balances.
# Key local variables:
#  lv:       Local Verbose value, set to 1 or 2 for debugging.
#  deltas:   Amounts account changed between dates of interest.
#  balances: Dollar balances of account on dates of interest.
#  indexes:  List of indexes to access latest date of interest to earliest.
def acctValues(rootAccount, account, dates):
    lv = 0
    txnEnum = rootAccount.getTransactionSet().getTransactionsForAccount(account)
    txns = txnEnum.getAllTxns()
    deltas = []
    balances = []
    for i in dates:
        deltas.append(0L)
        balances.append(0L)
    indexes = range(len(dates))
    indexes.reverse()
    for txn in txns:
        date = txn.getDate()
        if date < dates[0]:	# Earlier than earliest date of interest?
            if lv > 1: print 'skipping', date
            continue
        if lv > 1: print repr(txn)
        for dateIndex in indexes:
            if date > dates[dateIndex]:
                break
        deltas[dateIndex] = deltas[dateIndex] + txn.getValue()
        if lv > 1: print 'txn counted in', date, dateIndex, deltas[dateIndex]
    balances[indexes[0]] = account.getBalance() - deltas[indexes[0]]
    for dateIndex in indexes[1:]:
        balances[dateIndex] = balances[dateIndex + 1] - deltas[dateIndex]
    if lv: print 'deltas:', deltas, 'balances', balances
    for dateIndex in indexes:
        if account.getAccountType() == account.ACCOUNT_TYPE_SECURITY:
            currencytype = account.getCurrencyType()
            rate = currencytype.getRawRateByDate(dates[dateIndex])
            balances[dateIndex] = long(round(balances[dateIndex] / rate))
            if lv > 1: print 'Value for', dates[dateIndex], 'is', balances[dateIndex]
    return balances

# Main routine.
# After some initialization, we scan each account that has a worth
# associated with it (any but deleted, expense, or income), call
# acctValues to get the balances we want, and accumulate the data in the
# account type and overall net worth lists.  Then, since I don't know if
# there's a way to call swing, generate new files for viewing and
# printing.
def doit(datestr, dates):
    rootAccount = moneydance.getRootAccount()
    if verbose:
        print 'Looking through %d accounts\n' % rootAccount.getHighestAccountNum()
    typeWorth = {}
    aTNames = {}
    aTNames[rootAccount.ACCOUNT_TYPE_ASSET] = 'Asset'
    aTNames[rootAccount.ACCOUNT_TYPE_BANK] = 'Bank'
    aTNames[rootAccount.ACCOUNT_TYPE_CREDIT_CARD] = 'Credit card'
    aTNames[rootAccount.ACCOUNT_TYPE_EXPENSE] = 'Expense'
    aTNames[rootAccount.ACCOUNT_TYPE_INCOME] = 'Income'
    aTNames[rootAccount.ACCOUNT_TYPE_INVESTMENT] = 'Investment'
    aTNames[rootAccount.ACCOUNT_TYPE_LIABILITY] = 'Liability'
    aTNames[rootAccount.ACCOUNT_TYPE_LOAN] = 'Loan'
    aTNames[rootAccount.ACCOUNT_TYPE_ROOT] = 'Root'
    aTNames[rootAccount.ACCOUNT_TYPE_SECURITY] = 'Security'
    accountRecs = {}
    zeroes = []
    for i in dates:
        zeroes.append(0L)
    netWorth = zeroes[:]	# Make a copy, there will be several more
    for id in range(1, rootAccount.getHighestAccountNum() + 1):
        account = rootAccount.getAccountById(id)
        if account == None:
            continue
        balance = account.getBalance()
        accountType = account.getAccountType()
        aTName = aTNames[accountType]
        if accountType == account.ACCOUNT_TYPE_EXPENSE or accountType == account.ACCOUNT_TYPE_INCOME:
            continue
        try: tmp = typeWorth[aTName]
        except: typeWorth[aTName] = zeroes[:]
        name = account.getAccountName()
        fullName = account.getFullAccountName()
        subaccount = account.getDepth() > 1
        accountRecs[fullName] = accountRec(id, name, aTName, subaccount)
        values = acctValues(rootAccount, account, dates)
        accountRecs[fullName].values = values[:]
        for dateIndex in range(len(dates)):
            netWorth[dateIndex] = netWorth[dateIndex] + values[dateIndex]
            typeWorth[aTName][dateIndex] = typeWorth[aTName][dateIndex] + values[dateIndex]
        if verbose:
            print '%3d: %-40s %11.2f   %d' % (id, name, values[-1] / 100.0, aTName)
        pass # if len(accountRecs) == 10:	# Early termination?
        pass #    break
    checkPrint(accountRecs)
    maketext(textfile, datestr, accountRecs, typeWorth, netWorth)
    makehtml(htmlfile, datestr, accountRecs, typeWorth, netWorth)
    return

dates = []
td = time.localtime(time.time())
for date in datestr:
    tmp = date.split('-')
    td = (int(tmp[0]), int(tmp[1]), int(tmp[2]), 12, 0, 0, 0, 0, 0)
    dates.append(long(time.mktime(td)) * 1000L)

# print 'datestr', datestr
# print 'dates', dates
doit(datestr, dates)
