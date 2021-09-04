# HoverMower
Lawn mower made from the basics of a hoverboard

sudo apt-get install python-dev python-pip gcc
pip3 install approxeng.input

sudo apt-get install bluetooth libbluetooth3 libusb-dev
sudo systemctl enable bluetooth.service
sudo usermod -G bluetooth -a pi

bluetoothctl

agent on
scan on
pair C8:3F:26:1E:C3:7F
connect C8:3F:26:1E:C3:7F
trust C8:3F:26:1E:C3:7F

CTRL-D