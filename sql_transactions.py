"""Manage the interaction with the database."""
import sqlite3


class Accounts_SQL:
    """Manage the accounts transactions."""

    def __init__(self, sqlite_file):
        """Open Connection to the file."""
        self.conn = sqlite3.connect(sqlite_file)
        self.cur = self.conn.cursor()

    def setup_database(self):
        """Create the database file with one table."""
        self.cur.execute('''
        CREATE TABLE transactions(id INTEGER PRIMARY KEY, bank_account TEXT,
                                trans_date DATE, amount REAL, counterparty TEXT,
                                description TEXT, memo TEXT, category TEXT, FX_curr TEXT, FX_rate REAL, inGC BOOLEAN, matched BOOLEAN)
                                ''')
        self.conn.commit()

    def insert_transaction(self, transaction):
        """Insert a banking transaction into the database."""
        self.cur.execute('''
                        INSERT INTO transactions(bank_account,trans_date,amount,counterparty,description,memo,category,FX_curr,FX_rate,inGC,matched)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (transaction))
        print(self.cur.lastrowid)
        self.conn.commit()

    def match_transaction(self, transaction):
        """Match a transaction to the database based on Bank_account, Transaction date, ammount, counterpary and description and returns No. of Matches."""
        self.cur.execute('''
                      SELECT COUNT(*) FROM transactions WHERE
                      bank_account = ? AND trans_date = ? AND
                      amount = ? AND counterparty = ? AND description = ? ''', (transaction[0], transaction[1], transaction[2], transaction[3], transaction[4]))
        if(self.cur.fetchone()[0] > 0):
            match_bol = True
        else:
            match_bol = False
        return(match_bol)


#mydb = Accounts_SQL("accounts.sqlite3")
#ydb.setup_database()
# mydb.insert_transaction(("HSBC", 5, 100, "Me", "toolate", "Salesteam", "EUR", 1.0, False, False))
# result = mydb.match_transaction(("HSBC", 5, 100, "Me", "toolate", "Salesteam", "EUR", 1.0, False, False))
# print(result)
# result = mydb.match_transaction(("HSBC", 5, 100, "MeToo", "toolate", "Salesteam", "EUR", 1.0, False, False))
# print(result)
# (number_of_rows,)=cursor.fetchone()
