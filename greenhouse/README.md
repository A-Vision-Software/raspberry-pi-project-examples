# A-Vision Greenhouse monitor

The A-Vision Greenhouse monitor makes use of https://webthings.io and does *not* include a WebThings gateway.

Please refer to https://webthings.io/docs/gateway-getting-started-guide.html to install a WebThings gateway.
You can either chose to install the Greenhouse monitor on a separate Raspberry Pi (3/4/ZeroW) or combine it with a WebThings gateway.

Requirements:
- Python (version 3 - https://www.python.org)
- I²C enabled (https://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/)
- gpiozero (https://gpiozero.readthedocs.io/en/stable/)
- WebThings framework (https://webthings.io/api/)


## Installation



    wget https://github.com/A-Vision-Software/raspberry-pi-project-examples/archive/refs/heads/main.zip
    unzip main.zip "raspberry-pi-project-examples-main/greenhouse/*" -d greenhouse
    rm main.zip
    cd greenhouse
    chmod 0775 install.sh
    ./install.sh

## Run the greenhouse script as a service

Running the greenhouse WebThings script as a service is required to autmoatically start the WebThings greenhouse server after rebooting the Raspberry Pi.

Add a new service to the system using the following command-

    sudo nano /lib/systemd/system/greenhouse.service

Add the following content to the service file-

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


Then update the services

    sudo systemctl daemon-reload

And enable the new service

    sudo systemctl enable greenhouse.service

Finally start the new greenhouse service and view their status

    sudo systemctl start greenhouse.service
    sudo systemctl status greenhouse.service