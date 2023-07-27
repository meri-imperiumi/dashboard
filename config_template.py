# -*- coding:utf-8 -*-

import logging

#signalk_host = 'localhost'
signalk_host = 'raspberrypi400.local'
#signalk_host = 'hal.local'
signalk_port = 3000

#Set the global logging level. This is also used by WaveShare code
log_level = logging.WARNING
#log_level = logging.DEBUG

# Set to False for screen not having partial update, True for screens that has
# !!Partial updates not implemented!!
# If set to true, slots will be updated in the backgroud but with not
# drawn until a certain number of slots have been updated.
partial_update = False
partial_frame_limit = 20

# Update speeds in miliiseconds, you may want to increase this for scren 
# with no partial update as they do fullrefresh each time.
#
# Refreshtime for a display is quite long (seconds) for a full refresh, 
# do not make this too short if the screen is not using partial refresh.
# As per WaveShare notes, a full refresh time should not be lower than 180s (180000 ms)
loop_time_alarm=30000
loop_time_moving=180000
loop_time_anchor=300000
loop_time_moored=600000

# Global settings for all screens (moored, sailing etc)
#
# first_row_height : Size of the bigger first row in pixels
# space_row: Space between rows on the display in pixels
# space_edges: Space to the edges of the screen (in pixels)
# other_row_height: High of the second or thrd row (if used) in pixels
# text_field_height: Hight of the textfield if used (in pixels)
# text_field_offset: Offest from top where to place the text field (e.g under the value slots + margins etc
# time_width: The width of the clock in the right end corner (in pixels)
# time_height: The hight in plixels of the clock (and message area and status message)

#
# Each screen is configured individually when it comes to how many values that are to be shown
# by using these settings
# 
# number_of_top_slots: Number of Top row (large text) slots(values): 3 for 4,2" display 4 for 7,5" dislay
# number_of_mid_slots: Number of Mid row(s) (smaller text): 4 for 4,2"  5 for 7,5"
# number_of_slots: Total number of slots with values. Values after those can be used by the text field.
# text_field:False/True: Activates a text filed under the value slots where text can be written (like wearh prognosis)
# number_of_text_slots: Number of slots(collums) for the text field (if used)
#

dashboard = {
    'name': 'Tugboat Timmy',

    'assets': {
        'display_font': 'nasalization-rg.otf',
        'body_font': 'Eurostile.ttf',
        'splash': 'signalK.bmp'
    },
    
    'fontsizes': {
        #Top_to_meta is also used time and status fonts in the bottom
        'top_row_meta': 32,
        'top_row_value': 54,
        'mid_row_meta': 20,
        #Mid row meta is also used for the warning text between time and status
        'mid_row_value': 32, 
        'alarm':48,
        'text_field':20
    },


# Timeformat. Enable use of GPS (navigation.position) to get the right timezone
# when converting from UTC. Also det the default timezone.
# GPS based timezone not implemented
#        'TZ_conversion_use_GPS':False,
    'time_format': '%H:%M',
    'TZ_default_name': 'CEST',
    'TZ_default_offset': 2*3600,

    'layout': {
        'first_row_height': 130,
        'space_row':10,
        'space_edges':7,
        'other_row_height': 80,
        'text_field_height':100,
        'text_field_offset':325,
        'time_width':91,
        'time_height':40,
        'alarm_screen':True,
        
# value_margin is the distance between the label to the value
# unit_margin is the distance between the value and the unit
        'slot_margins' : {
            'top_row' : {
                'value_margin': 30,
                'unit_margin' : 75
            },
            'mid_row': {
                'value_margin': 20,
                'unit_margin' : 45
            }
        },


## If alarm_screen is set to True, the program will listen to alarms
## and switch to an alarm screen and show the alarms until they are canceled

##  'number_of_top_slots' Number of slots in the top row (bigger)
##  'number_of_mid_slots' Number of smaller slots under the top (per row)
##  'number_of_slots':0 Number of values for slots in total
##  'number_of_text_slots' Nuber of colums for the text

##  'alarm_screen' 
## This is just a dummy and can't be configured
        'loading': {
            'text_field':False,
            'number_of_top_slots':0,
            'number_of_mid_slots':0,
            'number_of_slots':0,
            'number_of_text_slots':0
        },

# Default screen is only used when there is no navigation state.
# This however do not take long time for Signal K to figure out so
# don't bother with dealing this one...
        'default': {
            'text_field':False,
            'number_of_top_slots':0,
            'number_of_mid_slots':0,
            'number_of_slots':0,
            'number_of_text_slots':0
        },

       'moored': {
            'text_field':False,
            'number_of_top_slots':2,
            'number_of_mid_slots':4,
            'number_of_slots':6,
            'number_of_text_slots':2
        },
        'anchored': {
            'text_field':False,
            'number_of_top_slots':3,
            'number_of_mid_slots':2,
            'number_of_slots':7,
            'number_of_text_slots':2
        },
        'sailing': {
            'text_field':True,
            'number_of_top_slots':4,
            'number_of_mid_slots':5,
            'number_of_slots':13,
            'number_of_text_slots':2
        },
        'motoring': {
            'text_field':False,
            'number_of_top_slots':4,
            'number_of_mid_slots':5,
            'number_of_slots':13,
            'number_of_text_slots':2
        }
    },
##########################################################################
## Screen content
##########################################################################
    'loading': {},
    'alarm': {},
    'default': {},

#################################################
## Moored        ################################
#################################################  
    'moored': {
        # Top row (large text, max number_of_top_slots
        'environment.wind.angleApparent': {
            'label': 'AWA',
            'unit': '°',
            'conversion': 'rad',
            'max_age': 240
        },
        #2
        'environment.wind.speedApparent': {
            'label': 'AWS',
            'unit': 'm/s',
            'conversion': False,
            'max_age': 240
        },
        #3
# Empty

        # Mid rows (smaller text), max number_of_mid_slots
        #1,1
        'environment.depth.belowTransducer': {
            'label': 'Depth',
            'unit': 'm',
            'conversion': False,
            'max_age': 240
        },
        #1,2
        'design.beam': {
            'label': 'Beam',
            'unit': 'm',
            'conversion': '.x',
            'max_age': 240
        },
        #1,3
        'design.airHeight': {
            'label': 'Hight',
            'unit': 'm',
            'conversion': '.x',
            'max_age': 240
        },
        #1,4
        'sensors.gps.fromBow': {
            'label': 'GPS from bow',
            'unit': 'm',
            'conversion': '.x',
            'max_age': 240
        },
  
        ################## Text fields
        'environment.outside.pressure.prediction.front.prognose': {
            'label': 'Overview:',
            'unit': ' ',
            'conversion': False,
            'max_age': 240
        },
        'environment.outside.pressure.prediction.front.tendency': {
            'label': 'Tendency:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
    'environment.outside.pressure.prediction.front.wind': {
            'label': 'Wind change:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
        'environment.outside.pressure.system': {
            'label': 'Systems:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
    'environment.outside.pressure.trend.tendency': {
            'label': 'Baro Change:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
        'environment.outside.pressure.prediction.season': {
            'label': 'Prognosis:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
        'environment.outside.pressure.prediction.beaufort.description': {
            'label': 'Wind:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
        'environment.outside.pressure.prediction.quadrant': {
            'label': 'Prognosis:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        }
   },
   
#################################################
## Anchor        ################################
#################################################    
   'anchored': {
        # Top row (large text, max number_of_top_slots
        #1
       'navigation.anchor.currentRadius': {
            'label': 'Anchor',
            'unit': 'm',
            'conversion': 'm',
            'max_age': 30
        },

       #2
        'environment.depth.belowTransducer': {
            'label': 'Depth',
            'unit': 'm',
            'conversion': 'm',
            'max_age': 240
        },
       #3
        'environment.wind.speedApparent': {
            'label': 'AWS',
            'unit': 'm/s',
            'conversion': '.x',
            'max_age': 240
        },
        
        # Mid rows (smaller text), max number_of_mid_slots
        #1,1
        'environment.outside.temperature': {
            'label': 'Outside',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 240
        },
        #1,2
        'design.beam': {
            'label': 'Beam',
            'unit': 'm',
            'conversion': '.x',
            'max_age': 240
        },
        #1,3
        'design.airHeight': {
            'label': 'Hight',
            'unit': 'm',
            'conversion': '.x',
            'max_age': 240
        },
        #1,4
        'sensors.gps.fromBow': {
            'label': 'GPS from bow',
            'unit': 'm',
            'conversion': '.x',
            'max_age': 240
        },
        
        #2,1
        'environment.wind.speedMax': {
            'label': 'WS Max',
            'unit': 'm/s',
            'conversion': '.x',
            'max_age': 240
        },
        

 
        ################## Text fields  #################
        'environment.outside.pressure.prediction.front.prognose': {
            'label': 'Overview:',
            'unit': ' ',
            'conversion': False,
            'max_age': 240
        },
        'environment.outside.pressure.prediction.front.tendency': {
            'label': 'Tendency:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
	'environment.outside.pressure.prediction.front.wind': {
            'label': 'Wind change:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
        'environment.outside.pressure.system': {
            'label': 'Systems:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
	'environment.outside.pressure.trend.tendency': {
            'label': 'Baro Change:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },	
        'environment.outside.pressure.prediction.season': {
            'label': 'Prognosis:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
        'environment.outside.pressure.prediction.beaufort.description': {
            'label': 'Wind:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
        'environment.outside.pressure.prediction.quadrant': {
            'label': 'Prognosis:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        }
   },
   
#################################################
## Sailing       ################################
#################################################    
  'sailing': {
        # Top row (large text, max number_of_top_slots
        #1
	'navigation.speedOverGround': {
            'label': 'SOG',
            'unit': 'kn',
            'conversion': 'm/s',
            'max_age': 240
        },
        #2
        'navigation.courseOverGroundTrue': {
            'label': 'COG',
            'unit': '°',
            'conversion': 'rad',
            'max_age': 240
        },
        #3
        'navigation.courseRhumbline.crossTrackError': {
            'label': 'XTE',
            'unit': 'm',
            'conversion': '.x',
            'max_age': 240
        },
        
        #4
        'environment.wind.directionTrue': {
            'label': 'GWA',
            'unit': '°',
            'conversion': 'rad',
            'max_age': 240
        },
        
        # Mid rows (smaller text), max number_of_mid_slots
        #1,1
        'environment.wind.angleApparent': {
            'label': 'AWA',
            'unit': '°',
            'conversion': 'rad',
            'max_age': 240
        },
        #1,2
        'environment.wind.speedApparent': {
            'label': 'AWS',
            'unit': 'm/s',
            'conversion': '.x',
            'max_age': 240
        },
        #1,3
        'environment.wind.speedMax': {
            'label': 'WSM',
            'unit': 'm/a',
            'conversion': '.x',
            'max_age': 240
        },
        
        #1,4
        'environment.wind.speedMaxPeriodAverage': {
            'label': 'WSM PA',
            'unit': 'm/s',
            'conversion': '.x',
            'max_age': 240
        },
        
        #1,5
        'environment.wind.speedPeriodAverage': {
            'label': 'WS PA',
            'unit': 'm/s',
            'conversion': '.x',
            'max_age': 240
        },

        #2,1
        'environment.wind.speedPeriodMax': {
            'label': 'WS PAM',
            'unit': 'm/s',
            'conversion': '.x',
            'max_age': 240
        },
        #2,2
        'environment.forecast.wind.speed': {
            'label':'For GWS',
            'unit' : 'm/s',
            'conversion': None,
            'max_age':10800
        },
        
        #2,3
        'environment.forecast.wind.direction': {
            'label': 'For GWD',
            'unit': '°',
            'conversion': 'rad',
            'max_age': 10800
        },
        
        #2,4
        'environment.forecast.weather': {
            'label':'Forcast',
            'unit' : ' ',
            'conversion' : None,
            'max_age':10800
        },
        
        
        ################## Text fields
        'environment.outside.pressure.prediction.front.prognose': {
            'label': 'Overview:',
            'unit': ' ',
            'conversion': False,
            'max_age': 240
        },
        'environment.outside.pressure.prediction.front.tendency': {
            'label': 'Tendency:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
	'environment.outside.pressure.prediction.front.wind': {
            'label': 'Wind change:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
        'environment.outside.pressure.system': {
            'label': 'Systems:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
	'environment.outside.pressure.trend.tendency': {
            'label': 'Baro Change:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },	
        'environment.outside.pressure.prediction.season': {
            'label': 'Prognosis:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
        'environment.outside.pressure.prediction.beaufort.description': {
            'label': 'Wind:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
        'environment.outside.pressure.prediction.quadrant': {
            'label': 'Prognosis:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        }
    },
    
#################################################
## Motoring       ###############################
#################################################    
    'motoring': {
                # Top row (large text, max number_of_top_slots
        #1
	'navigation.speedAverage ': {
            'label': 'Avg SOG',
            'unit': 'kn',
            'conversion': 'm/s',
            'max_age': 240
        },
        #2
        'environment.wind.speedPeriodAverage': {
            'label': 'Avg GWS',
            'unit': 'm/s',
            'conversion': None,
            'max_age': 240
        },
        #3
        'environment.wind.speedMax': {
            'label': 'Max GWS',
            'unit': 'm/s',
            'conversion': None,
            'max_age': 240
        },
        
        #4
        'environment.wind.directionTrue': {
            'label': 'GWA',
            'unit': '°',
            'conversion': 'rad',
            'max_age': 240
        },
        
        # Mid rows (smaller text), max number_of_mid_slots
        #1,1
        'environment.outside.temperature': {
            'label': 'Outside',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 240
        },
        #1,2
        'environment.inside.mainCabin.temperature': {
            'label': 'Inside',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 240
        },
        #1,3
        'environment.wind.angleApparent': {
            'label': 'AWA',
            'unit': '°',
            'conversion': 'rad',
            'max_age': 240
        },
        
        #1,4
        'electrical.solar.279.controllerMode': {
            'label': 'PV 1 Mode',
            'unit': ' ',
            'conversion': None,
            'max_age': 240
        },
        
        #1,5
        'electrical.solar.279.panelPower': {
            'label': 'PV 1 Power',
            'unit': 'W',
            'conversion': '.x',
            'max_age': 240
        },

        #2,1
        'environment.forecast.temperature': {
            'label': 'Fore Temp',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 10800
        },
        #2,2
        'environment.forecast.wind.speed': {
            'label':'For GWS',
            'unit' : 'm/s',
            'conversion': None,
            'max_age':10800
        },
        
        #2,3
        'environment.forecast.wind.direction': {
            'label': 'For GWD',
            'unit': '°',
            'conversion': 'rad',
            'max_age': 10800
        },
        
        #2,4
        'environment.forecast.weather': {
            'label':'Forcast',
            'unit' : ' ',
            'conversion' : None,
            'max_age':10800
        },
        
        
        ################## Text fields
        'environment.outside.pressure.prediction.front.prognose': {
            'label': 'Overview:',
            'unit': ' ',
            'conversion': False,
            'max_age': 240
        },
        'environment.outside.pressure.prediction.front.tendency': {
            'label': 'Tendency:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
	'environment.outside.pressure.prediction.front.wind': {
            'label': 'Wind change:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
        'environment.outside.pressure.system': {
            'label': 'Systems:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
	'environment.outside.pressure.trend.tendency': {
            'label': 'Baro Change:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },	
        'environment.outside.pressure.prediction.season': {
            'label': 'Prognosis:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
        'environment.outside.pressure.prediction.beaufort.description': {
            'label': 'Wind:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
        'environment.outside.pressure.prediction.quadrant': {
            'label': 'Prognosis:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        }
    }  
}
