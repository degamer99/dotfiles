import random
from threading import Thread

chars = "abcdefghijklmnopqrstuvwxyz0123456789"
user_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
counter = 0
name = 1

def main():
    while True:
        valid = False
        while not valid:
            rndrstg = random.choices(user_chars, k=4)
            rstg = f"RSTG{"".join(rndrs)}"
            file = open("rstg.txt", 'r')
            contents_of_rstg_file = file.read()
            file.close()
            if rstg in contents_of_rstg_file:
                pass
            else:
                with open("rstg.txt", "a") as f:
                    f.write(f"{rstg}\n")
                    f.close()
                print(f"Incorrect {rstg}\n")
                valid = True


for x in range(50):
    Thread(target=main).start()
