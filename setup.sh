#!/bin/bash

echo "Installing PathSense system script..."

sudo apt-get update
sudo apt-get install v4l-utils -y
sudo apt-get install python3-opencv -y
sudo apt-get install libbluetooth-dev -y
sudo apt-get install python3-pybluez -y

# Copy the SystemScript folder to the root directory
cp -r SystemScript /

echo "PathSense system script installed"

# Check if main.py is already in the boot file
if grep -Fxq "python /SystemScript/main.py &" /etc/rc.local
then
    echo "PathSense system script is already set to run at boot"
else
    # If not, add the command to the boot file
    sed -i '$i python /SystemScript/main.py &' /etc/rc.local
    echo "PathSense system script is now set to run at boot"
fi

echo "PathSense system script installation complete"
