# Linux Battery Status script for the Tutle Beach Stealth 600 Gen3
This script reads the current state of charge from the proprietary 2.4GHz usb dongle using raw hid.

## How to install
###Fedora

```
sudo dnf install hidapi python3-pip
pip install --break-system-packages hid
sudo cp etc/udev/rules.d/99-turtlebeach.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
sudo usermod -aG plugdev $USER
```

Copy the script `headset_battery.py` can be put anywhere in your path.
I personally put it into `/usr/local/bin`

## Usage
The script has three output types.

```
$ headset-battery --json
{"battery": 100}
$ headset-battery --short
100%
$ headset-battery
Stealth 600: 100%
```

## Limitations
As of now it only works with the Stealth 600 other headsets may also just work but you'll need to change the VID and PID to fit them.

## AI usage for this project
I don't know much about USB HID devices and such. I just wanted to know the SoC of my headset in Linux and not rely on my phone, bluetooth or a Windows VM.
I used Claude to help me decode what I found and to point me in the right direction. It also helped me clean up the code and trim it down.
Without the usage of AI I would not have complete it and got this working.