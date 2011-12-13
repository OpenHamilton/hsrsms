#!/usr/bin/evn python
# vim: ai ts=4 sts=4 et sw=4

'''Converts the .txt files downloaded by getgtfs.py to .json format.

Notes: This file is temporary. Should be built into syncdb.
'''

import os, re, csv
import django
import simplejson as json

def fixhour(mo):
    h = int(mo.group(0))
    if(h >= 24):
        return str(h - 24)
    return str(h)

# Files included in GTFS data
FILES = ['agency', 'calendar', 'calendar_dates', 'fare_attributes', 'routes', 'shapes', 'stop_times', 'stops', 'trips', 'frequencies']
DIR = 'tmp'

for FILE in FILES:
    path = os.path.join(DIR, FILE + '.txt')
    dest = os.path.join(DIR, FILE + '.json')

    if not os.path.exists(path):
        print 'Error: missing data file: ' + path
        exit()

    data = csv.reader(open(path))
    fields = data.next()
    json_data = []

    for row in data:
        items = dict(zip(fields,row)) # Zips fields with target data
        json_data.append(items) # Append dictionary to list

    # Print example output from each file (last item)
    print '\n' + FILE + '\n'
    print items

    json_list = json.dumps(json_data)
    f = open(dest, 'w')
    f.write(json_list)
    f.close()
