import logging
import datetime
import dateutil.parser
import time
import math
import timeconverter

logger = logging.getLogger(__name__)

def convert_value(self, value, conversion = None):
    if value == None:
        return 'N/A'
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
    if conversion == 'Z_local':
        dt=datetime.fromisoformat(value[0:len(value)-1])
        #Need to set to local time!
        return dt.strftime('%H:%M')
    if conversion == '.x':
        return "{0:.1f}".format(value)

    return 'Undef conv.'
