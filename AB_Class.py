#pylint: dissable
#-------------------------------------------------------------------------------
# Name:         WTV_Class_v1.py
# Purpose:      Classes for methods to be called for accessing the TransportViewer.db
#
#  Classes and completed methods:

#    Database(Object)                    ::A GTFS feed transformed into a SQLite database::
#      > __init__(database)              ::<database> is a SQLite3 database, constructed by the use of WTV_GTFStoSQL_v*.py::
#      > getFeedInfo()                   ::Returns cur.fetchall() of the feed_info table::
#      > feedEndDate()                   ::Returns a datetime object representing the end date of the GTFS feed::
#      > feedStartDate()                 ::Returns a datetime object representing the start date of the GTFS feed::
#      > feedDateRange()                 ::Returns a tuple of two datetime objects, representing [0] the start date of the feed and [1] the end date of the feed::
#      > getAllModes()                   ::Returns a list of Mode objects, one for each type of route_type_desc in the GTFS (routes table)::
#      > getAgencies()                   ::Returns cur.fetchall() of the agency table::
#      > checkTableEmpty(tableName="intervals") :: Checks if <tableName> (str) has any rows; returns Boolean to that effect::
#      > populateIntervals(DayObj=None, starti=0, endtime=datetime.time(21, 30)) ::Recursively populates the intervals table of self (Database) for <DayObj>. Be careful to ensure that the DB you're populating does not already have a populated intervals table::

#    Day(Database)                       ::A date. PT runs by daily schedules, considering things like whether it is a weekday, etc::
#      > __init__(database, datetimeObj) ::<database> is a Database object. <datetimeObj> is a datetime object::
#      > getCanxServices()               :CAUTION:Returns a list of PTService objects that are cancelled according to the calendar_dates table. For Wellington I suspect this table is a little dodgy::
#      > getServicesDay()                ::Returns a list of service IDs of services that are scheduled to run on self (Day). Accounts for exceptional additions and removals of services; but not the midnight bug, as a PTService is not a PTTrip::
#      > plotModeSplitNVD3(databaseObj, city) ::Uses the Python-NVD3 library to plot a pie chart showing the breakdown of vehicle modes (num. services) in Day. Useful to compare over time, weekday vs. weekend, etc. <city> is str, used in the title of the chart::
#      > animateDay(self, start, end, llcrnrlon, llcrnrlat, latheight, aspectratio, sourceproj=None, projected=False, targetproj=None, lat_0=None, lon_0=None, outoption="show", placetext='', skip=5, filepath='', filename='TestOut.mp4') ::See the method for parameter explanations::
#      > getActiveTrips(second)          ::Returns a list of PTTrip objects representing those trips that are running on self (Day) at <second>. Accounts for service cancellations and the "midnight bug"::
#      > countActiveTrips(second)        ::Returns an integer count of the number of trips of any mode that are operating at <second> on self (Day), according to self.getActiveTrips(<second>)::
#      > countActiveTripsByMode(second)  ::Returns an dictionary of {mode: integer} pairs similar to self.countActiveTrips(<second>) that breaks it down by mode::
#      > bokehFrequencyByMode(n, Show=False, name="frequency.py", title="frequency.py", graphTitle="Wellington Public Transport Services, ")  ::Returns an HTML graph of the number of active service every <n> seconds, on the second, broken down by mode::
#      > getSittingStops(second)         ::Returns a list of dictionaries which give information about any public transport stops which currently (<second>) have a vehicle sitting at them, on <DayObj>. Correctly handles post-midnight services::
#      > getAllTrips()                   ::Returns a list of PTTrip objects representing those trips that run at least once on self (Day). Accounts for midnight bug correctly::
#      > hexbinStops()                   ::Creates a hexbin plot representing the number of stops vehicles make in Day::

#    Mode(Database)                      ::A vehicle class, like "Bus", "Rail", "Ferry" and "Cable Car"::
#      > __init__(database, modetype)    ::<database> is a Database object. <modetype> is a string (as above) of the mode of interest::
#      > getRoutesOfMode                 ::Returns a list of route objects that are of the same mode type as self::
#      > getRoutesModeInDay(DayObj)      ::Same as Mode.getRoutesModeInDay, but only returns those routes that run on DayObj::
#      > countRoutesModeInDay(DayObj)    ::A count of the returned values from Mode.getRoutesModeInDay(DayObj)::
#      > countTripsModeInDay(DayObj)     :INEFFICIENT:A count of the number of discrete trips made on the routes returned from Mode.getRoutesModeInDay(DayObj)::
#      > getAgencies()                   ::Return a list of Agency objects that have routes of the same <modetype> as Mode::

#    PTService(Database)                 ::A "service" in GTFS parlance, is used to identify when a service is available for one or more routes, when these are run, and what trips they represent::
#      > __init__(database, service_id)  ::<service_id> is an Integer. See database::
#      > getRoutes_PTService()           ::Returns a list of all of the Route objects based on the route_id or route_ids (plural) that the PTService object represents::

#    Agency(Database)                    ::An Agency is an opertor usually contracted to run one or more routes with vehicles that they own. They are subject to performance measurements and re-tendering, etc.::
#      > __init(Database, agency_id)     ::<database> is a Database object. <agency_id> is a String representing the abbreviation of the agency name::
#      > getAgencyName()                 ::Returns a string of the full Agency name::
#      > getRoutes_Agency()              ::Returns a list of the Route objects representing the routes that the agency is contracted to operate on::
#      > getServices()                   ::Returns a list of the PTService objects representing the services that the agency's routes represent::

#    Route(Agency)                       ::A Route is a path that a trip takes. It has a shape, including vertices and end points. Each route is operated by a single Agency::
#      > __init__(database, route_id)    ::<database> is a Database object. <route_id> is a String (e.g. 'WBAO001I' for the incoming Number 1 bus)::
#      > getAgencyID()                   ::Returns a String of the Agency (agency_id) that operates the route. Used to construct the Agency object that the Route object inherits from.::
#      > getShortName()                  ::Returns a String of the route_short_name attribute from the routes table representing the name displayed to passengers on bus signage etc., e.g. "130"::
#      > getLongName()                   ::Returns a String of the route_long_name attribute from the routes table representing the full name of the route::
#      > getTripsInDayOnRoute(DayObj)    ::Returns a list of PTTrip objects that run along the entire route. <DayObj> is a Day object::
#      > countTripsInDayOnRoute(DayObj)  ::Returns an Integer count of the trips that run on the route on <DayObj> (a la Route.getTripsInDayOnRoute())::
#      > doesRouteRunOn(DayObj)          ::Returns a Boolean according to whether the Route has a trip on <DayObj>::
#      > inboundOrOutbound()             ::Returns Strings "Incoming" or "Outgoing" according to whether the Route is such::
#      > getMode()                       ::Returns the mode of the route, as a Mode object::

#    PTTrip(Route)                       ::A PTTrip is a discrete trip made by single mode along a single route::
#      > __init__(database, trip_id, DayObj=None) ::<database> is a Database object. <trip_id> is an Integer identifying the trip uniquely. See the database. <DayObj> is a Day object; if not None, then PTTrip.runstoday can be accessed (faster than PTTrip(DB, ID).doesTripRunOn(Day))::
#      > getRouteID()                    ::Returns the route_id (String) of the route that the trip follows. Used to construct the Route object which the Trip object inherits::
#      > doesTripRunOn(DayObj)           ::Returns a Boolean reporting whether the PTTtrip runs on <DayObj> or not. Considers the exceptions in calendar_dates before deciding, and handles >24h time::
#      > getRoute()                      ::Returns the Route object representing the route taken on Trip::
#      > getService()                    ::Returns the PTService object that includes this trip::
#      > getShapelyLine()                ::Returns a Shapely LineString object representing the shape of the trip::
#      > getShapelyLineProjected(source=4326, target=2134) ::Returns a projected Shapely LineString object, derived from self.getShapelyLine(), where <source> is the unprojected Shapely LineString GCS, and <target> is the target projection for the output. The defaults are WGS84 (<source>) and NZGD2000 (<target>).
#      > prettyPrintShapelyLine()        ::Prints a columised WKT representation of <self> (trip's) shape, ready tto be copy-pasted into QGIS via a TXT file::
#      > plotShapelyLine()               ::Uses matplotlib and Shapely to plot the shape of the trip. Does not plot stops (yet?)::
#      > getStopsInSequence()            ::Returns a list of the stops (as Stop ibjects) that the trip uses, in sequence::
#      > whereIsVehicle(DayObj, write=False) ::<DayObj> is a Day object. Returns an ordered list of (second, shapely.geometry.Point) for the entire range of the trip in <DayObj>, every second it runs. If write=True, then write the result to the intervals table of the database::
#      > getShapeID()                    ::Each trip has a particular shape, this returns the ID of it (str)::
#      > getTripStartDay(DayObj)         ::The start day of a PTTrip is either the given <DayObj>, or the day before it (or neither if it doesn't run). This method returns <DayObj> if the trip starts on <DayObj>, the Day BEFORE <DayObj> if that's right, and None in the third case. Raises an exception in the case of ambiguity::
#      > getTripEndDay(DayObj)           ::The end day of a PTTrip is either the given <DayObj>, or the day after it (or neither if it doesn't run). This method returns <DayObj> if the trip ends on <DayObj>, the Day AFTER <DayObj> if that's right, and None in the third case. Raises an exception in the case of ambiguity:: 
#      > getTripStartTime(DayObj)        ::The day and time that the trip starts, with reference to DayObj, if indeed it runs on DayObj. Returns a datetime.time object. IF the end time is ambiguous (as in some situtations when the trip continues over  midnight for consecutive days, this method returns a list of datetime.time objects with the date and the time, using <DayObj> as seed. Return values are to the microsecond resolution. Returns None if PTTrip does not run on <DayObj>::
#      > getTripEndTime(DayObj)          ::The day and time that the trip ends, with reference to DayObj, if indeed it runs on DayObj. Returns a datetime.time object. IF the end time is ambiguous (as in some situtations when the trip continues over  midnight for consecutive days, this method returns a list of datetime.time objects with the date and the time, using <DayObj> as seed. Return values are to the microsecond resolution. Returns None if PTTrip does not run on <DayObj>::

#    Stop(Object)                        ::A place where PT vehicles stop within a route::
#      > __init__(database, stop_id)     ::<database> is a Database object. <stop_id> is an Integer identifying the trip uniquely, able to link it to stop_times. See the database::
#      > getStopCode()                   ::Returns the stop_code, a short(er) integer version similar to stop_id, but published on signs and used in passenger text alerts::
#      > getStopName()                   ::Returns the stop_name, a long name of the stop (String)::
#      > getStopDesc()                   ::Returns the stop_desc, a short but textual name for the stop::
#      > getLocationType()               ::Returns location_type_desc from the stops table: ["Stop", "Station", "Hail and Ride"]. For Metlink: ["Stop", "Hail and Ride"]::
#      > getShapelyPoint()               ::Returns a shapely Point object representing the location of the stop::
#      > getShapelyPointProjected(source=4326, target=2134) ::Returns a Shapely point representing the location of the stop, projected from the <source> GCS to the <target> PCS. 2134 = NZGD2000 / UTM zone 59S (default <target>); 4326 = WGS84 (default <source>). Returns a shapely.geometry.point.Point object::
#      > getStopTime(TripObj, DayObj)    ::Returns a list of tuples of date+time objects representing the day-time(s) when the <TripObj> arrives and departs self (Stop), using <DayObj> as seed::
#      > getStopSnappedToRoute(TripObj)  ::Returns a Shapely.geometry.point.Point object representing the originally-non-overlapping Stop as a Point overlapping (or very, very nearly overlapping) the Route shape of <TripObj>::

# Tasks for next iteration/s:
#  > KEEP CODE DOCUMENTED THROUGHOUT
#  > Develop the HTML and CSS for the website and embed the JavaScript graphs
#  > Work on the visualisation of the network in real time (based on work done by Chris McDowell...)
#  > Work on the server//Django side of things to get an actual website!
#  > Have the first version of the website up and running (one city)!
#  > Expand to multiple cities
#  > Consider how fare information can be added
#
#
# Author:        Richard Law.
#
# Inputs:        Database written by WTV_GTFStoSQL_v*.py
#
#
# Created:            20131107
# Last Updated:       20140101
# Comments Updated:   20140101
#-------------------------------------------------------------------------------

################################################################################
############################### Notes ##########################################
################################################################################

"""
Before using script change filepath for database (db_pathstr) and potentially name of the database itself (db_str).
"""

################################################################################
############################## Program #########################################
################################################################################

import time
import os

from string import Template
import datetime

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from shapely.geometry import Point, LineString
from osgeo import ogr # Projecting
from shapely.wkb  import loads # Projecting
from math import sqrt # Snapping
from sys import maxint # Snapping

import bisect

import sqlite3 as dbapi
# Name of databse
##db_str = "GTFSSQL_Wellington_20140113_192434.db" # Sunday PT Wellington
##db_str = "GTFSSQL_Wellington_20140227_165759.db" # Monday PT Wellington
db_str = "Saturday/GTFSSQL_Wellington_20140402_210506.db" # Saturday PT Wellington

#db_pathstr = "G:\\Documents\\WellingtonTransportViewer\\Data\\Databases\\" + db_str # Path and name of DB under Windows, change to necessary filepath
##db_pathstr = "/media/alphabeta/RESQUILLEUR/Documents/WellingtonTransportViewer/Data/Databases/" + db_str # Path and name of DB under Linux with RESQUILLEUR, change to necessary filepath
db_pathstr = "/media/RESQUILLEUR/Documents/WellingtonTransportViewer/Data/Databases/" + db_str
myDB = dbapi.connect(db_pathstr) # Connect to DB
myDB.text_factory = dbapi.OptimizedUnicode

class CustomException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)

class Database(object):
  '''
  A GTFS feed transformed into a SQLite database.
  Methods for accessing miscellaneous information about the feed, such as the provider (and its website).
  '''
  def __init__(self, database):
    '''
    <database> is a SQLite3 database, constructed by the use of WTV_GTFStoSQL_v*.py.
    self.cur returns a cursor on this database for use in almost every other function.
    '''
    self.database = database
    self.cur = self.database.cursor()

  def checkTableEmpty(self, tableName="intervals"):
    '''
    Checks if tableName has any records.
    Returns True if it does, False if not.
    '''
    q = Template('SELECT exists(SELECT 1 FROM $tableName LIMIT 1)')
    query = q.substitute(tableName = tableName)
    results = self.cur.execute(query)
    for result in results:
      if result[0] == 0:
        # There are no records in the database table
        return False
      else:
        # There are records in the database table
        return True

  def getFeedInfo(self):
    '''
    Returns all of the information from the feed_info table of the database, which reports on the idenitity of the feed uploader (usu. also the network coordinator).
    Returns a cursor.fetchall() format .
    Example output:
    > [('Greater Wellington Regional Council', 'http://www.metlink.org.nz', 'en', '2013-04-19 00:00:00.000', '2013-07-24 00:00:00.000', None)]
    '''
    self.cur.execute('SELECT * FROM feed_info')
    return self.cur.fetchall()

  def feedEndDate(self):
    '''
    Returns a datetime object representing the end date of the GTFS feed, after which time the scheduled services in the GTFS and database are only indications.
    '''
    FI = self.getFeedInfo()
    end = FI[0][4]
    return datetime.datetime(int(end[0:4]), int(end[5:7]), int(end[8:10]), 23, 59, 59)

  def feedStartDate(self):
    '''
    Returns a datetime obect representing the start date of the GTFS feed (database), before which there is no data.
    '''
    FI = self.getFeedInfo()
    start = FI[0][3]
    return datetime.datetime(int(start[0:4]), int(start[5:7]), int(start[8:10]), 0, 0, 0)

  def feedDateRange(self):
    '''
    Returns a tuple of two datetime objects, representing [0] the start date of the feed and [1] the end date of the feed.
    '''
    FI = self.getFeedInfo()
    start = FI[0][3]
    end = FI[0][4]
    return(datetime.datetime(int(start[0:4]), int(start[5:7]), int(start[8:10]), 0, 0, 0), datetime.datetime(int(end[0:4]), int(end[5:7]), int(end[8:10]), 23, 59, 59))

  def getAllModes(self):
    '''
    Returns a list of Mode objects, one for each type of route_type_desc in the GTFS (routes table).
    '''
    modelist = []
    self.cur.execute('SELECT DISTINCT route_type_desc FROM routes')
    modes = self.cur.fetchall()
    for mode in modes:
      modelist.append(Mode(self.database, mode[0]))
    return modelist

  def getAgencies(self):
    '''
    Returns all of the information from the feed_info table of the database, which reports on the idenitity of the feed uploader (usu. also the network coordinator).
    Returns a cursor.fetchall() format .
    Example output:
    > [('Greater Wellington Regional Council', 'http://www.metlink.org.nz', 'en', '2013-04-19 00:00:00.000', '2013-07-24 00:00:00.000', None)]
    '''
    self.cur.execute('SELECT * FROM agency')
    return self.cur.fetchall()
  
  def populateIntervals(self, DB=myDB, DayObj=None, starti=0, endtime=datetime.time(21, 30)):
    '''
    Populates the intervals table of self (Database).
    Be careful not to run this method for a database which already has
    a populated intervals table (an Exception will be raised by this
    method, so it's not dire).
    
    <DayObj>: the day to populate for.
    <starti>: the trip_id to begin with.
    <endtime>: the IRL time to stop doing this (so the computer can be turned off)
    '''
    if DayObj == None:
      raise CustomException("Need to specify a day for the intervals table to be populated.")
      ## Example: DayObj=Day(datetimeObj=datetime.datetime(2013, 12, 8))
      
    if self.checkTableEmpty(tableName="intervals") == True:
      ## If there ARE records in the table
      print "Note, the intervals table is not blank."
      
    def durat(op=None, clock=[time.time()]):
      # Little timing function to test efficiency.
      # Source: http://code.activestate.com/recipes/578776-a-simple-timing-function/
      if op != None:
        duration = time.time() - clock[0]
        print '%s finished. Duration %.6f seconds.' % (op, duration)
      clock[0] = time.time()
    
    durat() # Initiate timer
    allTrips = DayObj.getAllTrips()
    durat('DayObj.getAllTrips()') # How long did it take to get all trip objects for DayObj?
    print len(allTrips), "to process."

    for trip in allTrips: # For all trips on DayObj
      current_time = datetime.datetime.now().time()
      if trip.trip_id >= starti and current_time < endtime:
        durat() # Re-initiate timer, once for each trip
        processing =  "Processing Trip=%i" % trip.trip_id
        print processing,
        trip.whereIsVehicle(DayObj, write=True) # The actual workhorse
        process="Trip=%s, i=%i, myPTTrip.whereIsVehicle(DayObj, write=True)" % (trip.trip_id, starti,)
        durat(process) # How long did it take to process the record?
        starti += 1 # Next index, in parallel with trip_id

    # When done, play some noise to let me know
    import pygame
    pygame.init()
    pygame.mixer.init()
    sound = pygame.mixer.Sound("test.wav")
    for i in range(0,5):
      sound.play()
      time.sleep(1)

class Day(Database):
  '''
  A date. PT runs by daily schedules, considering things like whether it is a weekday, etc.
  Today is gonna be a good day!
  '''
  def __init__(self, database, datetimeObj):
    '''
    <database> is a Database object.
    <datetimeObj> is a datetime object, e.g. datetime.datetime(2013, 12, 8)
    '''
    Database.__init__(self, database)
    self.datetimeObj = datetimeObj
    self.isoDate = self.datetimeObj.isoformat(' ')
    self.year = self.isoDate[0:4]
    self.month = self.isoDate[5:7]
    self.day = self.isoDate[8:10]

    self.dayOfWeekInt = self.datetimeObj.weekday()
    weekdayCorrespondence = {0: "monday", 1: "tuesday", 2: "wednesday", 3: "thursday", 4: "friday", 5: "saturday", 6: "sunday"}
    self.dayOfWeekStr = weekdayCorrespondence[self.dayOfWeekInt] # e.g. "saturday"

    # Get the relative "tomorrow" (useful for methods checking if a service is offered on a given day, because it gives the upper limit)
    tomorrowObj = self.datetimeObj + datetime.timedelta(days=1)
    self.tomorrow = tomorrowObj.isoformat(' ') # "2013-11-07 00:00:000"
    self.tomorrowObj = tomorrowObj

    # Get the relative "yesterday" (useful for methods checking post-midnight services)
    yesterdayObj = self.datetimeObj - datetime.timedelta(days=1)
    self.yesterdayISO = yesterdayObj.isoformat(' ')
    self.yesterdayObj = yesterdayObj
    
  def getSittingStops(self, second):
    '''
    Given a particular <second> (datetime.time) in a <dayObj>, returns a
    list of the XY positions of any public transport stops that any
    vehicle is currently sitting at (refers to trips).
    
    Nothing is returned for vehicles that are between stops: this is for
    stopped vehicles only.
    
    Correctly accounts for services that go over midnight

    Example <second>: datetime.time(5, 6) = 05:06am
    <dayObj> is a Day object.
    '''
    hour, mins, secs, ssecs = str(second.hour), str(second.minute), str(second.second), str(second.microsecond)
    if len(hour) == 1:
      hour = "0" + hour
    if len(mins) == 1:
      mins = "0" + mins
    if len(secs) == 1:
      secs = "0" + secs
    if len(ssecs) == 1:
      ssecs = "00" + ssecs
    if len(ssecs) == 2:
      ssecs = "0" + ssecs
    
    shortlist, sittingstops, captured = [], [], []
    q = Template('SELECT S.stop_lat, S.stop_lon, ST.trip_id, ST.stop_id, ST.pickup_type_text, ST.drop_off_type_text FROM stop_times_amended AS ST JOIN stops AS S ON ST.stop_id = S.stop_id WHERE arrival_time = "$second" OR departure_time = "$second" OR (arrival_time < "$second" AND departure_time > "$second")')
    query = q.substitute(second = hour + ":" + mins + ":" + secs + "." + ssecs)
    self.cur.execute(query)
    for sittingstop in self.cur.fetchall():
      if sittingstop[2] not in captured: # Ensures unique trip_ids
        captured.append(sittingstop[2])
        shortlist.append(sittingstop)
        
    # Need an additional query in case a stop dwells over the midnight break; checks the old stop_times table (not stop_times_amended)
    # This advances <second> by 24 hours so that it is a post-midnight check.
    q = Template('SELECT S.stop_lat, S.stop_lon, ST.trip_id, ST.stop_id, ST.pickup_type_text, ST.drop_off_type_text FROM stop_times AS ST JOIN stops AS S ON ST.stop_id = S.stop_id WHERE arrival_time < "$second24" AND departure_time > "$second24"')
    second24 = str(int(hour) + 24) + ":" + mins + ":" + secs + "." + ssecs
    query = q.substitute(second = hour + ":" + mins + ":" + secs + "." + ssecs, second24 = second24)
    self.cur.execute(query)
    for sittingstop in self.cur.fetchall():
      if sittingstop[2] not in captured: # Ensures unique trip_ids
        captured.append(sittingstop[2])
        shortlist.append(sittingstop)
        
    for sittingstop in shortlist:
      if PTTrip(self.database, str(sittingstop[2]), self).runstoday: # If the trip actually runs on the day being considered
        sittingstop = {"stop_lat":sittingstop[0], "stop_lon":sittingstop[1], "trip_id":sittingstop[2], "stop_id":sittingstop[3], "pickup_type_text":sittingstop[4], "drop_off_type_text":sittingstop[5]}
        sittingstops.append(sittingstop)
        
    return sittingstops

  def getCanxServices(self):
    '''
    Returns a list of PTService objects representing services that have been cancelled on self.day, as specified by the calendar_dates table.
    '''
    q = Template('SELECT DISTINCT service_id FROM calendar_dates WHERE date LIKE "$date%" AND exception_type = 2')
    query = q.substitute(date = self.isoDate[0:10])
    self.cur.execute(query)

    canxServices = []
    # Should return PTService objects
    for service in self.cur.fetchall():
      canxServices.append(PTService(self.database, service[0]))
    return canxServices
    
  def getAllTrips(self):
    '''
    Given a particular DayObj (<self>), returns a list of PTTrip objects that
    run on that day.
    
    Note: A trip that starts on one day and ends on the next will be
    returned in both of those days, so bear this in mind if you use this
    method to count the number of services in a day.
    '''
    q = Template('SELECT DISTINCT trip_id FROM stop_times_amended WHERE $daylabel = "1"')
    query = q.substitute(daylabel = self.dayOfWeekStr)
    self.cur.execute(query)
    
    trips = []
    for trip in self.cur.fetchall():
      pttrip = PTTrip(self.database, trip[0], self)
      if pttrip.runstoday:
        trips.append(pttrip)
    return trips

  def getServicesDay(self, verbose=False):
    '''
    Returns a list of service IDs representing services that are running
    on self.day. Takes into account the day of the week, and the
    cancelled services on Day.
    
    Does not take into account services that go beyond midnight, but a
    service is not meant to represent a trip.
    PTTrip.doesTripRunOn(DayObj) correctly accounts for the midnight bug
    '''
    regularservices = []
    q = Template('SELECT DISTINCT C.service_id FROM calendar AS C LEFT OUTER JOIN calendar_dates AS CD ON CD.service_id = C.service_id WHERE C.start_Date <= "$today1" AND C.end_date >= "$tomorrow" AND C.$DayOfWeek = 1')
    query = q.substitute(today1 = self.isoDate[0:10], tomorrow = self.tomorrow[0:10], DayOfWeek = self.dayOfWeekStr)
    for service in self.cur.execute(query):
      # Ordinarily, the service operates on self (Day)
      regularservices.append(service[0])
      
    # Find all removals and additions on self (Day)
    removed, added = [], []
    q = Template('SELECT * FROM calendar_dates WHERE date = "$date"')
    query = q.substitute(date = str(self.isoDate) + ".000")
    self.cur.execute(query)
    for service in self.cur.fetchall():
      if service[2] == 2:
        # Then the service has been removed on this self (Day) as an exception to the rule
        removed.append(service[0])
      elif service[2] == 1:
        # Then the service has been added on this self (Day) as an exception to the rule
        added.append(service[0])
      else:
        raise Exception
        
    # Only keep those services that have not been removed
    gotServices = [str(x) for x in regularservices if x not in removed]
    
    # Add those services that have been added
    gotServices = list(set(gotServices + added))
    
    if verbose:
      print "REGULAR SERVICES:", regularservices
      print "REMOVED:", removed
      print "ADDED:" , added
    
    return gotServices

  def plotModeSplit_NVD3(self, databaseObj, city):
    '''
    A Day method that uses the Python-nvd3 library to plot a pie chart showing the break-down of vehicle modes (number of services) in Day.
    E.g., could be useful to show how a city changes over time as new modes or lines are added, or compare a Sunday against a Monday.
    '''
    from nvd3 import pieChart
    output_file = open('test-nvd3_pie.html', 'w')
    type='pieChart'
    title1 = "Public Transport Trips by Mode"
    title2 = "%s, %s, %s.%s.%s" % (city, self.dayOfWeekStr.title(), self.day, self.month, self.year)
    chart = pieChart(name=type, color_category='category20c', height=400, width=400)
    chart.set_containerheader("\n\n<h2>" + title1 + "</h2>\n<h3>" + title2 + "</h3>\n\n\n")

    xdata, ydata = [], []
    modeobjs = databaseObj.getAllModes()
    for mode in modeobjs:
      xdata.append(mode.modetype)
      ydata.append(int(mode.countTripsModeInDay(self)))

    extra_serie = {"tooltip": {"y_start": "", "y_end": " trips"}}
    chart.add_serie(y=ydata, x=xdata, extra=extra_serie)
    chart.buildhtml()

    output_file.write(chart.htmlcontent)
    output_file.close()
    return None

  def getActiveTrips(self, second, internalCall=False):
    '''
    Returns an integer count of the number of trips in operation during
    self at <second>.
    <second> is a datetime.time object representing the seconds after
    midnight on self.<internalCall> is used by self.countActiveTripsByMode

    Examples of <second>:
    4pm (exactly, to the second) = datetime.datetime.time(16)
    4.01pm (to the second) = datetime.datetime.time(16, 01)
    4.01pm and 32 seconds = datetime.datetime.time(16, 01, 32)
    # if you're silly and give it split seconds... I check and round to
    the nearest whole second (01:00:00.002 >> 01:00:00.000)
    '''
    # Fix up the time
    # There could be more elegant ways...
    if second.microsecond > 0:
      msec = int(round(second.microsecond, -6)) # round to nearest million (0 or 1,000,000)
      if msec > 0:
        # If 1 million, add to seconds
        secs = second.second + 1
        mins = second.minute
        hours = second.hour
        if secs > 59:
          # if 60 seconds, add to minutes
          mins = second.minute + 1
          secs = 0
          if mins > 59:
            # if 60 minutes, add to hours
            hours = second.hour + 1
            mins = 0
            if hours > 23:
                # If 24 hours or more, subtract 24 hours
                hours = hours - 24
                newsecond = datetime.time(hours, mins, secs)
      try:
        hours
      except:
        hours = second.hour
      try:
        mins
      except:
        mins = second.minute
      try:
        secs
      except:
        secs = second.second
      try:
        newsecond
      except NameError:
        newsecond = datetime.time(hours, mins, secs)
    else:
      newsecond = second
      
    # Use newsecond to get all of the trips that operate at <second>
    newsecond = str(newsecond.hour*3600 + newsecond.minute*60 + newsecond.second)
    query = 'SELECT DISTINCT trip_id FROM intervals WHERE seconds = "%s"' % newsecond # Dont change this without referring to self.countActiveTripsByMode first
    self.cur.execute(query)
    nominallyrunning = self.cur.fetchall()
    
    todaystrips = [trip.trip_id for trip in self.getAllTrips()] # Trips that are actually running on self (Day)
    testtrips = [trip_id[0] for trip_id in nominallyrunning] # Trips that have a vehicle at operation at <second> on whatever Day they run
 
    # Return trips that run at <second> AND run on self (Day), as a list of PTTrip objects
    return [PTTrip(self.database, str(trip), self) for trip in list(set(todaystrips).intersection(set(testtrips)))]
  
  def countActiveTrips(self, second):
    '''
    A count of the trips that are running at <second> on self (Day),
    according to self.getActiveTrips(<second>)
    '''
    return len(self.getActiveTrips(second))

  def countActiveTripsByMode(self, second):
    '''
    Similar to countActiveTrips(<second>), but returns a dictionary of {modetype: count} pairs.
    '''
    mode_count = {}
    trips = self.getActiveTrips(second)
    for trip in trips:
      mode = trip.getMode().modetype
      if mode not in mode_count:
        mode_count[mode] = 1
      else:
        mode_count[mode] = mode_count[mode] + 1
    
    return mode_count

  def bokehFrequencyByMode(self, n, Show=False, name="frequency.html", pagetitle="frequency.py", graphTitle="Wellington Public Transport Services, "):
    '''
    Uses blokeh to make a HTML chart of the frequency of public transport over self (Day), at intervals of n
    The chart begins at midnight on self, and ends at midnight 24 hours later.
    <n> is considered in seconds.
    <name> is a string that can be used to name the HTML file.
    If <show> is true, opens the result in a browser automatically.
    '''
    import bokeh.plotting

    def incrementT(mode, count):
      '''Adds to t'''
      if mode == 'Rail':
        increment = incrementSpecial(count)
      else:
        increment = count
      return increment

    def incrementSpecial(count):
      '''Special increment for a mode, e.g., to make a capacity graph'''
      # example: Trains could be weighted 4 times as buses to reflect their size.
      return count * 1

    def ifZeroCount():
      '''The value to be used when the count is 0'''
      return None

    seconds = [] # The x-axis
    total, bus, rail, ferry, cablecar = [], [], [], [], [] # The lines (y-axis values)

    for sec in range(0, 24*3600, n):
      seconds.append(sec)
      t, addBus, addRail, addFerry, addCableCar = 0, False, False, False, False # Define values, assume absence
      secs = datetime.timedelta(seconds=sec)
      secs = str(secs).split(":")
      h, m, s = int(secs[0]), int(secs[1]), int(secs[2])
      mode_count = myDay.countActiveTripsByMode(datetime.time(h, m, s)) # Dictionary
      for mode in mode_count: # For each mode in the city
        if mode == 'Bus':
          addBus = True
          count = mode_count[mode]
          t += incrementT(mode, count)
          bus.append(count)
        elif mode == 'Rail':
          addRail = True
          count = mode_count[mode]
          t += incrementT(mode, count)
          rail.append(incrementSpecial(count))
        elif mode == 'Ferry':
          addFerry = True
          count = mode_count[mode]
          t += incrementT(mode, count)
          ferry.append(count)
        elif mode == 'Cable Car':
          addCableCar = True
          count = mode_count[mode]
          t += incrementT(mode, count)
          cablecar.append(count)
        else:
          raise CustomException("You need to add another list for that modetype.")


      if addBus == False:
        bus.append(ifZeroCount())
      if addRail == False:
        rail.append(ifZeroCount())
      if addFerry == False:
        ferry.append(ifZeroCount())
      if addCableCar == False:
        cablecar.append(ifZeroCount())

      if t > 0:
        total.append(t)
      else:
        total.append(ifZeroCount())

    bokeh.plotting.output_file(name, title=pagetitle)
    bokeh.plotting.hold()

    bokeh.plotting.line(np.array(seconds), bus, color='#BA5F22', tools='pan,zoom,resize', legend="Bus")
    bokeh.plotting.line(np.array(seconds), rail, color='#003300', tools='pan,zoom,resize', legend="Train")
    bokeh.plotting.line(np.array(seconds), ferry, color='#0099FF', tools='pan,zoom,resize', legend="Ferry")
    bokeh.plotting.line(np.array(seconds), cablecar, color='#FF0000', tools='pan,zoom,resize', legend="Cable Car")

    graphTitle = graphTitle + self.dayOfWeekStr.title() + ", " + str(self.datetimeObj.day) +"/"+ str(self.datetimeObj.month) +"/"+ str(self.datetimeObj.year)
    bokeh.plotting.curplot().title = graphTitle
    bokeh.plotting.grid().grid_line_alpha=0.3
    bokeh.plotting.figure()
    if Show == True:
      bokeh.plotting.show()
    return None
  
  def nvd3FrequencyByMode(self, n, name="frequency_nvd3.html", verbose=True):
    '''
    Plots frequency of the various PT modes in the city at in intervals of n seconds.
    That is, the numbers of vehicles at operation at any given n, from 0000 to 2359.
    '''
    def appendmodecount(modecount, modetypestr, modetypelist):
      try:
        modetypelist.append(modecount[modetypestr])
      except KeyError:
        modetypelist.append(0)
      return modetypelist
    
    def getData(xdata):
      '''
      select route_type_desc, seconds, count(route_type_desc)
      from intervals
      where seconds = 25000 or seconds = 30000 or seconds = 35000 or seconds = 40000
      group by route_type_desc, seconds
      
      Example output: {'Cable Car': {0: 0, 28800: 2, 57600: 2, 3600: 0, 82800: 0, 46800: 2, 7200: 0, 39600: 2, 64800: 2, 10800: 0, 54000: 2, 14400: 0, 36000: 2, 43200: 2, 18000: 0, 72000: 2, 32400: 2, 61200: 2, 21600: 0, 75600: 2, 50400: 2, 25200: 2, 79200: 0, 86399: 0, 68400: 2}, 'Bus': {0: 0, 28800: 269, 57600: 194, 3600: 0, 82800: 30, 46800: 129, 7200: 0, 39600: 126, 64800: 223, 10800: 0, 54000: 145, 14400: 0, 36000: 136, 43200: 124, 18000: 0, 72000: 65, 32400: 178, 61200: 240, 21600: 25, 75600: 47, 50400: 126, 25200: 145, 79200: 37, 86399: 11, 68400: 112}, 'Rail': {0: 0, 28800: 21, 57600: 20, 3600: 0, 82800: 4, 46800: 11, 7200: 0, 39600: 11, 64800: 22, 10800: 0, 54000: 10, 14400: 0, 36000: 12, 43200: 10, 18000: 2, 72000: 10, 32400: 13, 61200: 21, 21600: 10, 75600: 7, 50400: 11, 25200: 22, 79200: 4, 86399: 2, 68400: 13}, 'Ferry': {0: 0, 28800: 2, 57600: 1, 3600: 0, 82800: 0, 46800: 1, 7200: 0, 39600: 1, 64800: 2, 10800: 0, 54000: 0, 14400: 0, 36000: 1, 43200: 1, 18000: 0, 72000: 0, 32400: 2, 61200: 2, 21600: 0, 75600: 0, 50400: 0, 25200: 2, 79200: 0, 86399: 0, 68400: 2}}

      '''
      query = 'SELECT route_type_desc, seconds, count(route_type_desc) FROM intervals WHERE seconds = '
      for second in xdata:
        query += str(second) + ' or seconds = '
      query = query[:-13] # Strip off the 'or seconds = ' of the last entry
      query += 'GROUP BY route_type_desc, seconds'
      self.cur.execute(query)
      retdata = self.cur.fetchall()
      
      # Grab modes
      modes = []
      for line in retdata:
        mode = line[0]
        if mode not in modes: modes.append(mode)
      
      # Establish dictionary, 0 count is default
      modecountsmoments = {}
      for mode in modes:
        modecountsmoments[mode] = {}
        for second in xdata:
          modecountsmoments[mode][second] = 0
      
      # Populate dictionary with real values
      for line in retdata:
        mode, moment, count = line[0], line[1], line[2]
        modecountsmoments[mode][moment] = count
      
      return modes, modecountsmoments
    
    import calendar
    def converttimetoUnix(day, secondstoadd):
      daytime = day + datetime.timedelta(0,secondstoadd)
      return calendar.timegm(daytime.utctimetuple()) * 1000 # Milliseconds 1000000
    
    eod = 24*60*60-1
    xdata = [n for n in range(0,eod,n)]
    if eod not in xdata: xdata.append(eod)
    modes, fullYdata = getData(xdata)
    
    # Convert xdata to Unix timestamp
    # https://github.com/mbostock/d3/wiki/Time-Formatting
    daytimeobj = self.datetimeObj
    convertedxdata = [converttimetoUnix(daytimeobj, x) for x in xdata]
    convertedxdata.sort()

    # Initialise chart type
    from nvd3 import lineWithFocusChart
    chart = lineWithFocusChart(name='lineWithFocusChart', x_is_date=True, x_axis_format="%c") # %X is time as "%H:%M:%S"
    extra_serie = {"tooltip": {"y_start": "", "y_end": " vehicles"}, "date_format": "%c"}
    # Build mode specific data list, sorted
    for mode in modes:
      datalist = [fullYdata[mode][second] for second in xdata]
      if verbose: print mode, datalist, convertedxdata
      chart.add_serie(name=mode, y=datalist, x=convertedxdata, extra=extra_serie)
    # Build HTML and JS
    output_file = open('frequency_nvd3.html', 'w')
    chart.buildhtmlheader()
    #chart.create_y_axis(name="yAxis",label="Vehicles")
    chart.buildhtml()
    output_file.write(chart.htmlcontent)
    output_file.close()
    
  def animateDay(self, start, end, llcrnrlon, llcrnrlat, latheight, aspectratio, sourceproj=None, projected=False, targetproj=None, lat_0=None, lon_0=None, outoption="show", placetext='', skip=5, filepath='', filename='TestOut.mp4'):
    '''
    Animates the public transport system for self day.
    
    # Timing within day
    <start> = start seconds since midnight on self (Day)
    <end> = see <start>
    
    # Text control
    <placetext> = The heading along the top, e.g. "Wellington Region Public Transport"
    
    # Frame control
    <llcrnrlon> = lower-left corner longitude, e.g. 174.7
    <llcrnrlat> = lower-left cotner latitude, e.g. -41.4
    <latheight> = height of the frame in latitude, e.g. 0.5
    <aspectratio> = "equal", "4:3", "16:9", "2:1"
    NOTE: Frame coordinates should be given in WGS84 (not constrained
    to this, but would need changing).
    
    # Projection
    <sourceproj> = The projection system that the data in the intervals
    table is stored in. See: http://spatialreference.org/ref/epsg/2193/
    for example. Enter it as an integer, e.g. 2193 (EPSG format).
    <projected> (Boolean), for whether the output should be projected in
    something other than a standard lat/lon cylindrical projection.
    <targetproj> controls what this is. Example: 'tmerc'.
    See http://matplotlib.org/basemap/api/basemap_api.html for more
    options.
    <lon_0> and <lat_0> are needed for 'tmerc' and other projections.
    
    # Output control
    <outoption> = "show", "video"; controls whether the output should
    be shown interactively (show), recorded to a video file (video).
    <skip> = How many frames to skip each time (integer), e.g. 5.
    <filename> = if <outoption> == "video", then this controls the
    filename of the output.
    <flilpath> gives the directory it is to be stored in.
    '''
    import matplotlib.animation as manimation
    
    def make_GCS(lonlist,latlist,fromsourceproj):
      '''
      Rather than writing the intervals table in lat/lon values,
      this function converts <x> and <y> from a <source> projected
      coordinate system to lat/lon.
      Many thanks to John A. Stevenson:
      http://all-geo.org/volcan01010/2012/11/change-coordinates-with-pyproj/
      '''
      if latlist == [] and lonlist == []:
        return (lonlist, latlist)
      else:
        source = pyproj.Proj("+init=EPSG:%i" % fromsourceproj)
        # Return the lat lons (WGS84)
        return source(lonlist, latlist, inverse=True) # Tuple of two lists
    
    def thin(posdict, everyN):
      '''
      Creates an index of only those seconds in self (Day) that will
      actually have a dedicated frame.
      '''
      newdict, posindex = {}, []
      for mode in posdict:
        for k in posdict[mode]:
          if k % everyN == 0 and k not in posindex:
            posindex.append(k)
      return posindex
        
    import mpl_toolkits.basemap.pyproj as pyproj
    from mpl_toolkits.basemap import Basemap
    
    if matplotlib.__version__ != '1.3.1':
      print "This method is only guaranteed to work with MPL v1.3.1."
      print "You are running v" + v + "."
    
    # Set up frame of animation
    fig = plt.figure(frameon=False, tight_layout=True)
    fig.subplots_adjust(top=1, bottom=-0.2, left=-0.3, right=1.3, wspace=None, hspace=None)
    
    if aspectratio == "4:3":
       # 4:3 aspect ratio
      urcrnrlon, urcrnrlat = llcrnrlon+(latheight*(4.0/3.0)), llcrnrlat+latheight
    elif aspectratio == "16:9":
      # 16:9 aspect ratio
      urcrnrlon, urcrnrlat = llcrnrlon+(latheight*(16.0/9.0)), llcrnrlat+latheight
    elif aspectratio == "2:1":
      # 2:1 aspect ratio, which seems to be the Vimeo assumption
      urcrnrlon, urcrnrlat = llcrnrlon+(latheight*2.0), llcrnrlat+latheight
    elif aspectratio == "equal":
      # Equal aspect ratio
      urcrnrlon, urcrnrlat = llcrnrlon+latheight, llcrnrlat+latheight
    else:
      raise CustomException("aspectratio must be one of '4:3', '16:9', '2:1', 'equal'")
    
    ax = plt.axes(xlim=(llcrnrlon,urcrnrlon), ylim=(llcrnrlat,urcrnrlat), frame_on=False, rasterized=False) #frame_on ## TODO: decide on this
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_xlim(-float('Inf'), float('Inf')) 
    ax.set_ylim(-float('Inf'), float('Inf')+1) 
    ax.set_xticks([])
    ax.set_yticks([])
    textcolor = '#FFF5EE' # Eggshell white
    place_text  = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=11, family='sans-serif', color=textcolor)
    time_text = ax.text(0.87, 0.03, '', transform=ax.transAxes, fontsize=11, family='monospace', weight='heavy', color=textcolor)
    day_text = ax.text(0.87, 0.07, '', transform=ax.transAxes, fontsize=11, family='sans-serif', color=textcolor)
    date_text = ax.text(0.87, 0.11, '', transform=ax.transAxes, fontsize=9, family='monospace', color=textcolor)
    author_text = ax.text(0.02, 0.03, '', transform=ax.transAxes, fontsize=9, family='sans-serif', color=textcolor)
    tailsize=0.6
    bus, = ax.plot([], [], 'o', ms=3, c='#d95f02', alpha=1, zorder=3) # Bus colour, BA5F22
    min15headway_bus, = ax.plot([], [], '.', ms=tailsize, c='#fc8d62', alpha=1, zorder=2) # Bus tails, =<15 minute frequency
    train, = ax.plot([], [], 'o', ms=4, c='#1b9e77', alpha=1, zorder=3) # Train colour, 000000, e7298a
    min15headway_train, = ax.plot([], [], '.', ms=tailsize, c='#66c2a5', alpha=1, zorder=2) # Train tails, =<15 minute frequency, e78ac3
    ferry, = ax.plot([], [], 'o', ms=3, c='#7570b3', alpha=1, zorder=3) # Ferry colour, FFFFFF
    min15headway_ferry, = ax.plot([], [], '.', ms=tailsize, c='#8da0cb', alpha=1, zorder=2) # Ferry tails, =<15 minute frequency
    cablecar, = ax.plot([], [], 'o', ms=2, c='#e7298a', alpha=1, zorder=3) # Cable Car colour, FF0000, 1b9e77
    min15headway_cablecar, = ax.plot([], [], '.', ms=tailsize, c='#e78ac3', alpha=1, zorder=2) # Cable car tails, =<15 minute frequency, 66c2a5
    # TODO: add more modes when there are more GTFS feeds (that have additional modes)
    
    # Establish basemap object; super-background
    if projected == True:
      print "Using %s projection for Basemap, lat_0=0.0, lon_0=173.0" % (targetproj)
      projection = targetproj
      lon_0 = lon_0
      lat_0 = lat_0
    else:
      projection = 'cyl' # Default
      lat_0 = None
      lon_0 = None
    m = Basemap(llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat, resolution='f', projection=projection, lon_0=lon_0, lat_0=lat_0, area_thresh = 0)
    m.drawcoastlines(linewidth=.2)
    landcolour = '#474747' # old: '#CDBC8E', '#677D6C'
    oceancolour = '#666666' # old: '#677D6C, 4A4A4A
    lakecolour = oceancolour
    m.fillcontinents(color=landcolour,lake_color=lakecolour)
    m.drawmapboundary(fill_color=oceancolour)
    
    # Plot the background of each frame
    def init():
      time_text.set_text('')
      place_text.set_text('')
      day_text.set_text(self.dayOfWeekStr.title())
      date_text.set_text(self.isoDate[0:10])
      author_text.set_text('')
      bus.set_data([], [])
      train.set_data([], [])
      ferry.set_data([], [])
      cablecar.set_data([], [])
      min15headway_bus.set_data([], [])
      min15headway_train.set_data([], [])
      min15headway_ferry.set_data([], [])
      min15headway_cablecar.set_data([], [])
      return min15headway_cablecar, min15headway_ferry, min15headway_bus, min15headway_train, bus, train, ferry, cablecar, time_text, author_text, place_text, date_text
      
    # Prepare the actual positions to plot
    tailallowance = 15*60 # 15 minute tails
    posdict = {'Bus': {}, 'Rail': {}, 'Ferry': {}, 'Cable Car': {}}
    query = 'SELECT seconds, lat, lon, route_type_desc FROM intervals WHERE seconds >= "%i" AND seconds <= "%i"' % (start-tailallowance, end)
    self.cur.execute(query)
    answer = self.cur.fetchall()
    for a in answer:
      second, lat, lon, mode = a[0], a[1], a[2], a[3]
      if second not in posdict[mode]:
        posdict[mode][second] = ([], [])
      posdict[mode][second][0].append(lat)
      posdict[mode][second][1].append(lon)
    del answer # Free a large amount of memory
    for mode in ['Bus', 'Rail', 'Ferry', 'Cable Car']:
      for s in range(start-tailallowance, end):
        try:
          lon, lat = make_GCS(posdict[mode][s][1], posdict[mode][s][0], sourceproj)
          lon, lat = m(lon, lat) # Converts them into (potentially projected) map coordinates
        except KeyError:
          # Mode doesn't operate at s
          lon, lat = [], []
        posdict[mode][s] = (lon, lat)
    # Thin the posdict into every n records, note the seconds
    posindex = thin(posdict, skip)
    
    def animate(i):
      # Animation function: called sequentially
      # i starts at 0
      try:
        sectail = posindex[i] # The current second, considering skips
      except IndexError:
        raise Exception # There should only be as many iterations as things in posindex once it has been thinned
      secvehicle = sectail + tailallowance
      if secvehicle >= end:
        secvehicle = end - 1
        sectail = secvehicle - tailallowance
        
      # Tails
      def makeTails(past, present, mode):
        # These will be ordered... could do some cool things with this...
        xs = [[x for x in posdict[mode][s][0]] for s in range(past, present)]
        ys = [[y for y in posdict[mode][s][1]] for s in range(past, present)]
        # ...but not after they have been flattened... here
        xs = [item for sublist in xs for item in sublist]
        ys = [item for sublist in ys for item in sublist]
        return (xs, ys)
      
      # Get the data for the tails
      fifteenminsago, present = max(0, sectail), secvehicle-1
      min15tails_bus = makeTails(fifteenminsago, present, 'Bus')
      min15tails_train = makeTails(fifteenminsago, present, 'Rail')
      min15tails_ferry = makeTails(fifteenminsago, present, 'Cable Car')
      min15tails_cablecar = makeTails(fifteenminsago, present, 'Ferry')
      # Set the data for the tails
      min15headway_bus.set_data(min15tails_bus[0], min15tails_bus[1])
      min15headway_train.set_data(min15tails_train[0], min15tails_train[1])
      min15headway_ferry.set_data(min15tails_ferry[0], min15tails_ferry[1])
      min15headway_cablecar.set_data(min15tails_cablecar[0], min15tails_cablecar[1])
      
      # Current vehicle positions
      time = str(datetime.timedelta(seconds=secvehicle))
      time_text.set_text('%s' % time)
      bus.set_data(posdict['Bus'][secvehicle][0], posdict['Bus'][secvehicle][1])
      train.set_data(posdict['Rail'][secvehicle][0], posdict['Rail'][secvehicle][1])
      ferry.set_data(posdict['Ferry'][secvehicle][0], posdict['Ferry'][secvehicle][1])
      cablecar.set_data(posdict['Cable Car'][secvehicle][0], posdict['Cable Car'][secvehicle][1])
      
      fadeoutsecs = max(0, int((end-start)/float(skip))*0.25) # 25% of duration
      if i < fadeoutsecs:
        # Fade out control
        author_text.set_text('Richard Law   CC BY-NC 3.0 NZ')
        place_text.set_text(placetext)
        alpha_author = max(0, 1-i/float(fadeoutsecs*0.6))
        alpha_place = max(0, 1-i/float(fadeoutsecs*0.9))
        alpha_date = alpha_place
        author_text.set_alpha(alpha_author)
        place_text.set_alpha(alpha_place)
      else:
        author_text.set_text('')
        place_text.set_text('')
      
      name = str(i) +".png"
      numzeros = 9 - len(name)
      name = numzeros*"0" + name
      fig.savefig(name, bbox_inches='tight', pad_inches=0) # Saves each i to a PNG
      return min15headway_cablecar, min15headway_ferry, min15headway_bus, min15headway_train, bus, train, ferry, cablecar, time_text, author_text, place_text, date_text
    
    # call the animator
    frames = (end-start)/skip # How many frames (essentially the duration)
    interval = 0.5 # New frame drawn every <interval> milliseconds. 1 means 1000 frames per second. 3 means 333 frames per second
    blit = True # Only re-draw the bits that have changed; if True, func and init_fucn should return an iterable of drawables to clear
    anim = manimation.FuncAnimation(fig, animate, init_func=init, frames=frames, interval=interval, blit=blit)

    if outoption == "show":
      plt.show()
    elif outoption == "video":
      from sys import platform as _platform
      if _platform in ["win32", "darwin", "cygwin"]:
        raise CustomException("The method Day.animateDay() is only supported on Linux operating systems.")
      elif _platform == "linux" or _platform == "linux2":
        # save as an mp4
        bitrate = 15000 # kbits/s: SD=2000--5000, 720pHD=5000--10000, 1080pHD=10000--20000
        writer='ffmpeg'
        codec = '-c:v libx264'
        fps=int(700/float(skip))
        # Vimeo likes 23.976, 24, 25, 29.97 or 30 FPS
        fpss = [23.976, 24, 25, 29.97, 30]
        try:
          # Take the closest value from fpss
          fpss = [bisect.bisect(fpss, fps)]
          fps = fpss
          fps = max(23.976, fps)
          fps = min(30, fps)
        except IndexError:
          # The FPS exceeds Vimeo's min/max
          fps = max(23.976, fps)
          fps = min(30, fps)
        
        fps = 15
        if filepath != '':
          retunpath = os.getcwd()
          os.chdir(filepath)
        anim.save("temp_" + filename)
        writevideo =  writer + " -r " + str(fps) + " -i %05d.png " + codec + " -qp 0 -b:v " + str(bitrate) + "k -minrate 15000k -maxrate 15000k -bufsize 1835k " + filename
        print "Script is running: " + writevideo
        os.system(writevideo) # Create the video file
        cleanup = "rm *.png; rm " + "temp_" + filename
        print "Script is running: " + cleanup 
        os.system(cleanup)
        if filepath != '':
          os.chdir(returnpath)
        print ">>>>>>> METHOD Day.animateDay() IS COMPLETE <<<<<<<"
        
  def hexbinStopVisits(self, projected=False, sourceproj=4326, targetproj=2134):
    '''
    hexbin is an axes method or pyplot function that is essentially
    a pcolor of a 2-D histogram with hexagonal cells.  It can be
    much more informative than a scatter plot; in the first subplot
    below, try substituting 'scatter' for 'hexbin'.
    
    See Stop.getShapelyPointProjected for information about sourceproj and targetproj,
    although this implementation is separate.
    '''
    
    import mpl_toolkits.basemap.pyproj as pyproj
    from mpl_toolkits.basemap import Basemap
    
    # There is an issue with the Wellington GTFS that means that the XY
    # locations recorded to not match well with the coastlines of Basemap.
    # I'm not sure if this holds for other GTFS.
    # For now, I apply a cosmetic adjustment to lats and lons from the
    # GTFS.
    cosmeticxadj = 0.0005 # Drags locations right
    cosmeticyadj = -0.002 # Drags locations down
    
    # Get all the trip ids for trips that run on self (Day)
    validtripids = [trip.trip_id for trip in self.getAllTrips()]
    #validtripids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 5000, 5001, 5002, 5003, 5004, 6700, 6701, 6702, 4908, 2345, 1000, 1001, 1002, 2000, 2001, 2002, 3000, 3001, 4000, 4001, 4002, 4003, 4004, 4005, 4006, 4007, 4008, 4009, 4010, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010]
    #validtripids = [i for i in range(1,10000)]
    q = "SELECT trip_id, stop_id FROM stop_times ORDER BY trip_id ASC"
    self.cur.execute(q)
    # Count the number of trips that stop at each stop.
    stopvisits = {}
    for stopthing in self.cur.fetchall():
      trip_id, stop_id = stopthing[0], stopthing[1]
      if trip_id in validtripids:
        try:
          stopvisits[stop_id] = stopvisits[stop_id] + 1
        except KeyError:
          stopvisits[stop_id] = 1
    
    aspectratio='equal'
    llcrnrlon = 174.7+cosmeticyadj
    llcrnrlat = -41.4+cosmeticxadj
    latheight=0.5
    if aspectratio == "4:3":
       # 4:3 aspect ratio
      urcrnrlon, urcrnrlat = llcrnrlon+(latheight*(4.0/3.0)), llcrnrlat+latheight
    elif aspectratio == "16:9":
      # 16:9 aspect ratio
      urcrnrlon, urcrnrlat = llcrnrlon+(latheight*(16.0/9.0)), llcrnrlat+latheight
    elif aspectratio == "2:1":
      # 2:1 aspect ratio, which seems to be the Vimeo assumption
      urcrnrlon, urcrnrlat = llcrnrlon+(latheight*2.0), llcrnrlat+latheight
    elif aspectratio == "equal":
      # Equal aspect ratio
      urcrnrlon, urcrnrlat = llcrnrlon+latheight, llcrnrlat+latheight
    else:
      raise CustomException("aspectratio must be one of '4:3', '16:9', '2:1', 'equal'")
      
    xmin = llcrnrlon #x.min()
    xmax = urcrnrlon #x.max()
    ymin = llcrnrlat #y.min()
    ymax = urcrnrlat #y.max()
    if projected:
      to_srs = ogr.osr.SpatialReference()
      to_srs.ImportFromEPSG(targetproj)
      from_srs = ogr.osr.SpatialReference()
      from_srs.ImportFromEPSG(sourceproj)
      mins = ogr.CreateGeometryFromWkb(Point(xmin, ymin).wkb)
      mins.AssignSpatialReference(from_srs)
      mins.TransformTo(to_srs)
      maxs = ogr.CreateGeometryFromWkb(Point(xmax, ymax).wkb)
      maxs.AssignSpatialReference(from_srs)
      maxs.TransformTo(to_srs)
      xmin = loads(mins.ExportToWkb()).x
      ymin = loads(mins.ExportToWkb()).y
      xmax = loads(maxs.ExportToWkb()).x
      ymax = loads(maxs.ExportToWkb()).y
      
    xs, ys, counts = [], [], []
    for stop in stopvisits:
      count = stopvisits[stop]
      stopobj = Stop(self.database, stop)
      if projected == False:
        xy = stopobj.getShapelyPoint()
      else:
        xy = stopobj.getShapelyPointProjected()
      x, y = xy.x+cosmeticxadj, xy.y+cosmeticyadj
      if x < xmax and x > xmin and y < ymax and y > ymin:
        for c in range(count):
          xs.append(x)
          ys.append(y)
      else:
        pass
    xs = np.array(xs)
    ys = np.array(ys)
    
    for i in range(1,4+1):
      place = int('22' + str(i))
      plt.subplot(place, aspect='equal')
      ax = plt.axes(xlim=(llcrnrlon,urcrnrlon), ylim=(llcrnrlat,urcrnrlat), frame_on=False, rasterized=False)
      ax.get_xaxis().set_visible(False)
      ax.get_yaxis().set_visible(False)
      ax.set_xlim(-float('Inf'), float('Inf')) 
      ax.set_ylim(-float('Inf'), float('Inf')+1) 
      ax.set_xticks([])
      ax.set_yticks([])
      m = Basemap(llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat, resolution='f', projection='cyl', lon_0=173.0, lat_0=0.0, area_thresh = 0)
      m.drawcoastlines(linewidth=.2)
      landcolour = '#474747'
      oceancolour = '#666666'
      lakecolour = oceancolour
      m.fillcontinents(color=landcolour,lake_color=lakecolour,zorder=0)
      m.drawmapboundary(fill_color=oceancolour)
      import brewer2mpl
      from matplotlib.ticker import LogFormatter
      class LogFormatterHB(LogFormatter): 
        def __call__(self, v, pos=None): 
            vv = self._base ** v 
            return LogFormatter.__call__(self, vv, pos)
      hbin = plt.hexbin(xs, ys, mincnt=1, gridsize=100, bins='log', cmap=brewer2mpl.get_map('BuPu', 'sequential', 3+i).mpl_colormap)
      plt.axis([xmin, xmax, ymin, ymax])
      plt.title(self.dayOfWeekStr.title(), fontsize=16)
    
    plt.suptitle("PT Vehicle Stops", fontsize=20)
    cb = plt.colorbar(format=LogFormatterHB())
    cb.set_label('Count of vehicle stops (logarithmic)')
    '''
    plt.subplot(122, aspect='equal')
    plt.hexbin(x,y,gridsize=50,bins='log', cmap=plt.cm.YlOrRd_r)
    plt.axis([xmin, xmax, ymin, ymax])
    plt.title("With a log color scale")
    cb = plt.colorbar()
    cb.set_label('log10(N)')
    '''
    plt.show()
        
class Mode(Database):
  '''
  A class of vehicle that has particular properties it does not share with other vehicles.
  '''
  def __init__(self, database, modetype):
    '''
    <modetype>: "Bus", "Train", "Ferry", "Cable Car", and others.
    '''
    Database.__init__(self, database)
    self.modetype = modetype

  def getRoutesOfMode(self):
    '''
    Returns a list of Route objects that are of the same mode type as self.
    '''
    q = Template('SELECT DISTINCT route_id FROM routes WHERE route_type_desc = "$modetype"')
    query = q.substitute(modetype = self.modetype)
    self.cur.execute(query)
    routes = []
    for route in self.cur.fetchall():
      routes.append(Route(self.database, route[0]))
    return routes

  def getRoutesModeInDay(self, DayObj, verbose=False):
    '''
    Same as Mode.getRoutesModeInDay, but only returns those Route objects that run on DayObj.
    Has its own query.
    '''
    # Get service_id of services that are running on DayObj
    services = DayObj.getServicesDay(verbose=verbose)

    # Distinct route/service pairs of the same modetype as self.Mode.
    q = Template('SELECT DISTINCT T.route_id, T.service_id FROM trips AS T JOIN routes AS R ON T.route_id = R.route_id WHERE R.route_type_desc = "$modetype"')
    query = q.substitute(modetype = self.modetype)
    self.cur.execute(query)
    routeservicespairs = self.cur.fetchall()
    
    if verbose:
      print "Services that are running: ", services
      print "Distinct pairs that are possible:", routeservicespairs
    
    # Append to set if the service runs on DayObj, return list of Route objects
    return list(set([Route(self.database, tripservice[0]) for tripservice in routeservicespairs if str(tripservice[1]) in services]))

  def countRoutesModeInDay(self, DayObj, verbose=False):
    '''
    Returns an integer representing the count of the returned values from Mode.getRoutesModeInDay(DayObj).
    '''
    return len(self.getRoutesModeInDay(DayObj, verbose=verbose))

  def countTripsModeInDay(self, DayObj):
    '''
    Like countRoutesModeInDay, but counts trips made, not routes.
    Unfinished.
    '''
    count = 0
    # TODO: Could be more efficient with a dedicated query.
    for route in self.getRoutesModeInDay(DayObj):
      count += route.countTripsInDayOnRoute(DayObj)
    return count

  def getAgencies(self):
    '''
    Returns a list of Agency objects representing the agencies that have routes of the same modetype as self.Mode
    '''
    q = Template('SELECT DISTINCT A.agency_id FROM routes AS R JOIN agency AS A ON R.agency_id = A.agency_id WHERE R.route_type_desc = "$modetype"')
    query = q.substitute(modetype = self.modetype)
    self.cur.execute(query)

    agencies = []
    for agency in self.cur.fetchall():
      agencies.append(Agency(self.database, agency[0]))
    return agencies

class PTService(Database):
  '''
  Takes a service_id (Integer).
  A service_id identifies when a service is available for one or more routes.
  A "service" in GTFS parlance, is used to identify when a service is available for one or more routes, when these are run, and what trips they represent.
  Quite  a weird concept, e.g. the service_id 1 has multiple modes.
  '''
  def __init__(self, database, service_id):
    '''

    '''
    Database.__init__(self, database)
    self.service_id = service_id

  def getRoutes_PTService(self):
    '''
    Returns a list of all of the Route objects based on the route_id or route_ids (plural) that the PTService object represents.
    '''
    q = Template('SELECT DISTINCT route_id FROM trips WHERE service_id = $service_id')
    query = q.substitute(service_id = self.service_id)
    self.cur.execute(query)

    routesOfService = []
    for route_id in self.cur.fetchall():
      routesOfService.append(route_id[0])
    return routesOfService

class Agency(Database):
  '''
  An Agency is an opertor usually contracted to run one or more routes with vehicles that they own. They are subject to performance measurements and re-tendering, etc.
  The class has methods that affect the child Route objects.

  In the future, Agency will be used to match performance metrics obtained elsewhere, and apply discrete stochastic schedule variations to routes>trips.
  '''
  def __init__(self, database, agency_id):
    '''
    <database> is a Database object.
    <agency_id> is a String representing the abbreviation of the agency name.
    Examples:
    "NLDS"="Newlands Coach Services"
    "GOW"="Go Wellington"
    "Mana"="Mana Coach Services Ltd"
    "VLYF"="Valley Flyer"
    "RUNC="Runciman Motors Ltd"
    "TZWA"="Tranzit Coachlines Wairarapa"
    "KCTL":"Kapiti Coach Tours Ltd"
    "MADG"="Madge Coachlines Limited"
    "RAIL"="Tranz Metro"
    "TRAN"="Tranz Scenic"
    "EBYW"="East by West Ferry"
    "WCCL"="Wellington Cable Car Ltd"
    '''
    Database.__init__(self, database)
    self.agency_id = agency_id

  def getAgencyName(self):
    '''
    Returns a string of the full Agency name.
    '''
    q = Template('SELECT agency_name FROM agency WHERE agency_id = "$agency_id"')
    query = q.substitute(agency_id = self.agency_id)
    self.cur.execute(query)
    return self.cur.fetchall()[0][0]

  def getRoutes_Agency(self):
    '''
    Returns a list of the Route objects representing the routes that the Agency is contracted to operate on.
    '''
    q = Template('SELECT DISTINCT route_id FROM routes WHERE agency_id = "$agency_id"')
    query = q.substitute(agency_id = self.agency_id)
    self.cur.execute(query)

    routes = []
    for route in self.cur.fetchall():
      routes.append(Route(self.database, route[0]))
    return routes

  def getServices(self):
    '''
    Returns a list of the PTService objects representing the services that the agency's routes represent.
    '''
    # Build a custom search query using all of an Agency's route_ids.
    routeIDCustom = "route_id = "
    for route in self.getRoutes_Agency():
      # Start of query
      routeIDCustom = routeIDCustom + '"' + route.route_id + '" OR route_id = '
    routeIDCustom = routeIDCustom[:-15] # At end of loop, remove last " OR route_id = "
    q = Template('SELECT DISTINCT service_id FROM trips WHERE $routeIDCustom')
    query = q.substitute(routeIDCustom = routeIDCustom)
    self.cur.execute(query)

    services = []
    for service in self.cur.fetchall():
      services.append(PTService(self.database, service[0]))
    return services


class Route(Agency):
  '''
  A route is a path that a trip takes. It has a shape.
  '''
  def __init__(self, database, route_id):
    '''

    '''
    Database.__init__(self, database)
    self.route_id = route_id
    Agency.__init__(self, self.database, self.getAgencyID())

  def getAgencyID(self,):
    '''
    Returns a String of the Agency (agency_id) that operates the route.
    '''
    q = Template('SELECT agency_id FROM routes WHERE route_id = "$route_id"')
    query = q.substitute(route_id = self.route_id)
    self.cur.execute(query)
    return self.cur.fetchall()[0][0]

  def getShortName(self):
    '''
    Returns a String of the route_short_name attribute from the routes table representing the name displayed to passengers on bus signage etc. (e.g. "130") for self.Route
    '''
    q = Template('SELECT route_short_name FROM routes WHERE route_id = "$route_id"')
    query = q.substitute(route_id = self.route_id)
    self.cur.execute(query)
    return str(self.cur.fetchall()[0][0])

  def getLongName(self):
    '''
    Return a String of the route_long_name attribute from the routes table representing the full name of the route.
    '''
    q = Template('SELECT route_long_name FROM routes WHERE route_id = "$route_id"')
    query = q.substitute(route_id = self.route_id)
    self.cur.execute(query)
    return str(self.cur.fetchall()[0][0])

  def getTripsInDayOnRoute(self, DayObj):
    '''
    Given a Day object, this method returns all of the trips of this
    route on that Day, as a list of PTTrip objects.
    
    NOTE: It considers trips, so a trip that runs over midnight will be
    included both on the origin day and on the following day.
    '''
    q = Template('SELECT DISTINCT T.trip_id FROM routes AS R JOIN trips AS T ON R.route_id = T.route_id WHERE R.route_id ="$route_id"')
    query = q.substitute(route_id = self.route_id)
    self.cur.execute(query)
    alltripsonroute = [PTTrip(self.database, str(trip[0]), DayObj) for trip in self.cur.fetchall()]
    alltripsonroutetoday = [trip for trip in alltripsonroute if trip.runstoday]
      
    return alltripsonroutetoday

  def countTripsInDayOnRoute(self, DayObj):
    '''
    Given a Day object, <DayObj>, this method returns an Integer count 
    of all the trips of this route on that Day.
    
    NOTE: Considers trips, so a trip that runs over midnight will be
    included both on the origin day and on the following day.
    '''
    return len(self.getTripsInDayOnRoute(DayObj))
    
  def doesRouteRunOn(self, DayObj):
    '''
    Returns a Boolean variable (True or False) according to whether the Route has a trip on <DayObj>.
    
    PTTrip.runstoday is more efficient.
    '''
    if self.countTripsInDayOnRoute(DayObj) > 0:
      return True
    else:
      return False

  def inboundOrOutbound(self):
    '''
    Returns a String informing whether the service is recorded as "Incoming" or "Outgoing".
    NOTE: Possibly idiosyncratic to Metlink GTFS, as the incoming/outgoing distinction is only made in the route_id field.
    '''
    q = Template('SELECT DISTINCT direction_id_text FROM trips WHERE route_id = "$route_id"')
    query = q.substitute(route_id = self.route_id)
    self.cur.execute(query)
    return self.cur.fetchall()[0][0]

  def getMode(self):
    '''
    Returns a Mode object representing the mode of transport for the route.
    '''
    q = Template('SELECT route_type_desc FROM routes WHERE route_id = "$route_id"')
    query = q.substitute(route_id = self.route_id)
    self.cur.execute(query)
    return Mode(self.database, self.cur.fetchall()[0][0])
    
class PTTrip(Route):
  '''
  A PTTrip is a discrete trip made by a vehicle.
  '''
  def __init__(self, database, trip_id, today=None):
    '''
    A trip_id is database unique.
    '''
    Database.__init__(self, database)
    self.trip_id = trip_id
    Route.__init__(self, database, self.getRouteID())
    if today != None:
      self.runstoday = self.doesTripRunOn(today)

  def getRouteID(self):
    '''
    Returns the route_id (String) of the trip.
    '''
    q = Template('SELECT route_id FROM trips WHERE trip_id = $trip_id')
    query = q.substitute(trip_id = self.trip_id)
    self.cur.execute(query)
    return self.cur.fetchall()[0][0]
  
  def getTripStartTime(self, DayObj):
    '''
    Returns the start time of the trip,
    if the trip runs on <DayObj>.
    
    Returns a datetime.time object.
    
    IF the end time is ambiguous (as in some situtations when the trip
    continues over  midnight for consecutive days, this method returns a
    list of datetime.time objects with the date and the time, using
    <DayObj> as seed.
    '''
    if self.doesTripRunOn(DayObj):
      q = Template('SELECT arrival_time FROM stop_times_amended WHERE trip_id = "$trip_id" ORDER BY stop_sequence ASC')
      query = q.substitute(trip_id = self.trip_id)
      self.cur.execute(query)
      starttime = self.cur.fetchall()[0][0].split(":")
      starttime[2] = starttime[2].split(".")
      startday = self.getTripStartDay(DayObj)
      
      if isinstance(startday, list):
        startdays, days = self.getTripStartDay(DayObj), []
        for startday in startdays:
          starttime = startday[0].datetimeObj.combine(startday[0].datetimeObj, datetime.time(int(starttime[0]), int(starttime[1]), int(starttime[2][0]), int(starttime[2][1])))
          days.append(starttime)
        return [days]
        
      elif isinstance(startday, Day):
        starttime = startday.datetimeObj.combine(startday.datetimeObj, datetime.time(int(starttime[0]), int(starttime[1]), int(starttime[2][0]), int(starttime[2][1])))
        return starttime

      else:
        raise Exception
    else:
      return None
      
  def getTripEndTime(self, DayObj, verbose=False):
    '''
    Returns the start time of the trip,
    if the trip runs on <DayObj>.
    
    Returns a datetime.time object.
    
    IF the end time is ambiguous (as in some situtations when the trip
    continues over  midnight for consecutive days, this method returns a
    list of datetime.time objects with the date and the time, using
    <DayObj> as seed.
    '''
    if self.doesTripRunOn(DayObj):
      q = Template('SELECT departure_time FROM stop_times_amended WHERE trip_id = "$trip_id" ORDER BY stop_sequence ASC')
      query = q.substitute(trip_id = self.trip_id)
      self.cur.execute(query)
      endtime = self.cur.fetchall()[-1][0].split(":")
      endtime[2] = endtime[2].split(".")
      endday = self.getTripEndDay(DayObj)
      
      if isinstance(endday, list):
        enddays, days = self.getTripEndDay(DayObj), []
        for endday in enddays:
          endtime = endday.datetimeObj.combine(endday.datetimeObj, datetime.time(int(endtime[0]), int(endtime[1]), int(endtime[2][0]), int(endtime[2][1])))
          days.append(endday)
        return [days]
      
      elif isinstance(endday, Day):
        endtime = endday.datetimeObj.combine(endday.datetimeObj, datetime.time(int(endtime[0]), int(endtime[1]), int(endtime[2][0]), int(endtime[2][1])))
        # Check that end time comes after start time
        if endtime < self.getTripStartTime(DayObj):
          if verbose:
            print "Potential case of start/end day/time ambiguity detected"
          return endtime + datetime.timedelta(days=1)
        else:
          return endtime
          
      else:
        raise Exception
    else:
      return None
    
  def getTripStartDay(self, DayObj, verbose=False):
    '''
    Trips that run over midnight strictly operate on two days of the
    week. However, exceptions are recorded as calendar dates that refer
    to the day when the trip started.
    Thus, given a <DayObj>, if the trip operates at all, it began on
    that day, or the day before it. This trip returns <DayObj>, or a
    Day object representing the day before <DayObj>, whichever correctly
    represents the day the trip BEGAN.
    
    If the trip runs on neither <DayObj> on the day before, returns
    None.
    
    NOTE: This does not check whether a trip actually ran on a given
    day (indeed, this is an input to that check).
    
    Exceptions are raised if the end day of the trip is ambiguous (as is
    the case for some (but not all) trips that progress through midnight.
    '''
    q = Template('SELECT DISTINCT $DOW FROM stop_times_amended WHERE trip_id = "$trip_id"')
    query = q.substitute(DOW = DayObj.dayOfWeekStr, trip_id = self.trip_id)
    if verbose:
      print query
    self.cur.execute(query)
    nottoday, today = False, False
    for indication in self.cur.fetchall():
      if indication[0] == 0:
        nottoday = True
      elif indication[0] == 1:
        today = True
      else:
        raise CustomException("calendar_date exceptions must be in [0, 1]")
    if nottoday == True and today == True:
      # Trip runs through a midnight period
      # Now need to find whether  it starts "today" (i.e. it ends
      # "tomorrow") or "yesterday" (i.e. it ends "today")
      # This can be ambiguous.
      if verbose:
        print "Trip runs through a midnight."
      yesterday = Day(self.database, DayObj.yesterdayObj)
      today = DayObj.dayOfWeekStr
      tomorrow = Day(self.database, DayObj.tomorrowObj)
      q = Template('SELECT $yesterday, $today, $tomorrow FROM stop_times_amended WHERE trip_id = "$trip_id" ORDER BY stop_sequence ASC')
      query = q.substitute(yesterday = yesterday.dayOfWeekStr, today = today, tomorrow = tomorrow.dayOfWeekStr, trip_id = self.trip_id)
      if verbose:
        print query
      self.cur.execute(query)
      beginning = self.cur.fetchall()[0] # The pattern for whether the last stop of the trip occurs yesterday, today and tomorrow (0 or 1 for each)
      
      if beginning[0] == 1 and beginning[1] == 1 and beginning[2] == 1:
        # If the trip starts at the same time yesterday, today and
        # tomorrow, then it is ambiguous as to when it starts.
        # I don't know how prevalent this is, so for now I'll make it
        # an exception, and address it conclusively if it arises.
        # If it arises, making it return "today" should work okay-ish.
        # Alternatively, this could return two objects, one with it
        # ending "today" and one with it ending "tomorrow".
        # The latter case will require additional checks regarding
        # duplicates.
        raise Exception
      elif (beginning[0] == 1 and beginning[1] == 1) or (beginning[1] == 1 and beginning[2] == 1):
        # Ambiguous, but we can return two values
        if beginning[0] == 1 and beginning[1] == 1:
          return [yesterday, today]
        elif beginning[1] and beginning[2] == 1:
          # Cannot start tomorrow
         return DayObj
        else:
          print beginning, query
          raise Exception
      elif beginning[0] == 1 and beginning[1] == 0:
        # Not ambiguous, it starts "yesterday"
        return yesterday
      elif beginning[0] == 0 and beginning[1] == 1:
        # Not ambiguous, it starts "today"
        return DayObj
      elif beginning[1] == 1 and beginning[2] == 1:
        # Erroneous, the trip can't start "tomorrow" if it is running "today"
        print beginning, query
        raise Exception
      else:
        print beginning, query
        raise Exception
        
    elif nottoday == False and today == True:
      # Trip starts and ends before midnight
      return DayObj
    elif nottoday == True and today == False:
    # Trip does not even run on this day of the week
      return None
    
  def getTripEndDay(self, DayObj, verbose=False):
    '''
    See PTTrip.etTripStartDay(DayObj)
    This method uses the same parameters, but returns a Day object repr-
    esenting the day the trip ended (which can be the same as DayObj, or
    the day after it).
    
    Exceptions are raised if the end day of the trip is ambiguous (as is
    the case for some (but not all) trips that progress through midnight.
    '''
    q = Template('SELECT DISTINCT $DOW FROM stop_times_amended WHERE trip_id = "$trip_id"')
    query = q.substitute(DOW = DayObj.dayOfWeekStr, trip_id = self.trip_id)
    if verbose:
      print query
    self.cur.execute(query)
    nottoday, today = False, False
    for indication in self.cur.fetchall():
      if indication[0] == 0:
        nottoday = True
      elif indication[0] == 1:
        today = True
      else:
        raise CustomException("calendar_date exceptions must be in [0, 1]")
    if nottoday == True and today == True:
      # Trip runs through a midnight period
      # We know this because on <Sundays> the trip arrives at a stop, and
      # then on a different day (say <Mondays>) it also arrives at a stop.
      # Now need to find whether  it ends "today" (i.e. it started
      # "yesterday") or "tomorrow" (i.e. it started "today")
      # This can be ambiguous.
      yesterday = Day(self.database, DayObj.yesterdayObj)
      today = DayObj.dayOfWeekStr
      tomorrow = Day(self.database, DayObj.tomorrowObj)
      q = Template('SELECT $yesterday, $today, $tomorrow FROM stop_times_amended WHERE trip_id = "$trip_id" ORDER BY stop_sequence ASC')
      query = q.substitute(yesterday = yesterday.dayOfWeekStr, today = today, tomorrow = tomorrow.dayOfWeekStr, trip_id = self.trip_id)
      if verbose:
        print query
      self.cur.execute(query)
      ending = self.cur.fetchall()[-1] # The pattern for whether the last stop of the trip occurs yesterday, today and tomorrow (0 or 1 for each)
      if verbose:
        print ending
      
      if ending[0] == 1 and ending[1] == 1 and ending[2] == 1:
        # If the trip ends at the same time yesterday, today and
        # tomorrow, then it is ambiguous as to when it ends.
        # I don't know how prevalent this is, so for now I'll make it
        # an exception, and address it conclusively if it arises.
        # If it arises, making it return "today" should work okay-ish.
        # Alternatively, this could return two objects, one with it
        # ending "today" and one with it ending "tomorrow".
        # The latter case will require additional checks regarding
        # duplicates.
        raise Exception
      elif (ending[0] == 1 and ending[1] == 1) or (ending[1] == 1 and ending[2] == 1):
        # Ambiguous, but we can return two values
        if ending[0] == 1 and ending[1] == 1:
          # Cannot end yesterday
          return DayObj
        elif ending[1] == 1 and ending[2] == 1:
          return [DayObj, tomorrow]
        else:
          print ending, query
          raise Exception
      elif ending[1] == 1 and ending[2] == 0:
        # Not ambiguous, it ends "today"
        return DayObj
      elif ending[1] == 0 and ending[2] == 1:
        # Not ambiguous, it ends "tomorrow"
        return tomorrow
      elif ending[0] == 1 and ending[1] == 0:
        # Erroneous, the trip can't end "yesterday" if it is running "today"
        print ending, query
        raise Exception
      else:
        print ending, query
        raise Exception
      
    elif nottoday == False and today == True:
      # Trip starts and ends before midnight, but could still be erroneous:
      # another check if done in self.getTripEndTime to make sure that 
      # the start and end times are sequential
      if verbose:
        print "Trip starts and ends before midnight"
      return DayObj
    elif nottoday == True and today == False:
    # Trip does not even run on this day of the week
      return None
      
  def getTripDuration(self, DayObj):
    '''
    Returns the duration of the trip, defined as the time elapsed between
    the self.getTripStartTime(<DayObj>) and the self.getTripEndTime(<DayObj>).
    
    Returns an object of type='datetime.timedelta'. To convert this to
    seconds, use timedelta.total_seconds()
    
    Returns None if the trip does not run on <DayObj>.
    '''
    if self.doesTripRunOn(DayObj):
      return self.getTripEndTime(DayObj) - self.getTripStartTime(DayObj)
    else:
      return None
      
  def getTripSpeed(self, DayObj):
    '''
    Returns the average speed for the total length and duration of the trip.
    Ignores dwelling time (time spent stopped): that is, to be clear,
    a trip that explicitly includes stopping time in its GTFS scheduling
    will appear slower than a trip that does not. This is a straightforward
    calculation that ignores possible embellishments in the calculation.
    
    from osgeo import ogr
    from shapely.wkb  import loads
    
    Returns speed as kilometres per hour.
    '''
    hours = self.getTripDuration(DayObj).total_seconds() / 60.0 / 60.0
    sline_length_KM = self.getShapelyLineProjected().length / 1000.0
    
    return sline_length_KM / hours   
      
  def doesTripRunOn(self, DayObj, verbose=False):
    '''
    Returns a Boolean to determine if the PTTrip runs on <DayObj>.
    Note that this is NOT as simple as checking the GTFS calendar table:
    a trip can start before midnight and end the next day.
    The typical database representation of this is to record such trips
    as being on the (say) Saturday but not the Sunday, because the trip
    did not originate on Saturday. I think this is wrong, so this code
    corrects it.

    Thus, a trip that starts on Saturday and ends on Sunday will return
    True for Saturday and for Sunday, even if the GTFS feed only says it
    runs on the Saturday.
    
    NOTE: This check cannot be performed by simply checking if the
    PTService runs on <DayObj>, as PTServices do not account for the
    "midnight bug".
    '''
    def checkIfAfterMidnight(self, DayObj):
      '''Brief interior function that checks if self actually runs beyond midnight, and therefore runs for more than one day'''
      q = Template('SELECT min(departure_time), max(departure_time) FROM stop_times WHERE trip_id = "$trip_id"')
      query = q.substitute(trip_id = self.trip_id)
      self.cur.execute(query)
      result = self.cur.fetchall()
      start, end = result[0][0], result[0][1]
      if int(start[0:2]) >= 24 and int(end[0:2]) >= 24:
        # '28:00:00.000' -->> 28
        # Then the trip ends some time after midnight, and this needs to insure that True is returned when asked if the trip runs today.
        return (True, True)
      elif int(start[0:2]) < 24 and int(end[0:2]) >= 24:
        # The trip starts before midnight and finishes after it
        return (False, True)
      elif int(start[0:2]) >= 24 and int(end[0:2]) < 24:
        ## return (True, False)
        raise CustomException("How can a trip start after midnight and finish before it?")
      else:
        # The trip does not end with a time beyond "23:59:59.999"
        return (False, False)
        
    q = Template('SELECT * FROM calendar WHERE service_id = "$service_id"')
    serviceid = self.getService().service_id
    query = q.substitute(service_id = serviceid)
    if verbose:
      print query
    self.cur.execute(query)
    info = self.cur.fetchone()
    Week = {"Monday": False, "Tuesday": False, "Wednesday": False, "Thursday": False, "Friday": False, "Saturday": False, "Sunday": False}

    minuit = checkIfAfterMidnight(self, DayObj)
    protectMonday, protectTuesday, protectWednesday, protectThursday, protectFriday, protectSaturday, protectSunday = False, False, False, False, False, False, False

    if info[1] == 1:
      Week["Monday"] = True
      if minuit[1] == True:
        Week["Tuesday"] = True
        protectTuesday = True
      if minuit[0] == True and protectMonday == False:
        Week["Monday"] = False

    if info[2] == 1:
      Week["Tuesday"] = True
      if minuit[1] == True:
        Week["Wednesday"] = True
        protectWednesday = True
      if minuit[0] == True and protectTuesday == False:
        Week["Tuesday"] = False

    if info[3] == 1:
      Week["Wednesday"] = True
      if minuit[1] == True:
        Week["Thursday"] = True
        protectThursday = True
      if minuit[0] == True and protectWednesday == False:
        Week["Wednesday"] = False

    if info[4] == 1:
      Week["Thursday"] = True
      if minuit[1] == True:
        Week["Friday"] = True
        protectFriday = True
      if minuit[0] == True and protectThursday == False:
        Week["Thursday"] = False

    if info[5] == 1:
      Week["Friday"] = True
      if minuit[1] == True:
        Week["Saturday"] = True
        protectSaturday = True
      if minuit[0] == True and protectFriday == False:
        Week["Friday"] = False

    if info[6] == 1:
      Week["Saturday"] = True
      if minuit[1] == True:
        Week["Sunday"] = True
        protectSunday = True
      if minuit[0] == True and protectSaturday == False:
        Week["Saturday"] = False

    if info[7] == 1:
      Week["Sunday"] = True
      if minuit[1] == True:
        Week["Monday"] = True
        protectMonday = True
      if minuit[0] == True and protectSunday == False:
        Week["Sunday"] = False
        
    if verbose:
      print Week
  
    DOW = DayObj.dayOfWeekStr.title()
    if verbose:
      print "The method is considering a " + DOW
    tripdate = self.getTripStartDay(DayObj)
    if tripdate == None:
      return False
    elif isinstance(tripdate, list):
      # The trip goes over midnight
      return True
    elif isinstance(tripdate, Day):
      tripdate = tripdate.isoDate + ".000"
      
    if Week[DOW] is True:
      # Then the trip does run on this day of the week, but we still need to check if there's an exception
      # for this particular date.
      
      # The start of the trip is either "today" (DayObj) or "yesterday" (the day before DayObj),
      # depending on whether the trip crosses midnight.
      # This date is the relevant one to check for exceptions.
      try:
        q = Template('SELECT * FROM calendar_dates WHERE service_id = "$service_id" and date = "$date"')
        query = q.substitute(service_id = serviceid, date = tripdate)
        if verbose:
          print query
        self.cur.execute(query)
        exceptions = self.cur.fetchall()
        for exception in exceptions:
          excdate, exctype = exception[1], exception[3]
          if excdate == tripdate and exctype == 'Removed':
            # The trip normally runs on this day, but today is an exception
            return False
        # Once all relevant exceptions have been checked, it is confirmed that the trip does run on <DayObj>
        return True
      except:
        # There are never any exceptions for this trip
        return True
    else:
      # Even if the trip does not normally run on this day of the week,
      # there may still be exceptions in the form of ADDITIONS
      q = Template('SELECT * FROM calendar_dates WHERE service_id = "$service_id" and date = "$date"')
      query = q.substitute(service_id = serviceid, date = tripdate)
      if verbose:
        print query
      self.cur.execute(query)
      exceptions = self.cur.fetchall()
      for exception in exceptions:
        excdate, exctype = exception[1], exception[3]
        if excdate == tripdate and exctype == 'Added':
          return True
          
      # Once all relevant exceptions have been checked and no additions have been found,
      # we have confirmed that the trip does not run on <DayObj>
      return False

  def getRoute(self):
    '''
    Returns the Route object that represents the path taken along PTtrip.
    '''
    routeOfTrip = Route(self.database, self.route_id)
    return routeOfTrip

  def getService(self):
    '''
    Returns the PTService object that includes this trip.
    '''
    q = Template('SELECT service_id FROM trips WHERE trip_id = $trip_id')
    query = q.substitute(trip_id = self.trip_id)
    self.cur.execute(query)
    PTServiceOfTrip = PTService(self.database, self.cur.fetchall()[0][0])
    return PTServiceOfTrip

  def getShapeID(self):
    '''
    Each trip has a particular shape.
    '''
    # Update up-top
    q = Template('SELECT DISTINCT shape_id FROM trips WHERE trip_id = "$trip_id"')
    query = q.substitute(trip_id = self.trip_id)
    self.cur.execute(query)
    shape_id = self.cur.fetchall()[0][0]
    try:
      shape_id = shape_id.replace('\n','') # Metlink includes line breaks
    except:
      shape_id = shape_id

    try:
      shape_id = shape_id.replace('\r','') # Metlink includes line breaks
    except:
      shape_id = shape_id

    shape_id.strip(" ")

    return shape_id

  def getShapelyLine(self, precise=True):
    '''
    Returns a Shapely Line object representing the trip.
    
    Type=LineString
    '''
    q = Template('SELECT shape_pt_lon, shape_pt_lat FROM shapes WHERE shape_id = "$shape_id" ORDER BY shape_pt_sequence')
    query = q.substitute(shape_id = self.getShapeID())
    self.cur.execute(query)

    vertices = []
    if precise == False:
      for vertex in self.cur.fetchall():
        newvertex0 = round(vertex[0], 7) # Restrict it to 7 dp, like the stops have.
        newvertex1 = round(vertex[1], 7)
        vertices.append((newvertex0, newvertex1))
    elif precise == True:
      vertices = [vertex for vertex in self.cur.fetchall()]

    return LineString(vertices)
    
  def getShapelyLineProjected(self, source=4326, target=2134):
    '''
    Projects self.getShapelyLine from <source> GCS to <target> PCS.
    
    2134 = NZGD2000 / UTM zone 59S (default <target>)
    4326 = WGS84 (default <source>)
    
    Returns a LineString object.
    '''
    to_epsg=target
    from_epsg=source
    
    to_srs = ogr.osr.SpatialReference()
    to_srs.ImportFromEPSG(to_epsg)
    
    from_srs = ogr.osr.SpatialReference()
    from_srs.ImportFromEPSG(from_epsg)
    
    ogr_geom = ogr.CreateGeometryFromWkb(self.getShapelyLine().wkb)
    ogr_geom.AssignSpatialReference(from_srs)
    
    ogr_geom.TransformTo(to_srs)
    return loads(ogr_geom.ExportToWkb())
    
  def prettyPrintShapelyLine(self):
    '''
    Pretty prints Shapely lines in WKT, so that they can be directly
    copied from the terminal, into a TXT file and put into QGIS.
    '''
    import shapely.geometry
    coords = self.getShapelyLine().coords
    print "vertex,wktpoint;"
    for n, c in enumerate(coords):
      print str(n) + "," + shapely.geometry.Point(c[0], c[1]).wkt + ";"
    print ""
    print myTrip.getShapelyLine().wkt

  def plotShapelyLine(self):
    '''
    Uses matplotlib to draw a quick representation of a trip.
    Uses Shapely via a dependant method.
    Uses mpl_toolkits.basemap, and projects to a Cassini projection.
    Does not plot stops (yet?).
    '''
    from matplotlib import pyplot as plt
    import matplotlib
    matplotlib.rcParams['backend'] = "Qt4Agg"
    from mpl_toolkits.basemap import Basemap

    line = self.getShapelyLine()
    bounds = line.bounds
    minx, miny, maxx, maxy = bounds[0]-0.005, bounds[1]-0.005, bounds[2]+0.005, bounds[3]+0.005
    m = Basemap(llcrnrlon=minx, llcrnrlat=miny, urcrnrlon=maxx, urcrnrlat=maxy, resolution='f',projection='cass',lon_0=line.centroid.x, lat_0=line.centroid.y)
    m.drawcoastlines(linewidth=.2)
    m.fillcontinents(color='#CDBC8E',lake_color='#677D6C')
    m.drawmapboundary(fill_color='#677D6C')

    lats, lons = [], []
    for vertex in list(line.coords):
      lons.append(vertex[0])
      lats.append(vertex[1])

    x,y = m(lons,lats)

    m.plot(x,y,c='#BA5F22',alpha=1,zorder=2)

    title = self.getRoute().getLongName().strip('"')
    plt.title(title)
    return plt.show()

  def getStopsInSequence(self, verbose=False):
    '''
    Returns a list of stop objects that the trip uses, in sequence.
    '''
    q = Template('SELECT stop_id FROM stop_times WHERE trip_id = "$trip_id" ORDER BY stop_sequence')
    query = q.substitute(trip_id = self.trip_id)
    self.cur.execute(query)
    if verbose:
      print query

    return [Stop(self.database, stop[0]) for stop in self.cur.fetchall()]

  def whereIsVehicle(self, DayObj, write=False):
    '''
    If self (trip) runs on <DayObj>, returns a list of tuples of integers
    and shapely.geomoetry.Point objects representing the seconds since
    midnight on <DayObj> and the position of the vehicle along its route
    shape.
    
    <write> (Boolean, default=False) controls whether the result is to be
    written to the database. If the trip_id is already in the database,
    the old trip_id is over-written with the new.
    '''
    def scale_factor(line, nominallength):
      '''
      Because the length implied by the database may not be the same as
      the length of the line feature that represents it,
      this function returns a value that can be used to scale the distances
      given by the GTFS up (or down) to the scale of the line feature.
      <linelength> and <nominallength> are both floats.
      '''
      return line.length / float(nominallength)
    
    def cut(line, distance):
      '''
      Cuts a line in two at a distance from its starting point.
      Source: shapely manual, linestrings: http://toblerity.org/shapely/manual.html#linear-referencing-methods
      '''
      if distance <= 0.0  or distance >= line.length:
        return [LineString(line)]
      coords = list(line.coords)
      for i, p in enumerate(coords):
        pd = line.project(Point(p))
        if pd == distance:
          return [LineString(coords[:i+1]), LineString(coords[i:])]
        if pd > distance:
          cp = line.interpolate(distance)
          return [LineString(coords[:i] + [(cp.x, cp.y)]), LineString([(cp.x, cp.y)] + coords[i:])]
    
    def interpolatedposition(stop1distalong, stop1depart, stop2distalong, stop2arrive, routeshape, relativesecond):
      '''
      Interior function to return the position along routeshape, between
      stop1 and stop2, that the vehicle will be at at <relativesecond>.
      <relativesecond> is the seconds passed since the trip departed stop1.
      '''
      if stop1distalong > stop2distalong:
        raise Exception
      # Remove the head segment
      line = cut(routeshape, stop1distalong)
      if len(line) > 1:
        line = line[1]
      else:
        line = line[0]
      # Remove the tail segment
      stop2distalong = stop2distalong-stop1distalong # stop2distalong shortened by length of stop1distalong
      line = cut(line, stop2distalong)
      if len(line) > 1:
        line = line[0]
      else:
        line = line[0]
      # line is now a segment of routeshape, between stop1 and stop2
      # travel_time is the time the vehicle takes to travel along the segment
      travel_time = float((stop2arrive - stop1depart).seconds)
      # What fraction of travel_time is second?
      try:
        fraction = relativesecond / travel_time
      except ZeroDivisionError:
        # This is possible (and intended) if the same stop is given for
        # stop1 as stop2
        fraction = 0.0
      # Return a point at the specified distance along a linear geometric object
      # normalized=True means that the distance is interpolated as a fraction of the object's length
      return line.interpolate(fraction, normalized=True)
      
    def cutLineAtMultiple(line, stopdistalongs):
      '''
      To avoid the need to cut and interpolate along lines multiple times
      when certain actions need only be performed once, this function
      segments a Shapely <line> into segments given in <stopdistalongs>,
      an ordered list of the locations of stops given as distances along
      a line.
      '''
      segments = {}
      for n, distance in enumerate(stopdistalongs):
        # n starts at 0
        try:
          m = n + 1
          tester = stopdistalongs[m]
        except IndexError:
          # n is end of trip
          m = n
        if stopdistalongs[n] > stopdistalongs[m]:
          print stopdistalongs
          print stopdistalongs[n], stopdistalongs[m]
          print n, m
          raise Exception
        # Remove the head segment
        seg = cut(line, stopdistalongs[n])
        if len(seg) > 1:
          seg = seg[1]
        else:
          seg = seg[0]
        # Remove the tail segment
        seglength = stopdistalongs[m] - stopdistalongs[n]
        seg = cut(seg, seglength)
        if len(seg) > 1:
          seg = seg[0]
        else:
          seg = seg[0]
        segments[n] = seg
      return segments
    
    def interpolatedOnSegment(segment, stop1depart, stop2depart, relativesecond):
      '''
      <segment> is a single segment from the dictionary returned in
      cutLineAtMultiple(). This method returns the interpolate position
      at <relativesecond> between stop1 and stop2.
      <relativesecond> is the number of seconds that have passed sine the
      veghicle departed stop1.
      '''
      travel_time = float((stop2depart-stop1depart).seconds)
      try:
        fraction = relativesecond / travel_time
      except ZeroDivisionError:
        fraction = 0.0
      return segment.interpolate(fraction, normalized=True)
    
    # Begin method proper
    positionlist = []
    
    factor = 10 # The multiplication factor, idiosyncratic to the GTFS
    #!! Use <factor> to adjust the shape_dist_traveled column in stop_times
    
    # Things that only need to be done once
    ## Get all the stops that the trip visits
    q = Template('SELECT ST.*, S.stop_lat, S.stop_lon FROM stop_times AS ST JOIN stops AS S ON S.stop_id = ST.stop_id WHERE trip_id = $trip_id ORDER BY stop_sequence')
    query = q.substitute(trip_id = self.trip_id)
    self.cur.execute(query)
    Stop_Times = self.cur.fetchall()
    line = self.getShapelyLineProjected()
    nominallength = Stop_Times[-1][10] * factor
    scalefactor = scale_factor(line, nominallength)
    Overall_Start = self.getTripStartTime(DayObj)
    Overall_End = self.getTripEndTime(DayObj)
    
    # Stop arrival/departures
    stoparrivedepart, seencount, stopdistalongs, stopobjs = {}, {}, [], []
    successat = None # For fewer SQL statements and the edge-case where
                     # the route doubles-back on itself.
    for n, stop in enumerate(Stop_Times):
      stopobj = Stop(self.database, stop[3])
      stopobjs.append(stopobj)
      try:
        seen = seencount[stopobj.stop_id]
        seencount[stopobj.stop_id] = seencount[stopobj.stop_id] + 1
      except KeyError:
        seen = 0
        seencount[stopobj.stop_id] = 1
      stoparrivedepart[n] = stopobj.getStopTime(self, DayObj)[seen]
      stopdistalongsuccess = False
      step = 1
      while stopdistalongsuccess == False:
        try:
          stopdistalongs.append(min((stopobj.getGivenDistanceAlong(self, max(successat, n+step), factor=factor) * scalefactor), (nominallength*scalefactor)))
          stopdistalongsuccess = True
          successat = n+step
        except TypeError:
          # Some trips skip stops and so have gaps in 'stop sequence', producing None for Stop.getGivenDistanceAlong
          step += 1
          stopdistalongsuccess = False
    segmentedline = cutLineAtMultiple(line, stopdistalongs)
    for second in range(0,24*60*60,1): # 12am to 11.59pm on <DayObj>, at 1 second intervals
      Second_as_Second = second
      Second = DayObj.datetimeObj + datetime.timedelta(seconds=second)
      if Second >= Overall_Start and Second <= Overall_End:
        # Then the trip is operating at <Second>
        # Now, refine the precise position using scheduled times.
        counts = {} # To keep a count of how many times a trip visits a stop
        for n, stop in enumerate(Stop_Times):
          segment = segmentedline[n] # The segment of the line from <stop> to its next stop (and no further)
          stopobj = stopobjs[n]
          # LIST OF TUPLE(S), each tuple representing an arrival/departure at the stop
          arrival_departure = stoparrivedepart[n] # TUPLE
          if Second == arrival_departure[0] or Second == arrival_departure[1] or (Second > arrival_departure[0] and Second < arrival_departure[1]):
            # Trip is arriving, departing or dwelling at stop
            ## return stopobj.getStopSnappedToRoute(Trip, projected=True) ## Logically, this is sensible.
            ## But the interpolate on a projected line seems to be off.
            ## So instead, I interpolate the position at a stop in the same manner I would for a betwee-stop point
            relativeseconds = Second_as_Second - (arrival_departure[1] - DayObj.datetimeObj).total_seconds()
            positionlist.append((second, interpolatedOnSegment(segment, arrival_departure[0], arrival_departure[0], relativeseconds)))
          elif Second > arrival_departure[1]:
            # elif second is after departing the current stop (but still in trip's time range)
            next_stopobj = stopobjs[n+1]
            try:
              counts[Stop_Times[n+1][3]] = counts[Stop_Times[n+1][3]] + 1
            except:
              counts[Stop_Times[n+1][3]] = 1
            index = counts[Stop_Times[n+1][3]]
            counts[Stop_Times[n+1][3]] = counts[Stop_Times[n+1][3]] - 1
            next_arrival = stoparrivedepart[n+1][index-1]
            if Second < next_arrival:
              # Then second is between stop and the next stop
              # Need the relative seconds: <second> rendered as time passed since trip departed stop
              relativeseconds = Second_as_Second - (arrival_departure[1] - DayObj.datetimeObj).total_seconds()
              # Need to interpolate its position
              positionlist.append((second, interpolatedOnSegment(segment, arrival_departure[0], next_arrival, relativeseconds)))
          # Move to next [n, stop] if no match found
      else:
        pass
    if write == False:
      # Then just return the result
      return positionlist
    elif write == True:
      # Then record the result in the database and return None
      # 1. Check if the trip has already been recorded: if so, delete it
      query = 'DELETE FROM intervals WHERE trip_id = %s' % (str(self.trip_id))
      self.cur.execute(query)
      self.database.commit
      # 2. Add the data to the table one row at a time, then commit
      # 2a. Get universally-applicable data
      trip_id = self.trip_id
      day = DayObj.isoDate[0:10] # e.g. 2013-12-08
      route = self.getRoute()
      route_type_desc = route.getMode().modetype
      agency_id = self.getAgencyID()
      route_id = route.route_id
      shape_id = str(self.getShapeID())
      for posi in positionlist:
        second = posi[0]
        lat = posi[1].y
        lon = posi[1].x
        ##pickup_type_text = None # For a later version
        ##drop_off_type_text = None # For a later version
        query = 'INSERT INTO intervals VALUES ("%i", "%s", "%i", "%f", "%f", "%s", "None", "None", "%s", "%s", "%s");' % (trip_id, day, second, lat, lon, route_type_desc, agency_id, route_id, shape_id)
        self.cur.execute(query)
      self.database.commit()
      return None

class Stop(Database):
  '''
  A stop is a place where a PT vehicle stops and passengers may board
  or depart. Routes (and hence PTTrips) are essentially comprised of an
  ordered sequence of Stops.
  '''
  def __init__(self, database, stop_id):
    '''
    A stop_id is database unique.
    '''
    Database.__init__(self, database)
    self.stop_id = stop_id

  def getStopCode(self):
    '''
    Returns the stop_code, a short(er) integer version similar to stop_id, but published on signs and used in passenger text alerts.
    '''
    q = Template('SELECT stop_code FROM stops WHERE stop_id = "$stop_id"')
    query = q.substitute(stop_id = self.stop_id)
    self.cur.execute(query)
    return self.cur.fetchall()[0][0]

  def getStopName(self):
    '''
    Returns the stop_name, a long name of the stop (String).
    '''
    q = Template('SELECT stop_name FROM stops WHERE stop_id = "$stop_id"')
    query = q.substitute(stop_id = self.stop_id)
    self.cur.execute(query)
    try:
      return self.cur.fetchall()[0][0].strip('"') # Removes quotation marks present in Metlink feeds
    except:
      return self.cur.fetchall()[0][0]

  def getStopDesc(self):
    '''
    Returns the stop_desc, a short but textual name for the stop.
    '''
    q = Template('SELECT stop_desc FROM stops WHERE stop_id = "$stop_id"')
    query = q.substitute(stop_id = self.stop_id)
    self.cur.execute(query)
    try:
      return self.cur.fetchall()[0][0].strip('"') # Removes quotation marks present in Metlink feeds
    except:
      return self.cur.fetchall()[0][0]

  def getLocationType(self):
    '''
    Returns location_type_desc from the stops table: ["Stop", "Station", "Hail and Ride"]
    For Metlink: ["Stop", "Hail and Ride"]
    '''
    q = Template('SELECT location_type_text FROM stops WHERE stop_id = "$stop_id"')
    query = q.substitute(stop_id = self.stop_id)
    self.cur.execute(query)
    self.cur.execute
    return self.cur.fetchall()[0][0]

  def getShapelyPoint(self):
    '''
    Returns a shapely Point object representing the location of the stop.
    See http://toblerity.org/shapely/manual.html for more information on this Object.
    '''
    q = Template('SELECT stop_lat, stop_lon FROM stops WHERE stop_id = "$stop_id"')
    query = q.substitute(stop_id = self.stop_id)
    self.cur.execute(query)
    loc = self.cur.fetchall()[0]
    lat, lon = round(loc[0], 7), round(loc[1], 7)
    return Point(lon, lat) # Shapely Point object... try Point.x, Point.y, etc.
    
  def getShapelyPointProjected(self, source=4326, target=2134, verbose=False):
    '''
    Returns a Shapely point representing the location of the stop,
    projected from the <source> GCS to the <target> PCS.
    
    2193 = NZGS2000 / NZTM 2000
    2134 = NZGD2000 / UTM zone 59S (default <target>)
    4326 = WGS84 (default <source>)
    '''
    to_epsg=target
    from_epsg=source
    
    to_srs = ogr.osr.SpatialReference()
    to_srs.ImportFromEPSG(to_epsg)
    
    from_srs = ogr.osr.SpatialReference()
    from_srs.ImportFromEPSG(from_epsg)
    
    ogr_geom = ogr.CreateGeometryFromWkb(self.getShapelyPoint().wkb)
    if verbose: print ogr_geom, self.getShapelyPoint().x, self.getShapelyPoint().y
    ogr_geom.AssignSpatialReference(from_srs)
    ogr_geom.TransformTo(to_srs)
    if verbose: print ogr_geom
    if verbose: print loads(ogr_geom.ExportToWkb()).x, loads(ogr_geom.ExportToWkb()).y
    return loads(ogr_geom.ExportToWkb())
    
  def countVisitsInDay(self, DayObj):
    '''
    Given a Day object, returns the the number of vehicles that stop at
    self (Stop) on Day, from 00:00.00 to 23:59.59
    '''
    q = Template("SELECT trip_id FROM stop_times WHERE stop_id = '$stop_id'")
    query = q.substitute(stop_id = self.stop_id)
    self.cur.execute(query)
    retcount = 0
    for tripid in self.cur.fetchall():
      if PTTrip(self.database, tripid[0], DayObj).runstoday:
        retcount += 1
    return retcount
    
  def getStopTime(self, TripObj, DayObj):
    '''
    Returns a list of (arrival, departure) time tuples.
    The elements of the tuple are datetime.datetime objects.
    They are in the same order as the stops visited along <TripObj>'s
    route on <DayObj>.
    '''
    def prepare_tuple(fetchall, DayObj):
      retlist = []
      for stop in fetchall:
        stop_time = stop
        arrival_time, departure_time = stop_time[0], stop_time[1] # Raw strings
        arrival_hour, arrival_min, arrival_sec, arrival_ssec = arrival_time[0:2], arrival_time[3:5], arrival_time[6:8], arrival_time[9:]
        departure_hour, departure_min, departure_sec, departure_ssec = departure_time[0:2], departure_time[3:5], departure_time[6:8], departure_time[9:]
        startday = TripObj.getTripStartDay(DayObj)
        if isinstance(startday, Day):
          if int(arrival_hour) < 24:
            # Then it is not post-midnight
            stop_arrival_datetime = startday.datetimeObj.combine(startday.datetimeObj, datetime.time(int(arrival_hour), int(arrival_min), int(arrival_sec), int(arrival_ssec)))
          elif int(arrival_hour) >= 24:
            # Time needs to be next day as well
            arrival_hour = str(int(arrival_hour) - 24)
            if len(arrival_hour) < 2:
              arrival_hour = "0" + arrival_hour
            nextday = DayObj.tomorrowObj
            stop_arrival_datetime = nextday.combine(nextday, datetime.time(int(arrival_hour), int(arrival_min), int(arrival_sec), int(arrival_ssec)))
          if int(departure_hour) < 24:
            stop_departure_datetime = startday.datetimeObj.combine(startday.datetimeObj, datetime.time(int(departure_hour), int(departure_min), int(departure_sec), int(departure_ssec)))
          elif int(departure_hour) >= 24:
            departure_hour = str(int(departure_hour) - 24)
            if len(departure_hour) < 2:
              departure_hour = "0" + departure_hour
            if nextday not in locals():
              nextday = DayObj.tomorrowObj
            stop_departure_datetime = nextday.combine(nextday, datetime.time(int(departure_hour), int(departure_min), int(departure_sec), int(departure_ssec)))
          retlist.append((stop_arrival_datetime, stop_departure_datetime))
      return retlist
      
    # 1. Check if trip runs on DayObj
    if TripObj.doesTripRunOn(DayObj) == True:
      # 2. Get the raw arrival and departure times
      q = Template('SELECT arrival_time, departure_time FROM stop_times WHERE stop_id = "$stop_id" and trip_id = "$trip_id" ORDER BY stop_sequence ASC')
      query = q.substitute(stop_id = self.stop_id, trip_id = TripObj.trip_id)
      self.cur.execute(query)
      stops = self.cur.fetchall()
      # Returns a list, because in some cases there are trips that
      # visit the same stop twice (or potentially more) in one trip:
      # loop routes.
      return prepare_tuple(stops, DayObj)
    else:
      return None

  def getStopSnappedToRoute(self, TripObj, projected=True, new=True):
    '''
    The Stops listed in the GTFS do not have to intersect the Routes which
    are essentially defined by them. This method returns a Shapely.geometry
    Point object representing the location of the Stop when shifted the
    minimum neccessary distance to intersect the <RouteObj>.
    
    elif new == False adapted from:
    http://gis.stackexchange.com/questions/396/nearest-neighbor-between-a-point-layer-and-a-line-layer
    Date: 20140101
    '''
    if new == True:
      if projected == True:
        stoploc = self.getShapelyPointProjected()
        routeline = TripObj.getShapelyLineProjected()
      elif projected == False:
        stoploc = self.getShapelyPoint()
        routeline = TripObj.getShapelyLine()
      return routeline.interpolate(routeline.project(stoploc))
      
    elif new == False:
      # Define the line and point of interest
      if projected == False:
        stoploc = self.getShapelyPoint()
        routeline = TripObj.getShapelyLine()
      elif projected == True:
        stoploc = self.getShapelyPointProjected()
        routeline = TripObj.getShapelyLineProjected()
      
      # pairs iterator:
      # http://stackoverflow.com/questions/1257413/1257446#1257446
      def pairs(lst):
          i = iter(lst)
          first = prev = i.next()
          for item in i:
              yield prev, item
              prev = item
          yield item, first

      # these methods rewritten from the C version of Paul Bourke's
      # geometry computations:
      # http://local.wasp.uwa.edu.au/~pbourke/geometry/pointline/
      def magnitude(p1, p2):
          vect_x = p2.x - p1.x
          vect_y = p2.y - p1.y
          return sqrt(vect_x**2 + vect_y**2)

      def intersect_point_to_line(point, line_start, line_end):
          line_magnitude =  magnitude(line_end, line_start)
          u = ((point.x - line_start.x) * (line_end.x - line_start.x) +
               (point.y - line_start.y) * (line_end.y - line_start.y)) \
               / (line_magnitude ** 2)

          # closest point does not fall within the line segment, 
          # take the shorter distance to an endpoint
          if u < 0.00001 or u > 1:
              ix = magnitude(point, line_start)
              iy = magnitude(point, line_end)
              if ix > iy:
                  return line_end
              else:
                  return line_start
          else:
              ix = line_start.x + u * (line_end.x - line_start.x)
              iy = line_start.y + u * (line_end.y - line_start.y)
              return Point([ix, iy])
              
      def attemptSnap(line, point):
        min_dist = maxint
        for seg_start, seg_end in pairs(list(routeline.coords)[:-1]):
            line_start = Point(seg_start)
            line_end = Point(seg_end)

            intersection_point = intersect_point_to_line(point, line_start, line_end)
            cur_dist =  magnitude(point, intersection_point)

            if cur_dist < min_dist:
                min_dist = cur_dist
                nearest_point = intersection_point
        return nearest_point
      
      if stoploc.intersects(routeline) == False:
        stoploc = attemptSnap(routeline, stoploc)
         
      return stoploc
      
      
  def getGivenDistanceAlong(self, TripObj, stop_sequence, factor=None):
    '''
    The database records the distance along the route that the stop is.
    Although this can be inferred with high accuracy, there are edge cases
    where this would be erroneous (points jumping to their nearest edge
    may be moving away from the actual stop location).
    
    <stop_sequence> (integer) must be given, as a PTTtrip can visit a 
    stop more than once.
    
    <factor> can be used to scale numbers (e.g. km-->m requires factor=1000.
    
    Returns a float.
    
    Returns None if there is no match.
    '''
    q = Template('SELECT shape_dist_traveled FROM stop_times WHERE stop_id = "$stop_id" AND trip_id = "$trip_id" and stop_sequence = "$stop_sequence"')
    query = q.substitute(stop_id = self.stop_id, trip_id = TripObj.trip_id, stop_sequence = stop_sequence)
    self.cur.execute(query)
    dist = self.cur.fetchall()
    if len(dist) == 1 :
      if factor is None:
        return float(dist[0][0])
      else:
        return float(dist[0][0]) * factor
    else:
      return None

if __name__ == '__main__':
  ################################################################################
  ########################## Testing Section #####################################
  ################################################################################
  '''
  # Testing
  myDatabase = Database(myDB)
  myDay = Day(myDB, datetimeObj=datetime.datetime(2013, 12, 6))
  myTrip = PTTrip(myDB, 1)
  print myTrip.doesTripRunOn(myDay)
  print myTrip.doesRouteRunOn(myDay)
  '''
  
  # Populating intervals table
  myDatabase = Database(myDB)
  myDatabase.populateIntervals(DayObj=Day(myDB, datetimeObj=datetime.datetime(2013, 12, 7)), DB=myDB, starti=743, endtime=datetime.time(22, 30))
  
  '''
  # Animating
  myDatabase = Database(myDB)
  myDay = Day(myDB, datetimeObj=datetime.datetime(2013, 12, 9))
  myDay.animateDay(0, 24*60*60, 174.7, -41.35, .25, "2:1", sourceproj=2134, projected=True, lon_0=173.0, lat_0=0.0, targetproj='tmerc', outoption="video", placetext="Wellington Public Transport", skip=30, filename='WellingtonMonday24h.mp4')
  '''
  
  '''
  # Hexbinning
  myDatabase = Database(myDB)
  myDay = Day(myDB, datetimeObj=datetime.datetime(2013, 12, 9))
  #myDay.hexbinStopVisits(projected=False)
  myDay.nvd3FrequencyByMode(n=60*15)
  '''
  ################################################################################
  ################################ End ###########################################
  ################################################################################
