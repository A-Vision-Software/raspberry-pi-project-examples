![A-Vision Solutions][logo]

# A-Vision Powercontrol thing

The [A-Vision Powercontrol thing][productlink] makes use of https://webthings.io and does **not** include a WebThings gateway.

Please refer to https://webthings.io/docs/gateway-getting-started-guide.html to install a WebThings gateway.
You can either chose to install the Powercontrol thing on a separate Raspberry Pi (3/4/ZeroW) or combine it with a WebThings gateway.

Requirements:
- Python (version 3 - https://www.python.org)
- I²C enabled (https://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/)
- gpiozero (https://gpiozero.readthedocs.io/en/stable/)
- WebThings framework (https://webthings.io/api/)

![A-Vision Powercontrol thing][product]

## Installation

Once you have your Raspberry Pi up and running, follow the following instructions to get the Powercontrol thing script
```shell
wget https://github.com/A-Vision-Software/raspberry-pi-project-examples/archive/refs/heads/main.zip
unzip -j main.zip "raspberry-pi-project-examples-main/powercontrol-thing/*" -d powercontrol
rm main.zip
cd powercontrol
chmod 0755 install.sh
./install.sh
```
Make sure to have installed Python3 + pip (`sudo apt install python3 python3-pip`) before installing the Powercontrol thing script.


## Run the powercontrol Python script as a service

Running the Powercontrol WebThings script as a service is required to autmoatically start the WebThings Powercontrol server after rebooting the Raspberry Pi.
**This is not a part of the install script.**

Add a new service to the system using the following command-
```
sudo nano /lib/systemd/system/powercontrol.service
```
Or copy the `powercontrol.service` file to `/lib/systemd/system/`.

Add the following content to the service file-
```ini
[Unit]
Description=Powercontrol thing service
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
User=pi
Group=pi
ExecStart=/usr/bin/python3 /home/pi/powercontrol/powercontrol.py
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
sudo systemctl enable powercontrol.service
```
Finally start the new powercontrol service and view their status
```
sudo systemctl start powercontrol.service
(alternative => sudo service powercontrol start)
```
Check if the service is running and view warnings/errors
```
sudo systemctl status powercontrol.service
(alternative => sudo service powercontrol status)
```

[logo]: https://raspberry.a-vision.solutions/wp-content/uploads/2021/03/logo-company-name-description-automatically-gene.png "A-Vision solutions"
[product]: https://raspberry.a-vision.solutions/wp-content/uploads/2020/09/PCB-Pi-Power-Control-HAT-Rev-1.5-3D.png "A-Vision Powercontrol thing"
[productlink]: https://raspberry.a-vision.solutions/nl/product/ppchat15/
