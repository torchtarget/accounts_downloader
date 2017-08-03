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
                                date DATE, amount FLOAT, counterparty TEXT,
                                description TEXT, category TEXT)
                                ''')
        self.conn.commit()


    def insert_transaction(self,transaction):
        print(transaction)
        self.cur.execute('''
                INSERT INTO transactions(bank_account,date,amount,counterparty,description,category)
                VALUES (?,?,?,?,?,?)''', (transaction))
        print(self.cur.lastrowid)
        self.conn.commit()



# mydb = Accounts_SQL("accounts.sql")
#m ydb.insert_transaction(("HSBC", 5, 100, "Me", "toolate", "Salesteam"))
