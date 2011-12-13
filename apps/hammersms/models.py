#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# encoding=utf-8


from django.db import models

class Route(models.Model):

    def __unicode__(self):
        return self.route_long_name

    route_long_name = models.CharField(max_length=40)
    route_short_name = models.CharField(max_length=4, unique=True)
    route_id = models.CharField(max_length=16, unique=True)

class Trip(models.Model):

    def __unicode__(self):
        return str(self.trip_id)

    route = models.ForeignKey(Route, to_field='route_id')
    trip_id = models.CharField(max_length=16, unique=True)
    calendar = models.ForeignKey(Calendar, to_field='service_id')

class Stop(models.Model):

    def __unicode__(self):
        return self.stop_id

    stop_id = models.CharField(max_length=16, unique=True)

class StopTime(models.Model):

    def __unicode__(self):
        return str(self.arrival_time)

    arrival_time = models.TimeField()
    trip = models.ForeignKey(Trip, to_field='trip_id')
    stop = models.ForeignKey(Stop, to_field='stop_id')

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

