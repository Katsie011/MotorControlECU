---
title: Steps to create device
---

# Raspberry Pi

## Setup Access Point if not connected to internet
Based on this article: `https://raspberrypi.stackexchange.com/questions/100195/automatically-create-hotspot-if-no-network-is-available`

1. Configure network
Copy the relevant file from this folder into `/etc/wpa_supplicant/wpa_supplicant.conf `



# install wiringPi

<!-- 
``` bash
cd ~
sudo apt update
sudo apt-get install wiringpi
``` -->

If on a Bullseye branch system using the following command:
```bash
sudo apt install -y git
git clone https://github.com/WiringPi/WiringPi
cd WiringPi
./build
gpio -v
```

validate install with 
``` bash
gpio -v
```

# Installing python can tools
```bash
sudo apt-get update
sudo apt-get install -y python3-serial python3-can
```



# Setting up the can interface with the network:

`sudo  /boot/config.txt` <<
```
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000
```


```bash
sudo reboot
```

After rebooting, run the command to see if the initialization was successful:
```bash
dmesg | grep -i '\(can\|spi\)'
```

Once all is wired, check if it's working with Open CAN:
```bash
sudo ip link set can0 up type can bitrate 1000000
sudo ifconfig can0 txqueuelen 65536
sudo ifconfig can0 up
```


Install the can utils
```bash
sudo apt-get install can-utils
```
