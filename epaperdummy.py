# *****************************************************************************
# * | File        :	  epaperdummy
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2021-12-20
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

# This module is a dummy e-paper module having the same functions
# but draws on the screen instead of drawing to an e-paper display
# This is useful when developing and testing


import logging
#from waveshare_epd import epdconfig
#from . import epdconfig

import time

# Display resolution
EPD_WIDTH       = 800
EPD_HEIGHT      = 480

logger = logging.getLogger(__name__)

class EPD:
    def __init__(self):
#        self.reset_pin = epdconfig.RST_PIN
#        self.dc_pin = epdconfig.DC_PIN
#        self.busy_pin = epdconfig.BUSY_PIN
#        self.cs_pin = epdconfig.CS_PIN
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

    # Hardware reset
    def reset(self):
        logger.debug("Display reset")

    def send_command(self, command):
        logger.debug("Send command")

    def send_data(self, data):
        logger.debug("Send data")

    def send_data2(self, data):
        logger.debug("Send data2")

    def ReadBusy(self):
        logger.debug("e-Paper busy")
        busy = 0
        while(busy == 0):
            self.send_command(0x71)
            busy = 1
#        epdconfig.delay_ms(20)
            time.sleep(0.02)

        logger.debug("e-Paper busy release")
        
    def SetLut(self, lut_vcom, lut_ww, lut_bw, lut_wb, lut_bb):
        logger.debug("SetLut")

    def init(self):
        return 0
 
    def getbuffer(self, image):
        img = image
        imwidth, imheight = img.size
        if(imwidth == self.width and imheight == self.height):
            img = img.convert('1')
        elif(imwidth == self.height and imheight == self.width):
            # image has correct dimensions, but needs to be rotated
            img = img.rotate(90, expand=True).convert('1')
        else:
            logger.warning("Wrong image dimensions: must be " + str(self.width) + "x" + str(self.height))
            # return a blank buffer
            return [0x00] * (int(self.width/8) * self.height)

        buf = bytearray(img.tobytes('raw'))
        # The bytes need to be inverted, because in the PIL world 0=black and 1=white, but
        # in the e-paper world 0=white and 1=black.
        for i in range(len(buf)):
            buf[i] ^= 0xFF
        return image

    def display(self, image):
        image.show()
        time.sleep(0.1)
#        epdconfig.delay_ms(100)

    def Clear(self):
        buf = [0x00] * (int(self.width/8) * self.height)
        logger.debug("Clear Display")

    def sleep(self):
        logger.debug("Display sleep")
 #       epdconfig.delay_ms(2000)
        time.sleep(2)

### END OF FILE ###
