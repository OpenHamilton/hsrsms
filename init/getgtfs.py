#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

'''This module refreshes the Google GTFS data.

Downloads the file from BUS_URL via HTTP. It then unzips the archive to the
/tmp archive in a series of text files.

Notes: This file is temporary. Ideally this should occur during the built in
Django syncdb command.
'''

import os
import urllib
import zipfile

BUS_URL = "http://googlehsr.hamilton.ca/latest/google_transit.zip"
DIR = "tmp"
FILE = 'google_transit.zip'

path = os.path.join(DIR, FILE)

# Attempt download via HTTP
try:
  path, hdrs = urllib.urlretrieve(BUS_URL, path)
except IOError, e:
  print "Can't retreive %r to %r: %s" % (BUS_URL, DIR, e)
  exit()

# Attempt unzip archive
try:
  z = zipfile.ZipFile(path)
except zipfile.error, e:
  print "Bad zipfile (from %r): %s" % (BUS_URL, e)
  exit()

 # Loop through files unzipping to DIR                       
for n in z.namelist():
  dest = os.path.join(DIR, n)
  destdir = os.path.dirname(dest)
  if not os.path.isdir(destdir):
    os.makedirs(destdir)
  data = z.read(n)
  f = open(dest, 'w')
  f.write(data)
  f.close()
z.close()
os.unlink(path)

