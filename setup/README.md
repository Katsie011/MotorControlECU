---
title: Steps to create device
---

# Raspberry Pi

## Setup Access Point if not connected to internet
Based on this article: `https://raspberrypi.stackexchange.com/questions/100195/automatically-create-hotspot-if-no-network-is-available`

1. Configure network
in `/etc/wpa_supplicant/wpa_supplicant.conf `

add:
``` bash
country=CH
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
ap_scan=1

### your access point/hotspot ###                           

network={
    priority=0            # Lowest priority, so wpa_supplicant prefers the other networks below
    ssid="REX_ECU_AP"    # your access point's name
    mode=2
    key_mgmt=WPA-PSK    
    psk="Control2023!"      # your access point's password 
    frequency=2462
}

### your network(s) ###
network={
    priority=10       # add a priority higher then 0 to any networks
    ssid="Büro Züri Innovationspark"   # except the access point's one!
    psk="BZI2022<3"
} 

network={
    priority=8
    ssid="Michael's iPhone"
    psk="getFucked"
}
#network={
#    priority=9
#    ssid="REX_ECU_AP"
#    psk="Control2023!"
#}
```

2. mkdir ~/Tools && cd ~/Tools
3. git clone https://github.com/0unknwn/auto-hotspot.git
4. cd auto-hotspot
5. sudo chmod +x install.sh
6. sudo ./install.sh
7. reboot


# install wiringPi

``` bash
cd ~
sudo apt-get install wiringpi
```

validate install with 
``` bash
gpio -v
```

# Installing python can tools
sudo apt-get update
sudo apt-get install python3-serial
sudo apt-get install python3-can




# Setting up the can interface with the network:

`sudo nano /boot/config.txt` <<
```
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000
```