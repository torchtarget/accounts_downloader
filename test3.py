##! /usr/bin/python3
import HSBC.HSBCScraper
from configobj import ConfigObj
import sql_transactions
from webdriverwrapper.wrapper import Firefox


# import Santander.SantanderOpen
#import George.GeorgeScrapper
#import ICS.ICSScraper
# date and time representation

saldo_file = "/tmp/saldo.txt"
bank_config = ConfigObj("/home/chris/git/accounts_downloader/banks_config.ini")
sqlite_file = bank_config['sqlite_file']


def get_bank_info(bank_name):
    """Parse Config File and get Bank Data."""
    bank_user = bank_config['Banks'][bank_name]['Username']

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
    return({"user": bank_user, "pass1": bank_password1, "pass2": bank_password2})


def output_saldo(account_saldo):
    """Output the balances to a file."""
    # saldo_euro= c.convert(account_saldo["currency"], 'EUR', account_saldo["saldo"])
    saldo_euro = 1
    with open(saldo_file, "a") as output_file:
        output_file.write(account_saldo["bank"]+","+account_saldo["saldo"]+","+account_saldo["currency"]+","+str(saldo_euro)+"\n")
    return


browser = Firefox()

bank_info = get_bank_info('HSBC')
print(bank_info)
hsbc = HSBC.HSBCScraper.HSBCAccount(browser, bank_info)
hsbc.opensite()

mysaldo = hsbc.get_Saldo(0)
print(mysaldo)
mytrans=hsbc.get_transactions(3,0)
print(mytrans)
#trans_db = sql_transactions.Accounts_SQL(sqlite_file)

    #mysaldo = george.get_Saldo(i)
#        print(mysaldo)#
# output_saldo(mysaldo)


#print(monkey)
#browser.quit()
