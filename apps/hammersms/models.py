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

