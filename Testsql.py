import sqlite3
from configobj import ConfigObj


bank_config = ConfigObj("banks_config.ini")
sqlite_file = bank_config['sqlite_file']
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()


def setup_database():
    table_name = 'Transactions'
    c.execute('''
        CREATE TABLE transactions(id INTEGER PRIMARY KEY, bank_account TEXT,
                                date DATE, amount FLOAT, counterparty TEXT,
                                description TEXT, category TEXT)
                                ''')
    conn.commit()


def insert_transaction(transaction):
    print(transaction)
    c.execute('''
            INSERT INTO transactions(bank_account,date,amount,counterparty,description,category)
            VALUES (?,?,?,?,?,?)''', (transaction))
    print(c.lastrowid)
    conn.commit()


#setup_database()
insert_transaction(("HSBC", 5, 100, "Me", "toolate", "Salesteam"))
