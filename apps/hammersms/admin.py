#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
'''Models from models.py can be registered here for modification from the
admin interface.'''

from django.contrib import admin

from hammersms.models import StopTime, Trip, Route, Stop, Calendar

admin.site.register(Stop)
admin.site.register(StopTime)
admin.site.register(Trip)
admin.site.register(Route)
admin.site.register(Calendar)
