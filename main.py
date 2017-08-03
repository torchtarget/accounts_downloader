##! /usr/bin/python3
import myencoder
from selenium import webdriver
import Santander.SantanderOpen
import George.GeorgeScrapper
import time
from forex_python.converter import CurrencyRates

# date and time representation
saldo_file = "/tmp/saldo.txt"

santander_open = False
george_open = False
c = CurrencyRates()


def output_saldo(account_saldo):
    # saldo_euro= c.convert(account_saldo["currency"], 'EUR', account_saldo["saldo"])
    saldo_euro = 1
    with open(saldo_file, "a") as output_file:
        output_file.write(account_saldo["bank"]+","+account_saldo["saldo"]+","+account_saldo["currency"]+","+str(saldo_euro)+"\n")
    return


with open(saldo_file, "w") as output_file:
        output_file.write("Report: " + time.strftime("%c")+"\n")
browser = webdriver.Firefox()
#santander_open=Santander.SantanderOpen.opensite(browser)
#if(santander_open):
#     mysaldo=Santander.SantanderOpen.get_Saldo(browser,0)
#     output_saldo(mysaldo)

george_open = George.GeorgeScrapper.opensite(browser)
if(george_open):
    mysaldo = George.GeorgeScrapper.get_Saldo(browser, 0)
    output_saldo(mysaldo)
    mysaldo = George.GeorgeScrapper.get_Saldo(browser, 1)
    output_saldo(mysaldo)
    mysaldo = George.GeorgeScrapper.get_Saldo(browser, 2)
    output_saldo(mysaldo)
browser.quit()
