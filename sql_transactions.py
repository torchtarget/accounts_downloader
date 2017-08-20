"""Manage the interaction with the database."""
import peewee as pw
#from datetime import date

db = pw.SqliteDatabase('accounts.db')


def setdb(db_file):
    global db
    db = pw.SqliteDatabase(db_file)

class Reciepts(pw.Model):  
    amount = pw.FloatField()
    counterparty = pw.CharField()
    description = pw.CharField()
    memo = pw.CharField()
    category = pw.CharField()
    FX_curr = pw.CharField()
    FX_rate = pw.FloatField()
    inGC = pw.BooleanField()
    matched = pw.BooleanField()
    tag=pw.CharField()
    transaction_id=pw.IntegerField()
    
    class Meta:
        """Ensure db connection."""

        database = db

class Transaction(pw.Model):
    """Transaction class for DB access."""

    bank_account = pw.CharField()
    trans_date = pw.DateField()
    amount = pw.FloatField()
    counterparty = pw.CharField()
    description = pw.CharField()
    memo = pw.CharField()
    category = pw.CharField()
    FX_curr = pw.CharField()
    FX_rate = pw.FloatField()
    inGC = pw.BooleanField
    matched = pw.BooleanField

    class Meta:
        """Ensure db connection."""

        database = db


def insert_transaction(trans):
    """Insert a banking transaction into the database."""

    print(trans)
    db_trans = Transaction.create(bank_account=trans[0],
                                  trans_date=trans[1], amount=float(trans[2]),
                                  counterparty=trans[3], description=trans[4],
                                  memo=trans[5], category=trans[6], FX_curr=trans[7],
                                  FX_rate=float(trans[8]), inGC=trans[9], matched=trans[10])
    return(db_trans)


def match_transaction(trans):
    """Match a transaction to the database based on Bank_account, Transaction date, ammount, counterpary and description and returns No. of Matches."""
    query = Transaction.select().where(Transaction.bank_account == trans[0],
                                       Transaction.trans_date == trans[1],
                                       Transaction.amount == trans[2],
                                       Transaction.counterparty == trans[3],
                                       Transaction.description == trans[4])
    if(len(query)) > 0:
        return(True)
    else:
        return(False)



db.connect()
db.create_tables([Reciepts])
# mytrans = ("HSBC", date(1980, 8, 1), 5, "Helo", "toolate", "Salesteam", "test", "EUR", 1.0, False, False)
# print(mytrans(0))
# insert_transaction(mytrans)
# print(match_transaction(mytrans))