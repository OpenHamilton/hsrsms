#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# encoding=utf-8
'''The models.py module defines the database relations for custom classes.
'''

from django.db import models

class Route(models.Model):
    '''An example route would be KING. Buses take 'Trips' down routes.
    '''

    def __unicode__(self):
        return self.route_long_name

    route_long_name = models.CharField(max_length=40)
    route_short_name = models.CharField(max_length=15)
    route_id = models.CharField(max_length=16, unique=True)


class Calendar(models.Model):
    '''Models the data found in the calendar.txt GTFS data file. Monday
    through Friday are bools that tell if the stop times for a particular
    trip are for that day. Stop times generally differ for Sat, Sun and
    Holidays.
    '''

    def __unicode__(self):
        return str(self.service_id)

    service_id = models.CharField(max_length=16, unique=True)
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()
    # start_date = YYYYMMDD
    # end_date = YYYYMMDD

class Trip(models.Model):
    '''Trips occur on a selected Routes and occur during specific dates and
    times.
    '''
    def __unicode__(self):
        return str(self.trip_id)

    route = models.ForeignKey(Route, to_field='route_id')
    trip_id = models.CharField(max_length=16, unique=True)
    calendar = models.ForeignKey(Calendar, to_field='service_id')

class Stop(models.Model):
    '''A Stop simply a bus stop.
    '''
    def __unicode__(self):
        return self.stop_id

    stop_id = models.CharField(max_length=16, unique=True) # ie. '2899'

class StopTime(models.Model):
    '''A StopTime corresponds to a specific Stop and the Trip that the bus
    is on.
    '''
    def __unicode__(self):
        return str(self.arrival_time)

    arrival_time = models.TimeField()
    trip = models.ForeignKey(Trip, to_field='trip_id')
    stop = models.ForeignKey(Stop, to_field='stop_id')

