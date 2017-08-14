import smtplib


def send_saldo(msg):
    fromaddr = 'christian.bren@gmail.com'
    toaddrs  = 'christian,bren@gmail.com'
    username = 'christian,bren@gmail.com'
    password = 'rhohiyrvxgjydltq'
    server = smtplib.SMTP('smtp.gmail.com:587')
    subject="SALDO"
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (fromaddr, ", ".join(toaddrs), subject, msg)
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()



t=send_saldo("hello")
