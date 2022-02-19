## This module parses messages and converts those into text to be drawn
## on the screen. First the messages are parsed, then the module is called
## when the screen is to be drawn
## The module has two different ways to show notificatios, Alert screen or use the spave between statusmode and clock (for non-critical)

from PIL import Image,ImageDraw,ImageFont
import logging
import datetime
import dateutil.parser
import time
import math
import timeinterval

import config
from config import dashboard

logger = logging.getLogger(__name__)

## Dict of types of ntification and classification of those
states = {'nominal':0, 'normal':0, 'alert':1, 'warn':2, 'alarm':2, 'emergency':2}

class Alarmhandler:
    def __init__(self, alertfont,width,height):
        self.flush_needed = False
        self.number_of_calls = 0
        self.values = {}
        self.font = alertfont
        self.alerttext=""
        self.warningtext=""
        self.height=height
        self.width=width
        self.alarm_active = False
        self.number_of_active = 0
        self.number_of_active_warn = 0

## Parse messages and store alerts.
## Have a local copy (list), if delta=0, remove item, otherwise overwrite
## Check number of alarms, if 0, set alarm_active to False otherwise true
## Need exception list of alarms not to react on but use info instead
    def update_alarm(self, msg, timestamp):
        logger.debug("Got an alarm message: " + str(msg))
        logger.debug("Number of alarms:" + str(self.number_of_active))
        
## Handle notificatios that are not alarms (state {normal, nominal}
## Handle notifications that are alamrs(still safe state:{alarm}
## Handle notifications that are important state:{warn,alarm,emergency}

        state = msg['value']['state']
        state_group=states[state]
        new_notification = False

## Empty value of a previous alarm (should indicate to remove notification)     
        if not msg['value'] and msg['path'] in self.values:
            if self.values[msg['path']]['state_group']==1 :
                self.number_of_active_warn-=1
            elif self.values[msg['path']]['state_group']==2 :
                self.number_of_active -= 1 

            del self.values[msg['path']]
            logger.debug("Removed alarm:" + str(msg['path']))

## We don't want to add normal/nominal messages, drop them
        if state_group == 0 and (not msg['path'] in self.values):
            logger.debug("Got notification normal/noninal not in DB. Drop it")

## Handle transitions of older notifications recieved
        if msg['path'] in self.values:

## Handle alarms that have transitioned to normal/nominal      
            if state_group == 0:
                if self.values[msg['path']]['state_group']==1 :
                    self.number_of_active_warn-=1
                elif self.values[msg['path']]['state_group']==2 :
                    self.number_of_active -= 1
                
                del self.values[msg['path']]

            elif state_group == 1:
## Transition from alarm (2)-> alert (1)
                if self.values[msg['path']]['state_group']==2 :
                    self.number_of_active_warn+=1
                    self.number_of_active -= 1           
            else:
## Transition from alarm (1)-> alert (2)
                if self.values[msg['path']]['state_group']==1 :
                    self.number_of_active_warn-=1
                    self.number_of_active += 1             
## It's a new alarm
        else:
            logger.debug("New alarm.")
            if state_group == 1:
                self.number_of_active_warn += 1
            if state_group == 2:
                self.number_of_active += 1

## Update internal list if an alarm or alert
        if state_group !=0 :
            self.values[msg['path']] = {
                    'message': msg['value']['message'],
                    'time': dateutil.parser.parse(timestamp),
                    'state': state,
                    'state_group': state_group,
                    'rendered': False
            }
        
        old_alarm_active = self.alarm_active
        
        if self.number_of_active==0 :
            self.alarm_active = False
        else:
            self.alarm_active = True

        logger.debug("Done update alarm. Status: Number of alarms:" + str(self.number_of_active) + " status:" + str(self.alarm_active))
        logger.debug("Alarms:" + str(self.values))
        
        return (self.alarm_active, not old_alarm_active == self.alarm_active)

    def active_alarm(self):
        return self.alarm_active
    
 
# Draw alarm message on buffer 
    def draw(self):
        time_height = dashboard['layout']['time_height']
        image = Image.new('1', (self.width, self.height-time_height-dashboard['layout']['space_edges']) , 1)
        draw = ImageDraw.Draw(image)
        draw.text((1,1), self.alerttext, font=self.font)
        return image
