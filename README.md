e-ink dashboard for Signal K
============================

Status: Working

This project provides a dashboard view to telemetry from [Signal K](http://signalk.org/) to be displayed on an e-ink screen connected to a Raspberry Pi. Different dashboards can be viewed based on ship's `navigation.state`. The [signalk-autostate plugin](https://github.com/meri-imperiumi/signalk-autostate) can be used to automatically update `navigation.state` based on vessel telemetry.

![e-ink dashboard with Signal K data](https://live.staticflickr.com/65535/48726248553_6de2d37127_c_d.jpg)

Eventually this might replace more traditional marine display units on a Signal K enabled vessel.

The project is inspired on the [inkstate](https://github.com/yawkat/inkstate) weather display.

## Requirements

* Raspberry Pi (tested with 3B+,3B, 400 and Zero W)
* Python 3
* Working installation of Signal K
* Waveshare e-ink dsiplay such as [WaveShare 4.2inch e-paper module](https://www.waveshare.com/wiki/4.2inch_e-Paper_Module)

## Setup

* Download the software/drivers from WaveShare by cloning (as they describe)
* Connect the e-paper module to your Raspberry Pi and enable the SPI interface
* Test the Python example for your display to ensure that it works
	There might be an issue where the Python program runs but nothing is draw to the display. If so, try
	Modify in epdconfig.py (in lib folder) to the following SPI_FRQ = 2000000 (this reduces the data rate over SPI)
* Install the EPD library from the python directory	(/home/pi/e-Paper/RaspberryPi_JetsonNano/python)
	sudo python3 setup.py build
	sudo python3 setup.py install
* Clone this repository
* Install the other dependencies from `requirements.pip`
* Set up fonts and splash screen you want to use to the `assets` folder
* Edit `config.py` to your liking
* Copy the systemd unit file to `/lib/systemd/system` and start it

## TODO

* Test with more data providers/conversions
* Design casing for the display and Raspberry Pi
* (maybe) test outdoor usage
