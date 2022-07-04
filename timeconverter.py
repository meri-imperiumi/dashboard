## Supporting functions to convert and beutify times

import logging
from dateutil.parser import *
from dateutil.tz import *
from datetime import *
#import pytz
import config
from config import dashboard


logger = logging.getLogger(__name__)

def tconvert(printformat,dtvalue, latlon=None):

    timeoffset=int(dashboard['TZ_default_offset'])

    delta=timedelta(seconds=timeoffset)
    logger.debug("Date/Time to convert: " + str(dtvalue))
    local_dtvalue=dtvalue+delta

    logger.debug("Data/Time after convert:" + local_dtvalue.strftime(printformat))
    return local_dtvalue.strftime(printformat)
