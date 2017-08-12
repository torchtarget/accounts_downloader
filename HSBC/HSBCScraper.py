"""Manage Website Interaction with HSBC."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


# from selenium.common.exceptions import StaleElementReferenceException
# from datetime import date, timedelta
# import csv
# import re

# from selenium.webdriver.common.keys import Keys


class HSBCAccount():
    """HSCBAccount Class."""

    delay = 10

    def __init__(self, browser, bank_info):
        """Define all variable to access George Site."""
        self.browser = browser
        self.user = bank_info['user']
        self.password1 = bank_info['pass1']
        self.password2 = bank_info['pass2']

        self.url = "https://www.ebanking.hsbc.com.hk/1/2/logon?LANGTAG=en&COUNTRYTAG=US"
        self.account = str(0)
        self.bank_name = "HSBC"
        self.category_map_filename = 'HSBCCategoryMap.csv'

    def opensite(self):
        """Open website and place browser on  accounts page."""
        self.browser.get(self.url)
        try:
            myElem = WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.NAME, 'u_UserID')))
        except TimeoutException:
            print("Loading took too much time!")
        self.browser.find_element_by_name("u_UserID").clear()
        self.browser.find_element_by_name("u_UserID").send_keys(self.user)
        self.browser.find_element_by_css_selector("img[alt=\"Dual Password\"]").click()
        try:
            myElem = WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.ID, 'memorableAnswer')))
            self.browser.find_element_by_id("memorableAnswer").clear()
            self.browser.find_element_by_id("memorableAnswer").send_keys(self.password1)
        except TimeoutException:
            print("Loading took too much time!")
        i = 1
        while(i < 9):
            passstring = "pass"+str(i)
            if (self.browser.find_element_by_id(passstring).is_enabled()):
                self.browser.find_element_by_id(passstring).send_keys(self.password2[i-1])
            i = i+1
        self.browser.find_element_by_css_selector("input.submit_input").click()

    def get_Saldo(self, account=0):
        """Get the account Balance."""
        try:
            myElem = WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.XPATH, "//div[@id='hdx_dijits_TitlePane_0_pane']/div/span/span/span[4]")))
            print("Found bit")
        except TimeoutException:
            print("Loading took too much time!")
        self.browser.find_element_by_xpath("//div[@id='hdx_dijits_TitlePane_0_pane']/div/span/span/span[4]").click()

        try:
            myElem = WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.XPATH, "//div[@id='hdx_dijits_TitlePane_0_pane']/div[2]/span[2]/a")))
        except TimeoutException:
            print("Loading took too much time!")
        account_saldo = self.browser.find_element_by_xpath("//div[@id='hdx_dijits_TitlePane_0_pane']/div[2]/span[2]/a").text
        print(account_saldo)
        return(account_saldo)
