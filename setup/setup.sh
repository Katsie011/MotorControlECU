#! /bin/bash

# This script is to setup the ECU raspberry pi. 
# The main tasks are to:
# - configure the wifi so that we connect to the right networks in order to ssh
# - Setup CAN drivers and CAN network in the main config
# - Install neccessary libraries to run the ECU's code
# - Reboot
# - (do the rest of the setup so that we can run the ECU to control the arduino. Todo later)

setup () {
    if [[ $# -eq 0 ]]; then
        echo "Usage: $0 --ecu | --controller"
        echo "  --ecu        Set up the ECU configuration."
        echo "  --controller Set up the Controller configuration."
        return 1
    fi

    case "$1" in
        --ecu)
            echo "Setting up wifi for ECU"
            sudo cp ./ecu_wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf || { echo "Failed to setup wifi." && return 1; }
            ;;
        --controller)
            echo "Setting up wifi for Controller"
            sudo cp ./controller_wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf || { echo "Failed to setup wifi." && return 1; }
            ;;
        *)
            echo "Invalid option: $1"
            echo "Usage: $0 --ecu | --controller"
            return 1
            ;;
    esac

    echo "Installing wiringPi"
    sudo apt-get install wiringpi || { echo "Failed to install wiringPi!" && return 1; }

    echo "Validating wiringPi installation"
    gpio -v || { echo "wiringPi installation validation failed!" && return 1; }

    echo "Setting up the Python CAN tools:"
    sudo apt-get update || { echo "Failed to update package list!" && return 1; }
    sudo apt-get install python3-serial || { echo "Failed to install python3-serial!" && return 1; }
    sudo apt-get install python3-can || { echo "Failed to install python3-can!" && return 1; }

    echo "Setting up the CAN Bus network interface:"
    echo "Appending CAN configuration to /boot/config.txt"
    echo "dtparam=spi=on" | sudo tee -a /boot/config.txt || { echo "Failed to append dtparam!" && return 1; }
    echo "dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000" | sudo tee -a /boot/config.txt || { echo "Failed to append dtoverlay!" && return 1; }

    return 0
}

setup "$@" || {
    echo "🚧 Something went wrong with the auto setup. Please fix manually and edit the setup script :)" &&
    exit 1
}

echo "✅ Setup complete!"