"""Automatically instert transactions into the db."""
from accounts_downloader import sql_transactions as sqlt
import piecash as PC
from configobj import ConfigObj


#book=PC.open_book("C:/tmp/GnuTest.gnucash")

for transaction in sqlt.Transaction.select():
    print("Hello")
    print(transaction.inGC)
