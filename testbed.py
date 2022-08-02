#import logging
#import convert

import config
from config import dashboard

from dateutil.parser import *
from dateutil.tz import *
from datetime import *

utc_time="2022-08-01T19:34:49.000Z"

print ("Tjolahopp")

timeoffset=int(dashboard['TZ_default_offset'])
printformat="%H:%M:%S %z"

#local_tz="Europe/Stockholm"
#local_tz="W. Europe Standard Time"

#print (available_timezones())

l_zone=timezone(timedelta(seconds=timeoffset))

delta=timedelta(seconds=timeoffset)
#dtvalue=datetime.fromisoformat(utc_time)
dtvalue=datetime.fromisoformat(utc_time[0:len(utc_time)-1] + "+00:00")

print ("Date/Time to convert: " + str(dtvalue))
print ("Timezone:" + str(dtvalue.tzinfo))
#local_dtvalue=dtvalue+delta



local_dtvalue=dtvalue.astimezone(l_zone)

print ("Data/Time after convert:" + local_dtvalue.strftime(printformat))
