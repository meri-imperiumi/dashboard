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

#	timezone=str(dashboard['TZ_default_name'])
	timeoffset=int(dashboard['TZ_default_offset'])
	
	#utc_datetime=pytz.utc.localize(dtvalue)
	delta=timedelta(seconds=timeoffset)
	logger.debug("Date/Time to convert: " + str(dtvalue))
	local_dtvalue=dtvalue+delta
	
##	dt=parse(dtvalue)
##	dt=datetime.fromisoformat(str(dtvalue[0:len(dtvalue)-1]))
	logger.debug("Data/Time after convert:" + local_dtvalue.strftime(printformat))
	return local_dtvalue.strftime(printformat)
