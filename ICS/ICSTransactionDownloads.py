##! /usr/bin/python3
import requests

payload = {
    'login-form-type': 'pwd',
    'username': 'TBC',
    '_rememberLogin': 'on',
    'password': '"TBD"'

}

loginurl = 'https://www.mijn-icsbusiness.nl/pkmslogin.form'

downloadurl = 'https://www.mijn-icsbusiness.nl/icsbusiness/mijn/alltransactionpayments'
with requests.Session() as s:
    p = s.post(loginurl, data=payload)
    r = s.get(downloadurl)
    with open("/tmp/test.html", "w") as head_file:
        head_file.write(r.text)
