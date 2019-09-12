import os
from PIL import Image,ImageDraw,ImageFont
import logging
import datetime
import dateutil.parser
import time
import threading
from config import dashboard

fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets')
display48 = ImageFont.truetype(os.path.join(fontdir, dashboard['assets']['display_font']), 48)
display24 = ImageFont.truetype(os.path.join(fontdir, dashboard['assets']['display_font']), 24)
font48 = ImageFont.truetype(os.path.join(fontdir, dashboard['assets']['body_font']), 48)
font24 = ImageFont.truetype(os.path.join(fontdir, dashboard['assets']['body_font']), 24)

class Draw:
    def __init__(self, target):
        self.target = target
        self.display = None
        self.expected_flush_time = 0
        self.values = {}
        self.drawing = False

    def set_display(self, display):
        if self.display != display:
            self.display = display
            self.prepare_display()

    def show_message(self, msg):
        image = Image.new('1', (self.target.width, int(self.target.height / 2)), 1)
        draw = ImageDraw.Draw(image)
        draw.text((20, 50), msg, font=font24)
        self.target.draw(image)
        self.draw_frame()

    def update_value(self, msg, timestamp):
        self.values[msg['path']] = {
            'value': msg['value'],
            'time': dateutil.parser.parse(timestamp),
            'rendered': False
        }

    def prepare_slot_data(self, path):
        if not path in self.values:
            # Haven't received data for this slot
            self.values[path] = {
                'value': 'n/a',
                'time': datetime.datetime.now(datetime.timezone.utc),
                'rendered': False
            }
        since_update = (datetime.datetime.now(datetime.timezone.utc) - self.values[path]['time']).total_seconds()
        if since_update > dashboard[self.display][path]['max_age']:
            # Stale value, switch to n/a
            self.values[path] = {
                'value': 'n/a',
                'time': datetime.datetime.now(datetime.timezone.utc),
                'rendered': False
            }

    def convert_value(self, value, conversion = None):
        if value == 'n/a':
            return value.upper()
        if not conversion:
            return str(value)
        if conversion == 'K':
            return "{0:.1f}".format(value - 273.15)
        if conversion == 'int':
            return str(int(value))
        if conversion == 'Pa':
            return str(int(value / 100))

    def draw_slot(self, path):
        self.prepare_slot_data(path)
        print(path)
        print(self.values[path])
        if self.values[path]['rendered'] == True:
            print("Already rendered")
            # No need to re-render
            return
        slot = list(dashboard[self.display]).index(path)
        label = dashboard[self.display][path]['label']
        value = self.convert_value(self.values[path]['value'], dashboard[self.display][path]['conversion'])

        image = Image.new('1', (int(self.target.width / 3), self.target.height - 60), 1)
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), label.upper(), font=display24)
        draw.text((0, 30), value, font=font48)
        if 'unit' in dashboard[self.display][path]:
            draw.text((0, 85), dashboard[self.display][path]['unit'], font=display24)
        self.target.draw(image, int(self.target.width / 3 * slot), 10)
        self.values[path]['rendered'] = True

    def update_time(self):
        time_width = 80
        time_height = 40
        image = Image.new('1', (time_width, time_height), 1)
        draw = ImageDraw.Draw(image)
        now = datetime.datetime.now() + datetime.timedelta(seconds=self.expected_flush_time)
        draw.text((0, 0), now.strftime(dashboard['time_format']), font=display24)
        self.target.draw(image, self.target.width - time_width, self.target.height - time_height)

    def prepare_display(self):
        for path in self.values:
            self.values[path]['rendered'] = False

        image = Image.new('1', (self.target.width, self.target.height), 1)
        draw = ImageDraw.Draw(image)
        draw.text((10, self.target.height - 40), dashboard['name'].upper(), font = display24, fill = 0)
        self.target.draw(image, 0, 0)
        self.draw_frame()

    def draw_frame(self):
        if self.drawing == True:
            return
        self.drawing = True
        self.update_time()
        for path in dashboard[self.display]:
            self.draw_slot(path)
        flush_start = time.time()
        self.target.flush()
        flush_end = time.time()
        if flush_end > flush_start:
            self.expected_flush_time = self.expected_flush_time * 0.9 + (flush_end - flush_start) * 0.1
        self.drawing = False

    def loop(self):
        self.draw_frame()
        timer = threading.Timer(20.0, self.loop).start()
