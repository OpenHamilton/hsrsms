import re
import time

from rapidsms.apps.base import AppBase

from hammersms.models import StopTime, Trip, Route, Stop

class App(AppBase):

   # Handles recieving an SMS from the client
   #
   # Expected format is 'HSR stopnum busnum' or 'HSR stopnum'
   # e.g. HSR 1234 52A or HSR 1234
   #
   # Parses input responds with an SMS that contains the times when
   # the bus will be available.
   # e.g.
   # HSR Next bus 10 min, 2nd bus 15 min, 3rd bus 30 min
   # or
   # HSR Next Rte 1A 10 min, Rte 2 15 min, Rte 4 17 min.
   # Use HSR 1234 1A for more King.  Use 1234 2 for more Barton
    def handle(self, message):
      HELP_MSG = 'Usage: \'HSR stopnumber (bus)\'\n Ex. \'HSR 3001\'\nor \'HSR 3001 5C\''
      USER_ID = 'HSR' # prepended to text message
      DISP_MAX = 3 # maximum bus stop times displayed

      msg = message.raw_text.strip().upper();

      # implement help functionality here 
    if(msg == 'HELP' or msg == 'HELP.'):
        message.respond(HELP_MSG)
        return

      # parse sms into components.  If nothing is matched than the SMS is invalid
#match = re.match("^(?:" + userid + ")[ -_]*(?P<stop>\d{4})(?:[ \-_]+(?P<bus>[0-9A-Z]{1,4}))?$",msg,0) #Regex for 4 digits, use this with actual HSR data
    match = re.match("^(?:" + USER_ID + ")[ \-_]*(?P<stop>[^ ]+)(?:[ \-_]+(?P<bus>[0-9A-Z]{1,4}))?$",msg,0)

    if(match == None):
        message.respond('Invalid request. Text \'help\' for more options.')
        return

    stop = match.group('stop')
    bus = match.group('bus')

    # retrieve django filtered QuerySet objects
    stoptimes_obj = StopTime.objects.filter(stop__stop_id__contains=stop)

    print '\n' + str(stoptimes_obj[1]) + '\n'

    # convert query objects into time structures
    stoptimes = []
    for stoptime_obj in stoptimes_obj:
        time_tmp = time.strptime(str(stoptime_obj), '%H:%M:%S')
        stoptimes.append(time_tmp)


    current_time = time.localtime()

    # Formulate response

    resp = ''
    for item in stoptimes:
        resp += str(item)+ '\n'

    #resp = 'stop:' + stop
    if(bus):
        resp += ' bus:' + bus

    #TODO: implement lookup of bus schedule

    #right now, it's outputting all data for a stopid. It should get the first 3 times for a given stop #
    message.respond(resp)

