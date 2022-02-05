#from waveshare_epd import epd7in5_V2
import epaperdummy
import logging
from PIL import Image

logger = logging.getLogger(__name__)

#epd = epd4in2.EPD()
#epd = epd7in5_V2.EPD()
epd = epaperdummy.EPD()

class DrawTarget:
    def __init__(self):
        self.buffer = Image.new("1", (epd.width, epd.height), 1)
        self.width = epd.width
        self.height = epd.height
        self.partial_frames = 0
        self.partial_frame_limit = 20
        epd.init()
        epd.Clear()

    def draw(self, image: Image, x: int = 0, y: int = 0):
        assert image.width + x <= epd.width
        assert image.height + y <= epd.height
        self.buffer.paste(image, (x, y))

    def flush(self, full = False):
#        frame_buffer = epd.get_frame_buffer(self.buffer)
        frame_buffer = epd.getbuffer(self.buffer)
        if (full == True) or (self.partial_frames >= self.partial_frame_limit):
            logger.debug('Drawing full frame')
            #epd.display(frame_buffer)
# Debug , draw frame on screen
            frame_buffer.show()
# End debug
            self.partial_frames = 0
        else:
            #_display_frame_quick(frame_buffer)
            self.partial_frames += 1
        #Sleep after loading
        epd.sleep()
            
    def clear_screen(self):
        epd.Clear()
        epd.sleep()
