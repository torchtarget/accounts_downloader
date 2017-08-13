import codecs
import os
import pickle


# passfile = open('coffee.exe', 'wb')
# passlist={'Hello':'Monkeys'}
keyfile = "/tmp/scan.exe"


def store_key(key_name, key_encoder):
    with open(keyfile, "rb") as input_file:
        if(os.path.getsize(keyfile)) > 0:
            key_list = pickle.loads(codecs.decode(input_file.read(), "base64"))
        else:
            key_list = {'Hello': 'Monkeys'}
    key_list[key_name] = key_encoder
    key_store = codecs.encode(pickle.dumps(key_list, 4), "base64")
    with open(keyfile, "wb") as output_file:
            output_file.write(key_store)
    return


def get_key(name):
    with open(keyfile, "rb") as input_file:
        keylist = pickle.loads(codecs.decode(input_file.read(),"base64"))
    return(keylist[name])

def put_keys(bank,name,pass1,pass2="none"):
    store_key(bank+"_user",name)
    store_key(bank+"_pass1",pass1)
    store_key(bank+"_pass2",pass2)
    return;

def get_user(bank):
    return(get_key(bank+"_user"))

def get_pass1(bank):
    return(get_key(bank+"_pass1"))

def get_pass2(bank):
    return(get_key(bank+"_pass2"))

def get_pass(bank):
    return(get_key(bank+"_pass1"))
