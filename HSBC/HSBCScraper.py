"""Manage Website Interaction with HSBC."""


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
        self.no_accounts = bank_info['no_accounts']
        print(self.no_accounts)

    def opensite(self):
        """Open website and place browser on  accounts page."""
        self.browser.get(self.url)
        self.browser.wait_for_element(name='u_UserID').send_keys(self.user)
        self.browser.find_element_by_css_selector("img[alt=\"Dual Password\"]").click()
        self.browser.wait_for_element(timeout=30, id_='memorableAnswer').send_keys(self.password1)
        i = 1
        while(i < 9):
            passstring = "pass"+str(i)
            if (self.browser.find_element_by_id(passstring).is_enabled()):
                self.browser.find_element_by_id(passstring).send_keys(self.password2[i-1])
            i = i+1
        self.browser.find_element_by_css_selector("input.submit_input").click()
        self.browser.wait_for_element(timeout=60, xpath="//div[@id='hdx_dijits_TitlePane_0_pane']/div/span/span/span[4]").click()

    def get_Saldo(self, account=0):
        """Get the account Balance."""
        if(account == 0):
            account_saldo_raw = self.browser.wait_for_element(xpath="//div[@id='hdx_dijits_TitlePane_0_pane']/div[2]/span[1]/a").text
        elif(account == 1):
            account_saldo_raw = self.browser.wait_for_element(xpath="//div[@id='hdx_dijits_TitlePane_0_pane']/div[2]/span[2]/a").text
        elif (account == 2):
            account_saldo_raw = self.browser.wait_for_element(xpath="//div[@id='hdx_dijits_TitlePane_0_pane']/div[2]/span[3]/a").text
        elif (account == 3):
            account_saldo_raw = self.browser.wait_for_element(xpath="//div[@id='hdx_dijits_TitlePane_0_pane']/div[2]/span[4]/a").text
        elif (account == 4):
            account_saldo_raw = self.browser.wait_for_element(xpath="//div[@id='hdx_dijits_TitlePane_0_pane']/div[2]/span[5]/a").text
        else:
            account_saldo_raw = self.browser.wait_for_element(xpath="//div[2]/div/div/div/div/span/a").text
        # //div[@id='gridx_Grid_0']/div[3]/div[2]/div[3]/table/tbody/tr/td[3] other option
        account_data = account_saldo_raw.splitlines()
        print(account_saldo_raw)
        print(account_data)
        account_saldo = {'bank': "HSCB"+str(account), 'saldo': account_data[3], 'currency': account_data[2]}
        return(account_saldo)

    def get_transactions(self,  delta_days=3, account=0):
        """Get a list of transactions fom account from the website."""
        self.browser.wait_for_element_show(xpath="//div[@id='hdx_dijits_TitlePane_0_pane']/div[2]/span/a")
        trans_list = []
        if(account < 5):
            myaccount = self.browser.get_elms(xpath="//div[@id='hdx_dijits_TitlePane_0_pane']/div[2]/span/a")[account]
            myaccount.click()
            trans_FX_curr = myaccount.text.splitlines()[2]
            print(trans_FX_curr)
        else:
            self.browser.wait_for_element(xpath="//div[2]/div/div/div/div/span/a").click()
            trans_FX_curr = "HKD"
        try:
            self.browser.wait_for_element_show(id_='dapViewMoreDownload')
            print("foundit")
            trans_table = self.browser.get_elms(xpath='//div[2]/div/table/tbody/tr/td')
            i = 0
            print(len(trans_table))
            trans_account = self.bank_name+str(account)
            while(i < (len(trans_table)-4)):
                trans_date = trans_table[i].text
                trans_amount = trans_table[i+2].text
                trans_counterpart = ""
                trans_description = trans_table[i+1].text
                trans_memo = ""
                trans_category = ""
                trans_FX_rate = 0
                trans_list.append([trans_account, trans_date, trans_amount,
                                  trans_counterpart, trans_description,
                                  trans_memo, trans_category, trans_FX_curr,
                                  trans_FX_rate, False, False])
                i = i+5
                print("Inthelloop")
        except:
            print("ElementNotFound")
            pass
        print(trans_list)
        return(trans_list)
