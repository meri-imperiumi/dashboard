#from waveshare_epd import epd7in5_V2
import epaperdummy
import logging
from PIL import Image
from config import partial_frame_limit

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
        self.partial_frame_limit = partial_frame_limit
        epd.init()
        self.insleep = False
        epd.Clear()

    def draw(self, image: Image, x: int = 0, y: int = 0):
        assert image.width + x <= epd.width
        assert image.height + y <= epd.height
        self.buffer.paste(image, (x, y))

    def flush(self, full = False, tosleep=True):
        frame_buffer = epd.getbuffer(self.buffer)
        if (full == True) or (self.partial_frames >= self.partial_frame_limit):
            logger.debug('Drawing full frame')
            if self.insleep :
                logger.debug('Wake up from sleep')
  #              epd.init()
                self.insleep = False
            epd.display(frame_buffer)
# Debug , draw frame on screen
#            self.buffer.show()
# End debug
            self.partial_frames = 0
        else:
            #_display_frame_quick(frame_buffer)
            self.partial_frames += 1

#Send display to sleep during normal operation to prolong its life
        if tosleep:
  #          epd.sleep()
            self.insleep = True 
            
    def clear_screen(self):
        if self.insleep :
            logger.debug('Wake up from sleep')
            epd.init()
            self.insleep = False
        epd.Clear()
        epd.sleep()
