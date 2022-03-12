## Supporting functions to convert and beuify times

import logging
from dateutil.parser import *
from dateutil.tz import *
from datetime import *


logger = logging.getLogger(__name__)

def tconvert(printformat,dtvalue, latlon=None):
	
	logger.debug("Date/Time to convert: " + str(dtvalue))
##	dt=parse(dtvalue)
##	dt=datetime.fromisoformat(str(dtvalue[0:len(dtvalue)-1]))
	logger.debug("Data/Time after convert:" + dtvalue.strftime(printformat))
	return dtvalue.strftime(printformat)
