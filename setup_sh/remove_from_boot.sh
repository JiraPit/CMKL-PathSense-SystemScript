#!/bin/bash

echo "Removing PathSense system script from boot..."

# Check if the command is present in rc.local
if grep -Fxq "cd /SystemScript && sudo python main.py &" /etc/rc.local
then
    # Remove the line containing the command
    sudo sed -i '/cd \/SystemScript && sudo python main.py &/d' /etc/rc.local
    echo "PathSense system script removed from boot"
else
    echo "PathSense system script is not set to run at boot"
fi
