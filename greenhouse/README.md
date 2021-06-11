![A-Vision Solutions][logo]

# A-Vision Greenhouse monitor

The [A-Vision Greenhouse monitor][productlink] makes use of https://webthings.io and does **not** include a WebThings gateway.

Please refer to https://webthings.io/docs/gateway-getting-started-guide.html to install a WebThings gateway.
You can either chose to install the Greenhouse monitor on a separate Raspberry Pi (3/4/ZeroW) or combine it with a WebThings gateway.

Requirements:
- Python (version 3 - https://www.python.org)
- I²C enabled (https://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/)
- gpiozero (https://gpiozero.readthedocs.io/en/stable/)
- WebThings framework (https://webthings.io/api/)

![A-Vision Greenhouse monitor][product]

## Installation

Once you have your Raspberry Pi up and running, follow the following instructions to get the Greenhouse monitor script
```shell
cd /home/pi
wget https://github.com/A-Vision-Software/raspberry-pi-project-examples/archive/refs/heads/main.zip
unzip -j main.zip "raspberry-pi-project-examples-main/greenhouse/*" -d greenhouse
rm main.zip
cd greenhouse
chmod 0755 install.sh
chmod 0755 update.sh
./install.sh
```
Make sure to have installed Python3 + pip (`sudo apt install python3 python3-pip`) before installing the Greenhouse monitor script.

To update the monitor source code use `./update.sh` in the installation folder (`/home/pi/greenhouse`).

## Run the greenhouse Python script as a service

Running the greenhouse WebThings script as a service is required to autmoatically start the WebThings greenhouse server after rebooting the Raspberry Pi.
**This is not a part of the install script.**

Add a new service to the system using the following command-
```
sudo nano /lib/systemd/system/greenhouse.service
```
Or copy the `greenhouse.service` file to `/lib/systemd/system/`.

Add the following content to the service file-
```ini
[Unit]
Description=Greenhouse monitor service
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
User=pi
Group=pi
ExecStart=/usr/bin/python3 /home/pi/greenhouse/greenhouse.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then update the services
```
sudo systemctl daemon-reload
```
And enable the new service
```
sudo systemctl enable greenhouse.service
```
Finally start the new greenhouse service and view their status
```
sudo systemctl start greenhouse.service
(alternative => sudo service greenhouse start)
```
Check if the service is running and view warnings/errors
```
sudo systemctl status greenhouse.service
(alternative => sudo service greenhouse status)
```

[logo]: https://raspberry.a-vision.solutions/wp-content/uploads/2021/03/logo-company-name-description-automatically-gene.png "A-Vision solutions"
[product]: https://raspberry.a-vision.solutions/wp-content/uploads/2021/05/greenhousemonitor.png "A-Vision Greenhouse monitor"
[productlink]: https://raspberry.a-vision.solutions/greenhousemonitor/
