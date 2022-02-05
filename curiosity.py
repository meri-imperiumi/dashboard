#!/usr/bin/python
# -*- coding:utf-8 -*-
import display
import draw
import signalk
import json
import time
import atexit
import logging
import sys, traceback

logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(level=logging.WARNING)

logger = logging.getLogger(__name__)

target = display.DrawTarget()
dashboard = draw.Draw(target)

def on_message(ws, message):
    msg = json.loads(message)
    if not "updates" in msg:
        return
    for update in msg["updates"]:
        for value in update["values"]:
            if str(value) == "{}":
                break
            if value["path"] == "navigation.state":
                if dashboard.display != value["value"]:
                    dashboard.set_display(value["value"])
                    signalk.subscribe(ws, dashboard.get_paths())
                    dashboard.variable_loop()
            else:
                dashboard.update_value(value, update["timestamp"])

def on_error(ws, error):
    message = str(error)
    traceback.print_exc(file=sys.stdout)
    logging.error('on_error: ' + message)
    if not message:
        # This is from quitting software, so don't reconnect
        return
    logging.info("Trying to reconnect")
    dashboard.set_display('loading')
    time.sleep(10)
    dashboard.show_message('Trying to connect...')
    signalk.connect(on_message, on_error, on_open, on_close)

def on_close(ws, close_status_code, close_msg):
    logging.info("Connection closed. Close code:" + str(close_status_code) + " Close msg:" + str(close_msg))

def on_open(ws):
    logging.info("Connected to Signal K")
    dashboard.show_message('Connected to Signal K')
    initial_state = signalk.get_state()
    if initial_state:
        dashboard.set_display(initial_state)
    else:
        dashboard.set_display('default')
    signalk.subscribe(ws, dashboard.get_paths())

def clear_screen():
    logging.info("Clearing screen, please stand by...")
    dashboard.clear_screen()
    logging.info("Ready, safe to exit now")

atexit.register(clear_screen)

dashboard.set_display('loading')
dashboard.show_message('Connecting to Signal K...')
dashboard.variable_loop()
signalk.connect(on_message, on_error, on_open, on_close)
