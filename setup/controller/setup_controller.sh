#! /bin/bash

# This script is to setup the ECU raspberry pi. 
# The main tasks are to:
# - configure the wifi so that we connect to the right networks in order to ssh
#   - Speciffically, we need to host an AP if the known networks are not found. 
# - Setup CAN drivers and CAN network in the main config
# - Install neccessary libraries to run the main controller's code
# - Reboot
# - (do the rest of the setup so that we can run the ECU to control the arduino. Todo later)
