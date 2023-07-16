import os
from PIL import Image,ImageDraw,ImageFont
import logging
import datetime
import dateutil.parser
import time
import math
import timeinterval
import timeconverter
import alarm
import threading as th
import config
from config import dashboard
#from convert import convert_value

logger = logging.getLogger(__name__)

fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets')

display_font=os.path.join(str(fontdir), str(dashboard['assets']['display_font']))
body_font=os.path.join(fontdir, str(dashboard['assets']['body_font']))


top_row_meta_font = ImageFont.truetype(display_font, int(dashboard['fontsizes']['top_row_meta']))
mid_row_meta_font = ImageFont.truetype(display_font, int(dashboard['fontsizes']['mid_row_meta']))
top_row_value_font = ImageFont.truetype(body_font, int(dashboard['fontsizes']['top_row_value']))
mid_row_value_font = ImageFont.truetype(body_font, int(dashboard['fontsizes']['mid_row_value']))
text_field_font = ImageFont.truetype(body_font, int(dashboard['fontsizes']['text_field']))
alertfont = ImageFont.truetype(body_font, int(dashboard['fontsizes']['alarm']))
##

splash = Image.open(os.path.join(fontdir, dashboard['assets']['splash']))

class Draw:
    def __init__(self, target):
        self.target = target
        self.display = None
        self.navigation_state = None
        self.expected_flush_time = 0
        self.values = {}
        self.drawing = False
        self.last_time = self.get_time()
        self.offset_x = 0
        self.offset_y = 0
        self.timer = None
        self.info_message = None
        self.alarm_mode = False
        self.alarmhandler=alarm.Alarmhandler(alertfont,target.width,target.height)

    def set_display(self, display):
        temp_display=display

## New state change, but not alarm
        if display != "alarm" :
            self.navigation_state=display

## Show alarm screen if alarm
        if self.alarmhandler.has_active_alarm() or display=="alarm":
            temp_display = "alarm"

## Alarm has stopped. Revert back to original
        if (not self.alarmhandler.has_active_alarm()) and self.display=="alarm" :
            temp_display = self.navigation_state

## No change in displays, just return
        if self.display == temp_display:
            return
        
        logger.debug("Switching to {} display mode".format(temp_display))
        self.display = temp_display
        self.variable_loop()
        self.prepare_display()
        self.draw_frame()

    def get_paths(self):
        if self.display == None :
            return ('navigation.state')  #Bug as display is non on error
        paths = list(dashboard[str(self.display)])
        paths.append('navigation.state')
        if dashboard['layout']['alarm_screen']:
            paths.append('notifications.*')
        logger.debug("Paths subscribed to:" + str(paths))
        return paths

    def show_message(self, msg):
        image = Image.new('1', (int(self.target.width / 2), int(self.target.height / 2)), 1)
        draw = ImageDraw.Draw(image)
        draw.text((int(self.target.width / 2), int(self.target.height / 2)), msg, font=mid_row_value_font)
        self.target.draw(image)
        self.draw_frame()

    def set_info_message(self,msg):
        self.info_message = msg
 
 #Info message is a message in the footer between the status and time.It can be used for various purposes such as showing new NAVTEX messages
    def show_info_message(self, msg=None):
        self.info_message = msg
        if msg :
            time_width = dashboard['layout']['time_width']
            time_height = dashboard['layout']['time_height']
            startx=time_width+dashboard['layout']['space_edges'] 
            endx=self.target.width-time_width-dashboard['layout']['space_edges']-50
            image = Image.new('1', (endx-startx, time_height), 1)
            draw = ImageDraw.Draw(image)                     
            draw.text((0, 0), msg, font=mid_row_value_font)
            self.target.draw(image,startx+50,self.target.height-time_height-dashboard['layout']['space_edges'])

    def update_value(self, msg, timestamp):
        self.values[msg['path']] = {
            'value': msg['value'],
            'time': dateutil.parser.parse(timestamp),
            'rendered': False
        }
    
    def update_alarm(self,msg,timestamp):
        (self.alarm_mode,alarm_change)=self.alarmhandler.update_alarm(msg,timestamp)
        return (self.alarm_mode,alarm_change)
    
    def alarm_active(self):
        return self.alarmhandler.has_active_alarm()

    def prepare_slot_data(self, path):
        if not path in self.values:
            # Haven't received data for this slot
            self.values[path] = {
                'value': None,
                'time': datetime.datetime.now(datetime.timezone.utc),
                'rendered': False
            }
        since_update = (datetime.datetime.now(datetime.timezone.utc) - self.values[path]['time']).total_seconds()
        if dashboard[str(self.display)][path] and since_update > dashboard[str(self.display)][path]['max_age']:
            #print("Setting path {} as stale".format(path))
            logger.info("Setting path {} as stale".format(path))
            # Stale value, switch to n/a
            self.values[path] = {
                'value': None,
                'time': datetime.datetime.now(datetime.timezone.utc),
                'rendered': False
            }

    def convert_value(self, value, conversion = None):
        if value == None:
            return 'N/A'
        logger.debug('Converting value:'+str(value))
        if not conversion:
            return str(value)
        if conversion == 'K_C':
            return "{0:.1f}".format(value - 273.15)
        if conversion == 'm_m':
            return "{0:.1f}".format(value)
        if conversion == 'int_str':
            return str(int(value))
        if conversion == '%':
            return str(int(value * 100))
        if conversion == 'Pa_hPa':
            return str(int(value / 100))
        if conversion == 'rad_deg':
            return str(int(math.degrees(value)))
        if conversion == 'm/s_knots':
            return "{0:.1f}".format(value * 1.944)
        if conversion == 'm_NM':
            return "{0:.1f}".format(value / 1852)
        if conversion == 'Z_local_2':
            return tconvert('%H:%M',value)
        if conversion == 'Z_local_3':
            return tconvert('%H:%M:%S',value)
        if conversion == '.x':
            return "{0:.1f}".format(value)
        if conversion == '.xx':
            return "{0:.2f}".format(value)
        ##Older conversions for backward compability
        if conversion == 'Pa':
            return str(int(value / 100))
        if conversion == 'rad':
            return str(int(math.degrees(value)))
        if conversion == 'm/s':
            return "{0:.1f}".format(value * 1.944)
        if conversion == 'K':
            return "{0:.1f}".format(value - 273.15)
        if conversion == 'm':
            return "{0:.1f}".format(value)
        ## Default if no conversions was found
        return 'Undef conv.'
    
    def draw_slot(self, path):
        self.prepare_slot_data(path)
        if self.values[path]['rendered'] == True:
            # No need to re-render
            return
        slot = list(dashboard[str(self.display)]).index(path)
        label = dashboard[str(self.display)][path]['label']
        logger.debug("Value to print:" + str(self.values[path]['value']))
        #value = convert_value(self.values[path]['value'], dashboard[str(self.display)][path]['conversion'])
        value = self.convert_value(self.values[path]['value'], dashboard[str(self.display)][path]['conversion'])
        logger.debug('Value to be printed:' + value)

        if dashboard['layout'][self.display]['number_of_slots'] == 0:
            # No need to continue if thera are no slots to draw
            return

# Draw top row slots
        if slot < dashboard['layout'][self.display]['number_of_top_slots'] and slot < dashboard['layout'][self.display]['number_of_slots'] :   
            height = dashboard['layout']['first_row_height']
            width = int((self.target.width - dashboard['layout']['space_edges']) / dashboard['layout'][self.display]['number_of_top_slots'])
            meta_font = top_row_meta_font
            value_font = top_row_value_font
            slot_pos = slot
            top_margin = dashboard['layout']['space_edges']
            left_margin = slot_pos * width + dashboard['layout']['space_edges']
            value_margin = 30
            unit_margin = 75
# Draw middle row slots (the smaller ones)
        elif slot < dashboard['layout'][self.display]['number_of_slots']:
            height = dashboard['layout']['other_row_height']
            width = int((self.target.width - dashboard['layout']['space_edges']) / dashboard['layout'][self.display]['number_of_mid_slots'])
            meta_font = mid_row_meta_font
            value_font = mid_row_value_font
            slot_pos = slot - dashboard['layout'][self.display]['number_of_top_slots']
            # Draw first row or second of middle slots. This should be generalized!!
            if slot < (dashboard['layout'][self.display]['number_of_top_slots'] + dashboard['layout'][self.display]['number_of_mid_slots']):
                slot_pos = slot - dashboard['layout'][self.display]['number_of_top_slots']
                top_margin = dashboard['layout']['first_row_height'] + dashboard['layout']['space_row']
            else:
                slot_pos = slot - dashboard['layout'][self.display]['number_of_top_slots']-dashboard['layout'][self.display]['number_of_mid_slots']
                top_margin = dashboard['layout']['space_edges'] + dashboard['layout']['first_row_height'] + 2*dashboard['layout']['space_row'] + height
            left_margin = slot_pos * width + dashboard['layout']['space_edges']
            value_margin = 20
            unit_margin = 45
        else:
            # Number of slots has been reached (the rest is text field data). Don't draw these.
            return

        image = Image.new('1', (width, height), 1)
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), label.upper(), font=meta_font)
        draw.text((0, value_margin), value, font=value_font)
        if 'unit' in str(dashboard[str(self.display)][path]):
            draw.text((0, unit_margin), dashboard[str(self.display)][path]['unit'], font=meta_font)
        self.target.draw(image, int(left_margin) + self.offset_x, top_margin + self.offset_y)
        self.values[path]['rendered'] = True

    def get_time(self):
        now = datetime.datetime.now() + datetime.timedelta(seconds=self.expected_flush_time)
        return now.strftime(str(dashboard['time_format']))

    def update_time(self):
        
        time_width = dashboard['layout']['time_width']
        time_height = dashboard['layout']['time_height']
        image = Image.new('1', (time_width, time_height), 1)
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), self.get_time(), font=top_row_meta_font)
        self.target.draw(image, self.target.width - dashboard['layout']['space_edges'] - time_width + self.offset_x, self.target.height - dashboard['layout']['space_edges'] - time_height + self.offset_y)

    def prepare_display(self):
        
        label= dashboard['name']
        for path in self.values:
            self.values[path]['rendered'] = False
        image = Image.new('1', (self.target.width, self.target.height), 1)
        draw = ImageDraw.Draw(image)
        
        if self.display == 'loading':
            (iwidth, iheight) = splash.size
            image.paste(splash, (int((self.target.width-iwidth)/2), dashboard['layout']['space_edges']))
            label = dashboard['name']
        
        if self.display and self.display != 'default':
            label = self.display
        
        draw.text((dashboard['layout']['space_edges'] + self.offset_x, self.target.height - dashboard['layout']['time_height'] -dashboard['layout']['space_edges']+ self.offset_y), str(label).upper(), font = top_row_meta_font, fill = 0)

        self.target.draw(image, 0, 0)
        self.draw_frame(True)

    def draw_full_frame(self):
        draw_frame(not(config.partial_update))

    def draw_frame(self, full = False):

        logger.debug("Start draw frame")
# As as default, put the display to sleep according to WaveShare notes
        sendtosleep=True
        
        if self.drawing == True:
            return
        
        self.drawing = True
        self.update_time()

        if self.display == None:
            return  #Connection issues and no status
            
 # Populate all slots based on config if not alarm
        if self.display != 'alarm':
            for path in dashboard[str(self.display)]:
                self.draw_slot(path)
            #Add text field
            if dashboard['layout'][str(self.display)]['text_field']:
                self.draw_text_field()
                
## Draw alermessage between status and time
        self.show_info_message()

## Draw alarm screen if alarm is active
        if self.display == 'alarm':
            logger.debug("Alarm is to be drawn")
            self.target.draw(self.alarmhandler.draw(),0,0)

## Begin drawing to display
        flush_start = time.time()
#        logger.debug('Before flush of display')
 
# Do not put the display into sleep as we expect update soon       
        if self.display == 'loading':
            sendtosleep=False
            
        self.target.flush(full,sendtosleep)

# Wait 10s so we show our cool slash screen and just not flicker..
#        if self.display == 'loading':
#           time.sleep(10)

        logger.debug('After display has been flushed')
        flush_end = time.time()
        if flush_end > flush_start:
            self.expected_flush_time = int(self.expected_flush_time * 0.9 + (flush_end - flush_start) * 0.1)
        self.drawing = False

    def variable_loop(self):
        if (str(self.display) == "sailing") or (str(self.display) == "motoring"):
            # We want to update speed and course frequently
            logger.debug("Moving:Setting update loop to:" + str(config.loop_time_moving))
            self.loop(config.loop_time_moving)
        elif (self.display == "anchored"):
            # Distance to anchor is also somewhat critical value
            logger.debug("Anchor:Setting update loop to:" + str(config.loop_time_anchor))
            self.loop(config.loop_time_anchor)
        elif (self.display == "alarm"):
            logger.debug("Alarm:Setting update loop to:" + str(config.loop_time_alarm))
            self.loop(config.loop_time_alarm)           
        else:
            # If we're not moving it is fine to update less frequently
            logger.debug("Moored:Setting update loop to:" + str(config.loop_time_moored))
            self.loop(config.loop_time_moored)

    def loop(self, refresh_rate):
 #       logger.debug('Entering loop')
        if self.timer:
            logger.debug("Clearing previous timer")
            # Stop previous timer
            self.timer.set()
            self.timer=None
        logger.debug("Setting new refresh rate to {}".format(refresh_rate))
# Redraw frame after 20 seconds to let some data come in to avoid N/As for a full cycle
# however, don't do this for alarms as there is no data and short refresh
        if (self.display != "alarm"):
            S = th.Timer(20.0, self.draw_frame,(not(config.partial_update),))  
            S.start()  

# Start a timer to continously to redraw the screen
        self.timer = timeinterval.start(refresh_rate, self.draw_frame,not(config.partial_update))


    def clear_screen(self):
        self.drawing = True
        self.target.clear_screen()
        logger.debug('Clear_screen')

    def draw_text_field(self):
        image = Image.new('1', (self.target.width-2*dashboard['layout']['space_edges'], dashboard['layout']['text_field_height']), 1)
        draw = ImageDraw.Draw(image)

        number_textslots = dashboard['layout'][str(self.display)]['number_of_text_slots']
        row_space = int(self.target.width-2*dashboard['layout']['space_edges']) / number_textslots
        slot_space = 20

        number_other_value_rows = (dashboard['layout'][self.display]['number_of_slots']-dashboard['layout'][self.display]['number_of_top_slots']) // dashboard['layout'][self.display]['number_of_mid_slots']
        text_field_offset = dashboard['layout']['text_field_offset']

        text_slot = 0
        for path in dashboard[str(self.display)]:
            slot = list(dashboard[str(self.display)]).index(path)
            if slot >= dashboard['layout'][str(self.display)]['number_of_slots'] :
                label = dashboard[str(self.display)][path]['label']
                #value = convert_value(self.values[path]['value'], dashboard[str(self.display)][path]['conversion'])
                value = self.convert_value(self.values[path]['value'], dashboard[str(self.display)][path]['conversion'])
                drawtext = label + value
                draw.text(((text_slot%number_textslots)*row_space, (text_slot//number_textslots)*slot_space), drawtext, font=text_field_font)
                text_slot += 1
                self.values[path]['rendered'] = True

        self.target.draw(image, dashboard['layout']['space_edges'],text_field_offset)
