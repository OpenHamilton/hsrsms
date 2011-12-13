#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


import re
import time

from rapidsms.apps.base import AppBase

from hammersms.models import StopTime, Trip, Route, Stop

class App(AppBase):
    ''' Handles recieving an SMS from the client

    Expected format is 'HSR stopnum busnum' or 'HSR stopnum'
    e.g. HSR 1234 52A or HSR 1234

    Parses input responds with an SMS that contains the times when
    the bus will be available.
    e.g.
    HSR Next bus 10 min, 2nd bus 15 min, 3rd bus 30 min
    or
    HSR Next Rte 1A 10 min, Rte 2 15 min, Rte 4 17 min.
    Use HSR 1234 1A for more King.  Use 1234 2 for more Barton
    '''

    def handle(self, message):
        '''Receives incoming SMS message and parses it to formulate response
        '''

        HELP_MSG = 'Usage: \'HSR stopnumber (bus)\'\n Ex. \'HSR 3001\'\nor \'HSR 3001 5C\''
        USER_ID = 'HSR' # prepended to text message
        DISP_MAX = 3 # maximum bus stop times displayed

        msg = message.raw_text.strip().upper();

        # implement help functionality here 
        if(msg == 'HELP' or msg == 'HELP.'):
            message.respond(HELP_MSG)
            return

        # parse sms into components.  If nothing is matched than the SMS is invalid
        # match = re.match("^(?:" + userid + ")[ -_]*(?P<stop>\d{4})(?:[ \-_]+(?P<bus>[0-9A-Z]{1,4}))?$",msg,0) #Regex for 4 digits, use this with actual HSR data
        match = re.match("^(?:" + USER_ID + ")[ \-_]*(?P<stop>[^ ]+)(?:[ \-_]+(?P<bus>[0-9A-Z]{1,4}))?$",msg,0)

        if(match == None):
            message.respond('Invalid request. Text \'help\' for more options.')
            return

        stop = match.group('stop')
        bus = match.group('bus')

        # retrieve django filtered QuerySet objects
        stoptimes_obj = StopTime.objects.filter(stop__stop_id__contains=stop)

        # If a bus is given find the route
        route_obj = []
        if bus:
            route_obj = self.get_bus_route(bus)
            if not route_obj:
                resp = 'Invalid bus entry: ' + bus
                message.respond(resp)
                return


        print '\n' + str(stoptimes_obj[1]) + '\n'

        # convert query objects into time structures
        stoptimes = []
        for stoptime_obj in stoptimes_obj:
            time_tmp = time.strptime(str(stoptime_obj), '%H:%M:%S')
            stoptimes.append(time_tmp)

        current_time = time.localtime()

        # Formulate response

        resp = ''
        for stoptime in stoptimes:
            resp += time.strftime('%H:%M:%S', stoptime)+ '\n'

        #resp = 'stop:' + stop
        if(route_obj):
            resp += ' bus:' + route_obj.route_short_name

        #TODO: implement lookup of bus schedule

        #right now, it's outputting all data for a stopid. It should get the first 3 times for a given stop #
        message.respond(resp)


    def get_bus_route(self, bus):
        '''Query the database to ensure the bus exists. If so return a route
        object associated with that bus. Otherwise return False.
        '''
        # obtain QuerySet from db
        query_obj = Route.objects.filter(route_short_name=bus)
        if query_obj:
            # One query at most should be found (unique identifier)
            route_obj = query_obj[0]
            return route_obj
        else:
            return False

