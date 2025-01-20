---
title: Steps to create device
---

# Raspberry Pi

## Setup Access Point if not connected to internet
Based on this article: `https://raspberrypi.stackexchange.com/questions/100195/automatically-create-hotspot-if-no-network-is-available`

1. Configure network
in `/etc/wpa_supplicant/wpa_supplicant.conf `



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

`sudo  /boot/config.txt` <<
```
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000
```