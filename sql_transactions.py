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
                                date DATE, amount REAL, counterparty TEXT,
                                description TEXT, category TEXT, FX_curr TEXT, FX_rate REAL, inGC BOOLEAN, matched BOOLEAN)
                                ''')
        self.conn.commit()

    def insert_transaction(self, transaction):
        """Insert a banking transaction into the database."""
        self.cur.execute('''
                        INSERT INTO transactions(bank_account,date,amount,counterparty,description,category,FX_curr,FX_rate,inGC,matched)
                        VALUES (?,?,?,?,?,?,?,?,?,?)''', (transaction))
        print(self.cur.lastrowid)
        self.conn.commit()

    def match_transaction(self, transaction):
        """Match a transaction to the database."""
        cursor.execute('''
                      SELECT COUNT(*) FROM transactions WHERE
                      bank_account =? AND date = ?

mydb = Accounts_SQL("accounts2.sql")
# mydb.setup_database()
#  mydb.insert_transaction(("HSBC", 5, 100, "Me", "toolate", "Salesteam","EUR", 1.0, False, False))

(number_of_rows,)=cursor.fetchone()
