##! /usr/bin/python3
import re

from bs4 import BeautifulSoup
import requests


class ICSBank:
    """Object gets ICS Data."""

    def __init__(self, bank_info):
        """Define all the variables to access the sit."""
        payload = {
            'login-form-type': 'pwd',
            'username': bank_info['user'],
            '_rememberLogin': 'on',
            'password': bank_info['pass1']
        }
        loginurl = 'https://www.mijn-icsbusiness.nl/pkmslogin.form'
        trans_url = 'https://www.mijn-icsbusiness.nl/icsbusiness/mijn/alltransactionpayments'
        account_url = 'https://www.mijn-icsbusiness.nl/icsbusiness/mijn/accountoverview'
        with requests.Session() as s:
            p = s.post(loginurl, data=payload)
            self.trans_html = s.get(trans_url)
            self.account_html = s.get(account_url)

    def get_Saldo(self):
        """Test."""
        #print(self.account_html)
        soup = BeautifulSoup(self.account_html.text, "html.parser")
        class_list = ["amount"]
        myamounts = soup.find_all('span', class_=class_list)
        account_saldo_float = -1*(float(''.join(re.findall('\d+', str(myamounts[1]))))/100)
        account_saldo_str = str(account_saldo_float)
        account_currency = "EUR"
        saldo_return = {"bank": "ICS0", "saldo": account_saldo_str, "currency": account_currency}
        return(saldo_return)
# will find any divs with any names in class_list:


    def get_transactions(self, delta_dats=3, account=0):
        """Get all transactions."""
        r = self.__get_html_trans()
        soup = BeautifulSoup(r, "html.parser")
        print(soup.title)
        data = []
        table = soup.find('table', attrs={'class': 'expander-table'})
        rows = table.find_all('tr')
        for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                print("Cols:"+str(cols))
                # data.append([ele.replace(',', '') for ele in cols])
                data.append(cols)
        #print("Data"+data)
        with open("/tmp/test6.csv", "w") as output_file:
            for dataline in data:
                output_file.write("%s" % dataline)
        print(data[23])

    #    with open("/tmp/test.html", "w") as head_file:
    #        head_file.write(r.text)
