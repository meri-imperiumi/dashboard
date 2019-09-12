#!/usr/bin/python
# -*- coding:utf-8 -*-
import display
import draw
import signalk
import json

target = display.DrawTarget()
dashboard = draw.Draw(target)

def on_message(ws, message):
    msg = json.loads(message)
    if not "updates" in msg:
        return
    for update in msg["updates"]:
        for value in update["values"]:
            if value["path"] == "navigation.state":
                dashboard.set_display(value["value"])
                signalk.subscribe(ws, dashboard.get_paths())
            else:
                dashboard.update_value(value, update["timestamp"])

def on_error(ws, error):
    print(error)

def on_open(ws):
    initial_state = signalk.get_state()
    if initial_state:
        dashboard.show_message(f"Connected to Signal K, state: {initial_state}")
        dashboard.set_display(initial_state)
    else:
        dashboard.show_message('Connected to Signal K')
        dashboard.set_display('default')
    signalk.subscribe(ws, dashboard.get_paths())
dashboard.set_display('loading')
dashboard.show_message('Connecting to Signal K...')
dashboard.loop()
signalk.connect(on_message, on_error, on_open)
