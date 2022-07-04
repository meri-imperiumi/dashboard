# -*- coding:utf-8 -*-

import logging

signalk_host = 'localhost'
#signalk_host = 'raspberrypi400.local'
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
# As per WaveShare notes, a full refresh time should not be lower than 180s
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
    'name': 'Elinor',

    'assets': {
        'display_font': 'nasalization-rg.otf',
        'body_font': 'Eurostile.ttf',
        'splash': 'signalK.bmp'
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
        'time_width':80,
        'time_height':40,
## If alarm_screen is set to True, the program will listen to alarms
## and switch to an alarm screen and show the alarms until they are canceled
         'alarm_screen':True,




        'loading': {
            'text_field':False,
            'number_of_top_slots':0,
            'number_of_mid_slots':0,
            'number_of_slots':0,
            'number_of_text_slots':0
        },
        'default': {
            'text_field':False,
            'number_of_top_slots':0,
            'number_of_mid_slots':0,
            'number_of_slots':0,
            'number_of_text_slots':0
        },
        'moored': {
            'text_field':True,
            'number_of_top_slots':3,
            'number_of_mid_slots':4,
            'number_of_slots':7,
            'number_of_text_slots':2
        },
        'anchored': {
            'text_field':True,
            'number_of_top_slots':4,
            'number_of_mid_slots':5,
            'number_of_slots':10,
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
            'text_field':True,
            'number_of_top_slots':4,
            'number_of_mid_slots':5,
            'number_of_slots':10,
            'number_of_text_slots':2
        },
        'alarm': {
            'text_field':False,
            'number_of_top_slots':0,
            'number_of_mid_slots':0,
            'number_of_slots':0,
            'number_of_text_slots':0
        }
    },

## Screen content
    'loading': {},
    'alarm': {},
    'default': {},
   'moored': {
        # Top row (large text, max number_of_top_slots
        'environment.outside.temperature': {
            'label': 'Temp',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 240
        },
        #2
        'environment.outside.pressure': {
            'label': 'Baro',
            'unit': 'hPa',
            'conversion': 'Pa',
            'max_age': 240
        },
        #3
        'environment.outside.relativeHumidity': {
            'label': 'Humid',
            'unit': '%',
            'conversion': '%',
            'max_age': 240
        },
        # Mid rows (smaller text), max number_of_mid_slots
        'environment.inside.temperature': {
            'label': 'Inside',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 240
        },
        #1,2
        'environment.inside.refrigerator.temperature': {
            'label': 'Fridge',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 240
        },
        #1,3
        'environment.inside.freezer.temperature': {
            'label': 'Champagne',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 240
        },
        #1,4
        'environment.inside.engineRoom.temperature': {
            'label': 'Beer',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 240
        }
        #1,5
        #2,1
        #2,2
        #2,3
        #2,4
        #2,5
        
   },
   'anchored': {
        # Top row (large text, max number_of_top_slots
        'navigation.anchor.currentRadius': {
            'label': 'Anchor',
            'unit': 'm',
            'conversion': 'm',
            'max_age': 30
        },
        #2
        'environment.outside.temperature': {
            'label': 'Temp',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 240
        },
        #3
        'environment.outside.pressure': {
            'label': 'Baro',
            'unit': 'hPa',
            'conversion': 'Pa',
            'max_age': 240
        },
        # Mid rows (smaller text), max number_of_mid_slots
        'environment.outside.relativeHumidity': {
            'label': 'Humid',
            'unit': '%',
            'conversion': '%',
            'max_age': 240
        },
        #1,2
        'environment.inside.temperature': {
            'label': 'Inside',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 240
        },
        #1,3
        'environment.inside.refrigerator.temperature': {
            'label': 'Fridge',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 240
        },
        #1,4
        'environment.inside.freezer.temperature': {
            'label': 'Champagne',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 240
        }
        #1,5
        #2,1
        #2,2
        #2,3
        #2,4
        #2,5
    # Text Fields
   },
  'sailing': {
        # Top row (large text, max number_of_top_slots
        'navigation.speedOverGround': {
            'label': 'SOG',
            'unit': 'kn',
            'conversion': 'm/s',
            'max_age': 30
        },
        #2
        'navigation.courseOverGroundTrue': {
            'label': 'COG',
            'unit': '°',
            'conversion': 'rad',
            'max_age': 30
        },
        #3
        'environment.outside.pressure': {
            'label': 'Baro',
            'unit': 'hPa',
            'conversion': 'Pa',
            'max_age': 240
        },
        #4
            'environment.outside.relativeHumidity': {
            'label': 'Humid',
            'unit': '%',
            'conversion': '%',
            'max_age': 240
        },
        # Mid rows (smaller text), max number_of_mid_slots
        'environment.outside.temperature': {
            'label': 'Outside',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 240
        },
        #1,2
        'environment.inside.relativeHumidity': {
            'label': 'Humid',
            'unit': '%',
            'conversion': '%',
            'max_age': 240
        },
        #1,3
        'environment.inside.temperature': {
            'label': 'Inside',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 240
        },
        #1,4
        'environment.inside.freezer.temperature': {
            'label': 'Champagne',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 240
        },
        #1,5
        'environment.depth.belowTransducer': {
            'label': 'Depth',
            'unit': 'm',
            'conversion': 'm',
            'max_age': 30
        },
        #2.1
        'environment.outside.pressure.1hr': {
            'label': 'Baro 1hr',
            'unit': 'hPa',
            'conversion': 'Pa',
            'max_age': 240
        },
        #2,2
        'environment.forecast.wind.direction': {
            'label': 'Pred TWD',
            'unit': '°',
            'conversion': 'rad',
            'max_age': 11000
        },
        #2,3
        'environment.forecast.wind.speed': {
            'label': 'Pred TWS',
            'unit' : 'm/s',
            'conversion':'.x',
            'max_age':11000
        },
        #2,4
        'environment.forecast.description': {
            'label': 'Forecast',
            'unit' : '',
            'conversion': None,
            'max_age':11000
        },
        #2,5
        ## Text field
        'environment.outside.pressure.prediction.front.prognose': {
            'label': 'Overview:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
        'environment.outside.pressure.prediction.front.tendency': {
            'label': 'Tendency:',
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
        'environment.outside.pressure.prediction.pressureOnly': {
            'label': 'Prognosis:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
        'environment.outside.pressure.prediction.season': {
            'label': 'Weather:',
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
        'environment.outside.pressure.prediction.beaufort.description': {
            'label': 'Wind:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        },
        'environment.outside.pressure.prediction.quadrant': {
            'label': 'Wind quadrant:',
            'unit': 'hPa',
            'conversion': False,
            'max_age': 240
        }
    },
    'motoring': {
    }  
}
