#!/usr/bin/python
# -*- coding:utf-8 -*-
import display
import draw
import signalk
import json
import time
import atexit

target = display.DrawTarget()
dashboard = draw.Draw(target)

def on_message(ws, message):
    msg = json.loads(message)
    if not "updates" in msg:
        return
    for update in msg["updates"]:
        for value in update["values"]:
            if value["path"] == "navigation.state":
                if dashboard.display != value["value"]:
                    dashboard.set_display(value["value"])
                    signalk.subscribe(ws, dashboard.get_paths())
                    dashboard.variable_loop()
            else:
                dashboard.update_value(value, update["timestamp"])

def on_error(ws, error):
    message = str(error)
    print(message)
    if not message:
        # This is from quitting software, so don't reconnect
        return
    print("Trying to reconnect")
    dashboard.set_display('loading')
    time.sleep(10)
    dashboard.show_message('Trying to connect...')
    signalk.connect(on_message, on_error, on_open, on_close)

def on_close():
    print("Connection closed")

def on_open(ws):
    print("Connected to Signal K")
    dashboard.show_message('Connected to Signal K')
    initial_state = signalk.get_state()
    if initial_state:
        dashboard.set_display(initial_state)
    else:
        dashboard.set_display('default')
    signalk.subscribe(ws, dashboard.get_paths())

def clear_screen():
    print("Clearing screen, please stand by...")
    dashboard.clear_screen()
    print("Ready, safe to exit now")
atexit.register(clear_screen)

dashboard.set_display('loading')
dashboard.show_message('Connecting to Signal K...')
signalk.connect(on_message, on_error, on_open, on_close)
dashboard.variable_loop()
