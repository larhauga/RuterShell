#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from datetime import datetime,timedelta
from pytz import timezone
#from dateutil import tz
import pytz
import re, os
import sys
import time
from ast import literal_eval

base = 'http://reis.ruter.no/ReisRest/'

def localdate(timenr, toprint=True):
    epoch = re.search('\d+', timenr)
    utcdt = datetime.utcfromtimestamp(float(epoch.group(0)[:-3]))
    tzosl = timezone('Europe/Oslo')
    utc = utcdt.replace(tzinfo=pytz.utc)
    local = utc.astimezone(tzosl)
    if toprint:
        return local.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return local

def print_stop(stop):
    # AimedDepartureTime
    # PublishedLineName
    # LineRef
    # AimedArrivalTime
    # ExpectedDepartureTime
    # DestinationName
    # OriginName
    #aimeddeparture = stop['AimedDepartureTime']
    linename = stop['PublishedLineName']
    lineref = stop['LineRef']
    #arrivaltime = stop['AimedArrivalTime']
    departuretime = stop['ExpectedDepartureTime']
    destname = stop['DestinationName']
    origin = stop['OriginName']
    print "%s: %s -> %s" % (localdate(departuretime), lineref, destname)

def find_stops(name):
    address = base + 'Place/FindMatches/' + name
    print address
    stop = requests.get(address)
    s = stop.json()
    stops = []
    for stp in s:
        if 'Oslo' in stp['District']:
            stops.append(stp)

    if len(stops) > 1:
        print "Multiple stops match."
        i = 1
        for stop in stops:
            print "Nr. %s: %s" % (str(i), stop['Name'])
            i += 1

        nr = int(raw_input("Choose stop: "))
        return stops[nr-1]['ID']
    else:
        return stops[0]['ID']

def main():
    departures = None
    print sys.argv
    if len(sys.argv) > 1:
        stop = find_stops(sys.argv[1])
        if stop:
            req = requests.get(base + 'RealTime/GetAllDepartures/' + str(stop))
            departures = req.json()

    else:
        sys.exit(1)
        #r = requests.get(base + 'RealTime/GetAllDepartures/3010057')
        #departures = r.json()

    #for key in departures[0].keys():
        #print "%s: %s" % (key, departures[0][key])

    if departures:
        for line in departures:
            print_stop(line)
            #print line

if __name__ == '__main__':
    main()
