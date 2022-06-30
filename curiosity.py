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
import config

logging.basicConfig(level=config.log_level)
logger = logging.getLogger(__name__)

target = display.DrawTarget()
dashboard = draw.Draw(target)

def on_message(ws, message):
    alarm_change=False
    nav_state_change=False
    
    msg = json.loads(message)
 #   logging.debug("on_message: Message is:" + str(message))
                  
    if not "updates" in msg:
        return
    for update in msg["updates"]:
        for value in update["values"]:
            if str(value) == "{}":
                break

## Look for new alarms
            if "notifications." in value["path"]:
                (alarm_active,alarm_change)=dashboard.update_alarm(value,update["timestamp"])
                logging.debug("Found notification in message. Alarm change;" +str(alarm_change))
                
## Navigation state change           
                                       
            if value["path"] == "navigation.state" :
                if dashboard.display != value["value"] and not dashboard.alarm_active():
                    logging.debug("Navigation state changed")
                    nav_state_change=True
                    new_state = value["value"]
            else:
                dashboard.update_value(value, update["timestamp"])
                
            if nav_state_change:
                dashboard.set_display(value["value"])
                signalk.subscribe(ws, dashboard.get_paths())
            
            if alarm_change :
                if alarm_active:
                    dashboard.set_display('alarm')
                signalk.subscribe(ws, dashboard.get_paths())
 #               dashboard.variable_loop()
            


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
