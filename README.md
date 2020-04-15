e-ink dashboard for Signal K
============================

Status: in testing

This project provides a dashboard view to telemetry from [Signal K](http://signalk.org/) to be displayed on an e-ink screen connected to a Raspberry Pi. Different dashboards can be viewed based on ship's `navigation.state`.

![e-ink dashboard with Signal K data](https://live.staticflickr.com/65535/48726248553_6de2d37127_c_d.jpg)

Eventually this might replace more traditional marine display units on a Signal K enabled vessel.

The project is inspired on the [inkstate](https://github.com/yawkat/inkstate) weather display.

## Requirements

* Raspberry Pi (tested with 3B+ and Zero W)
* Python 3
* Working installation of Signal K
* [WaveShare 4.2inch e-paper module](https://www.waveshare.com/wiki/4.2inch_e-Paper_Module)

## Setup

* Connect the e-paper module to your Raspberry Pi and enable the SPI interface
* Clone this repository
* Install dependencies from `requirements.pip`
* Set up fonts you want to use to the `assets` folder
* Edit `config.py` to your liking
* Copy the systemd unit file to `/lib/systemd/system` and start it

## TODO

* Test with more data providers/conversions
* Design casing for the display and Raspberry Pi
* (maybe) test outdoor usage
