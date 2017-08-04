##! /usr/bin/python3
from configobj import ConfigObj
from selenium import webdriver
# import Santander.SantanderOpen
import George.GeorgeScrapper
import sql_transactions

from forex_python.converter import CurrencyRates

# date and time representation
saldo_file = "/tmp/saldo.txt"
bank_config = ConfigObj("banks_config.ini")
sqlite_file = bank_config['sqlite_file']


def get_bank_info(bank_name):
    """Parse Config File and get Bank Data."""
    bank_user = bank_config['Banks'][bank_name]['Username']
    bank_url = bank_config['Banks'][bank_name]['Url']
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
    return({"url": bank_url, "user": bank_user, "pass1": bank_password1, "pass2": bank_password2})


def output_saldo(account_saldo):
    """Output the balances to a file"""
    # saldo_euro= c.convert(account_saldo["currency"], 'EUR', account_saldo["saldo"])
    saldo_euro = 1
    with open(saldo_file, "a") as output_file:
        output_file.write(account_saldo["bank"]+","+account_saldo["saldo"]+","+account_saldo["currency"]+","+str(saldo_euro)+"\n")
    return



santander_open = False
c = CurrencyRates()
browser = webdriver.Firefox()
bank_info = get_bank_info('George')
print(bank_info)
george = George.GeorgeScrapper.GeorgeAccount(browser, bank_info)
trans_db = sql_transactions.Accounts_SQL(sqlite_file)



if (george.opensite()):
    mysaldo = george.get_Saldo(0)
    trans_list = george.get_transactions(4)
    print(mysaldo)
    trans_db.insert_transaction(trans_list[1])



browser.quit()


#with open(saldo_file, "w") as output_file:
#        output_file.write("Report: " + time.strftime("%c")+"\n")

#santander_open=Santander.SantanderOpen.opensite(browser)
#if(santander_open):
#     mysaldo=Santander.SantanderOpen.get_Saldo(browser,0)
#     output_saldo(mysaldo)

#george_open = George.GeorgeScrapper.opensite(browser)
