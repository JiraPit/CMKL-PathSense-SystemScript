#!/bin/bash

echo "Setting PathSense system script to run on boot..."

# Copy the SystemScript folder to the root directory
sudo cp -r SystemScript /

echo "PathSense system script added to root directory"

# Check if main.py is already in the boot file
if grep -Fxq "cd /SystemScript && sudo python main.py &" /etc/rc.local
then
    echo "PathSense system script is already set to run at boot"
else
    # If not, add the command to the boot file
    sed -i '$i cd /SystemScript && sudo python main.py &' /etc/rc.local
    echo "PathSense system script is now set to run at boot"
fi

echo "Reboot to start the system script"
