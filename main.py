##! /usr/bin/python3
from configobj import ConfigObj
from webdriverwrapper.wrapper import Firefox
# import Santander.SantanderOpen
import os
import George.GeorgeScrapper
import ICS.ICSScraper
import HSBC.HSBCScraper
import sql_transactions as sqlt


from forex_python.converter import CurrencyRates

def setup_bank(bank_name):
    """Create bank objects."""
    no_accounts = int(bank_config['Banks'][bank_name]['Accounts'])
    if no_accounts > 0:
        bank_info = get_bank_info(bank_name)
        print(bank_info)
        if(bank_name == 'George'):
            george = George.GeorgeScrapper.GeorgeAccount(browser, bank_info)
            return(george)
        elif(bank_name == 'HSBC'):
            hsbc = HSBC.HSBCScraper.HSBCAccount(bank_info)
            return(hsbc)
        elif(bank_name == 'ICS'):
            ics = ICS.ICSScraper.ICSAccount(bank_info)
            return(ics)
    return(None)


def get_bank_info(bank_name):
    """Parse Config File and get Bank Data."""
    bank_user = bank_config['Banks'][bank_name]['Username']
    no_accounts = int(bank_config['Banks'][bank_name]['Accounts'])
    try:
        bank_password1 = bank_config['Banks'][bank_name]['Password']
    except:
        pass
    try:
        bank_password1 = bank_config['Banks'][bank_name]['Password1']
    except:
        pass
    try:
        bank_password2 = bank_config['Banks'][bank_name]['Password2']
    except:
        bank_password2 = None
        pass
    return({"user": bank_user, "pass1": bank_password1, "pass2": bank_password2, "no_accounts": no_accounts})


def output_saldo(account_saldo):
    """Output the balances to a file."""
    # saldo_euro= c.convert(account_saldo["currency"], 'EUR', account_saldo["saldo"])
    if os.path.exists(saldo_file):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'  # make a new file if not
    saldo_euro = 1
    with open(saldo_file, append_write) as output_file:
        output_file.write(account_saldo["bank"]+","+account_saldo["saldo"]+","+account_saldo["currency"]+","+str(saldo_euro)+"\n")
    return


bank_config = ConfigObj("banks_config.ini")
saldo_file = bank_config['saldo_file']
sqlite_file = bank_config['sqlite_file']
no_days_trans = 15
sqlt.setdb(sqlite_file)
c = CurrencyRates()
bank_list = []
browser = Firefox()
sqlt.setdb(sqlite_file)
sqlt.db.connect

for bank_name in bank_config['Banks']:
    bank = setup_bank(bank_name)
    if(bank is not None):
        bank_list.append(bank)

for bank in bank_list:
    i = 0
    print(bank.no_accounts)
    bank.opensite()
    while(i < bank.no_accounts):
        account_saldo = bank.get_Saldo(i)
        output_saldo(account_saldo)
        print(account_saldo)
        trans_list = bank.get_transactions(no_days_trans, i)
        for trans in trans_list:
            print(trans)
            if(sqlt.match_transaction(trans) is False):
                print("Transaction not matched _ inserting")
                sqlt.insert_transaction(trans)
            else:
                print("Transaction Matched")
        i = i+1
browser.quit()
quit()
