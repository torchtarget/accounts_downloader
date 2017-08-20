import expensipy

# These are not your normal Expensify login credentials. You can find your
# 'integration' credentials by visiting https://www.expensify.com/tools/integrations/
# while logged in.
userid = "aa_chris_torchtarget_com"
secret = "5f2c536027b26eb81e9f2c950bc52e0bed141459"

ex = expensipy.Expensify(userid, secret)
reports = ex.reports("New Report")
print(reports)
#report=reports
#print("Report %s has %s transactdions:" % ( len(report['transactions'])))
print("Length coming")
print(len(reports))
for report in reports:
    print(report)
    myreport=(reports[report])
    print(myreport['name'])
    mytransactions=myreport['transactions']
    print(len(mytransactions))
    print(mytransactions[0])
    for transaction in mytransactions:
        print(" * %2.2f %s at merchant %s" % (transaction['amount'] / 100.0,
                                              transaction['currency'], transaction['merchant']))
    
    #print("Report %s has %s transactions:" % (report['name']))
    #print((report['transactions']))
    #for transaction in report['transactions']:
     #   print(" * %2.2f %s at merchant %s" % (transaction['amount'] / 100.0,
      #      transaction['currency'], transaction['merchant']))


   