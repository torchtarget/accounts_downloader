##! /usr/bin/python3
import HSBC.HSBCScraper
from configobj import ConfigObj
from selenium import webdriver
import George.GeorgeScrapper
import ICS.ICSScraper
import sql_transactions
# import Santander.SantanderOpen

from forex_python.converter import CurrencyRates

# date and time representation

bank_config = ConfigObj("banks_config.ini")
saldo_file = bank_config['saldo_file']
sqlite_file = bank_config['sqlite_file']
no_days_trans = 4


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
    saldo_euro = 1
    with open(saldo_file, "a") as output_file:
        output_file.write(account_saldo["bank"]+","+account_saldo["saldo"]+","+account_saldo["currency"]+","+str(saldo_euro)+"\n")
    return


santander_open = False
c = CurrencyRates()

bank_info = get_bank_info('ICS')
ics = ICS.ICSScraper.ICSBank(bank_info)
ics_saldo = ics.get_Saldo()
output_saldo(ics_saldo)
print(ics_saldo)
browser = webdriver.Firefox()
bank_info = get_bank_info('George')
print(bank_info)
george = George.GeorgeScrapper.GeorgeAccount(browser, bank_info)
trans_db = sql_transactions.Accounts_SQL(sqlite_file)


if (george.opensite()):
    i = 0
    while(i < bank_info['no_accounts']):
        mysaldo = george.get_Saldo(i)
        print(mysaldo)
        output_saldo(mysaldo)
        trans_list = george.get_transactions(no_days_trans, i)
        for trans in trans_list:
            if(trans_db.match_transaction(trans) is False):
                print("Transaction not matched _ inserting")
                trans_db.insert_transaction(trans)
            else:
                print("Transaction Matched")
        i = i+1
browser.quit()


#with open(saldo_file, "w") as output_file:
#        output_file.write("Report: " + time.strftime("%c")+"\n")

#santander_open=Santander.SantanderOpen.opensite(browser)
#if(santander_open):
#     mysaldo=Santander.SantanderOpen.get_Saldo(browser,0)
#     output_saldo(mysaldo)

#george_open = George.GeorgeScrapper.opensite(browser)
