#! /bin/bash

# This script is to setup the ECU raspberry pi. 
# The main tasks are to:
# - configure the wifi so that we connect to the right networks in order to ssh
# - Setup CAN drivers and CAN network in the main config
# - Install neccessary libraries to run the ECU's code
# - Reboot
# - (do the rest of the setup so that we can run the ECU to control the arduino. Todo later)

setup_wiringPi() {
    echo "Installing wiringPi"
    # sudo apt-get install wiringpi || { echo "Failed to install wiringPi!" && return 1; }
    sudo apt install -y git || return 1;
    git clone https://github.com/WiringPi/WiringPi || return 1;
    cd WiringPi || return 1;
    ./build || return 1;
} 

setup_bullseye() {
    echo "Appending CAN configuration to /boot/config.txt"
    echo "dtparam=spi=on" | sudo tee -a /boot/config.txt || { echo "Failed to append dtparam!" && return 1; }
    echo "dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000" | sudo tee -a /boot/config.txt || { echo "Failed to append dtoverlay!" && return 1; }
}

setup_bookworm() {
    echo "Appending CAN configuration to /boot/firmware/config.txt"
    echo "dtparam=spi=on" | sudo tee -a /boot/firmware/config.txt || { echo "Failed to append dtparam!" && return 1; }
    echo "dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000" | sudo tee -a /boot/firmware/config.txt || { echo "Failed to append dtoverlay!" && return 1; }
}
    
setup () {
    if [[ $# -eq 0 ]]; then
        echo "Usage: $0 --ecu | --controller"
        echo "  --ecu        Set up the ECU configuration."
        echo "  --controller Set up the Controller configuration."
        echo "  --skip       Skips the setup of control unit specific configurations"
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
        --skip)
            echo "Skipping specific configuration"
            ;;
        *)
            echo "Invalid option: $1"
            echo "Usage: $0 --ecu | --controller"
            return 1
            ;;
    esac

    echo "Validating wiringPi installation"
    gpio -v || { setup_wiringPi || { echo "wiringPi installation validation failed!" && return 1; } }

    echo "Setting up the Python CAN tools:"
    sudo apt-get update || { echo "Failed to update package list!" && return 1; }
    sudo apt-get install python3-serial || { echo "Failed to install python3-serial!" && return 1; }
    sudo apt-get install python3-can || { echo "Failed to install python3-can!" && return 1; }
    sudo apt-get install can-utils || { echo "Failed to install can-utils!" && return 1; }

    
    # Extract the version name from /etc/os-release
    VERSION_CODENAME=$(grep VERSION_CODENAME /etc/os-release | cut -d= -f2)
    
    case "$VERSION_CODENAME" in
        bookworm)
            setup_bookworm || { echo "Failed to run the CAN board setup for your bookworm system"  && return 1; }
            ;;
        bullseye)
            setup_bullseye || { echo "Failed to run the CAN board setup for your bullseye system"  && return 1; }
            ;; 
        *)
            echo "Unsupported Debian version: $VERSION_CODENAME"
            ;;
    esac

    
    return 0
}

setup "$@" || {
    echo "🚧 Something went wrong with the auto setup. Please fix manually and edit the setup script :)" &&
    exit 1
}

echo "✅ Setup complete!"
echo "Please reboot your system!"
