#!/bin/bash

echo "Installing PathSense system script..."

sudo apt-get update
sudo apt-get upgrade

sudo apt-get install v4l-utils -y
sudo apt-get install python3-dev -y
sudo apt-get install python3-opencv -y
sudo apt-get install libbluetooth-dev -y
sudo apt-get install python3-requests -y
sudo apt-get install unzip -y
sudo apt-get install wget -y

sudo rm -d -r pybluez-master
sudo rm master.zip
wget https://github.com/pybluez/pybluez/archive/master.zip
unzip master.zip
cd pybluez-master
yes all | sudo python setup.py install
cd ..

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

echo "PathSense system script installation complete"
echo "Reboot to start the system script"
