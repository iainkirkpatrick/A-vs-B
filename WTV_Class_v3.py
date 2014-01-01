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

#    Day(Database)                       ::A date. PT runs by daily schedules, considering things like whether it is a weekday, etc::
#      > __init__(database, datetimeObj) ::<database> is a Database object. <datetimeObj> is a datetime object::
#      > getCanxServices()               :CAUTION:Returns a list of PTService objects that are cancelled according to the calendar_dates table. For Wellington I suspect this table is a little dodgy::
#      > getServicesDay()                ::Returns a list of service IDs of services that are scheduled to run on self (Day). Accounts for exceptional additions and removals of services; but not the midnight bug, as a PTService is not a PTTrip::
#      > plotModeSplitNVD3(databaseObj, city) ::Uses the Python-NVD3 library to plot a pie chart showing the breakdown of vehicle modes (num. services) in Day. Useful to compare over time, weekday vs. weekend, etc. <city> is str, used in the title of the chart::
#      > animateDay()                    :Unfinished, but working::
#      > getActiveTrips(second)          ::Returns a list of PTTrip objects representing those trips that are running on self (Day) at <second>. Accounts for service cancellations and the "midnight bug"::
#      > countActiveTrips(second)        ::Returns an integer count of the number of trips of any mode that are operating at <second> on self (Day), according to self.getActiveTrips(<second>)::
#      > countActiveTripsByMode(second)  ::Returns an dictionary of {mode: integer} pairs similar to self.countActiveTrips(<second>) that breaks it down by mode::
#      > bokehFrequencyByMode(n, Show=False, name="frequency.py", title="frequency.py", graphTitle="Wellington Public Transport Services, ")  ::Returns an HTML graph of the number of active service every <n> seconds, on the second, broken down by mode::
#      > getSittingStops(second)         ::Returns a list of dictionaries which give information about any public transport stops which currently (<second>) have a vehicle sitting at them, on <DayObj>. Correctly handles post-midnight services::
#      > getAllTrips()                   ::Returns a list of PTTrip objects representing those trips that run at least once on self (Day). Accounts for midnight bug correctly::

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
#      > __init__(database, trip_id)     ::<database> is a Database object. <trip_id> is an Integer identifying the trip uniquely. See the database::
#      > getRouteID()                    ::Returns the route_id (String) of the route that the trip follows. Used to construct the Route object which the Trip object inherits::
#      > doesTripRunOn(DayObj)           ::Returns a Boolean reporting whether the PTTtrip runs on <DayObj> or not. Considers the exceptions in calendar_dates before deciding, and handles >24h time::
#      > getRoute()                      ::Returns the Route object representing the route taken on Trip::
#      > getService()                    ::Returns the PTService object that includes this trip::
#      > getShapelyLine()                ::Returns a Shapely LineString object representing the shape of the trip::
#      > getShapelyLineProjected(source=4326, target=2134) ::Returns a projected Shapely LineString object, derived from self.getShapelyLine(), where <source> is the unprojected Shapely LineString GCS, and <target> is the target projection for the output. The defaults are WGS84 (<source>) and NZGD2000 (<target>).
#      > plotShapelyLine()               ::Uses matplotlib and Shapely to plot the shape of the trip. Does not plot stops (yet?)::
#      > getStopsInSequence()            ::Returns a list of the stops (as Stop ibjects) that the trip uses, in sequence::
#      > whereIsVehicle(second, DayObj)  ::Returns a tuple (x, y) or (lon, lat) of the location of the vehicle at a given moment in time, <second>. <second> is a datetime.time object. <DayObj> is a Day object::
#      > intervalByIntervalPosition(DayObj, interval=1) ::WRITES TO THE DATABASE about the positions of every vehicle on <DayObj> at the temporal resolution of <interval>. Does not write duplicates. Make sure to only pass it PTTrips that doesTripRunOn(DayObj) == True::
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
#      > getStopTime(TripObj)            ::Returns a dictionary of {"stop_sequence":integer, "arrival_time":string, "departure_time":string, "pickup_type_text":string, "drop_off_type_text":string, "shape_dist_traveled":float} at the Stop for a given Trip. Strings are used for arrival_time and departure_time where datetime.time objects would be preferred, because these times can exceed 23:59:59.999999, and so cause a value error if instantiated::
#      > getStopSnappedToRoute(TripObj)  ::Returns a Shapely.geometry.point.Point object representing the non-overlapping Stop as a Point overlapping (or very, very nearly overlapping) the Route shape of <TripObj>::

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
def dur( op=None, clock=[time.time()] ):
  '''
  Little timing function to test efficiency.
  Source: http://code.activestate.com/recipes/578776-a-simple-timing-function/
  '''
  if op != None:
    duration = time.time() - clock[0]
    print '%s finished. Duration %.6f seconds.' % (op, duration)
  clock[0] = time.time()

from string import Template
import datetime

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
import numpy as np

import bokeh.plotting

from shapely.geometry import Point, LineString
from osgeo import ogr # Projecting
from shapely.wkb  import loads # Projecting
from math import sqrt # Snapping
from sys import maxint # Snapping

import sqlite3 as dbapi
db_str = "GTFSSQL_Wellington_20131208_215725.db" # Name of database
##db_str = "GTFSSQL_Wellington_20131207_212134__SUBSET__.db" # Subset database, for rapid testing
#db_pathstr = "G:\\Documents\\WellingtonTransportViewer\\Data\\Databases\\" + db_str # Path and name of DB under Windows, change to necessary filepath
db_pathstr = "/media/alphabeta/RESQUILLEUR/Documents/WellingtonTransportViewer/Data/Databases/" + db_str # Path and name of DB under Linux with RESQUILLEUR, change to necessary filepath
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
        return True
      else:
        return False

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
      if PTTrip(self.database, str(sittingstop[2])).doesTripRunOn(self): # If the trip actually runs on the day being considered
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
      pttrip = PTTrip(self.database, trip[0])
      if pttrip.doesTripRunOn(self):
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
    query = 'SELECT DISTINCT trip_id FROM intervals WHERE date = "%s"' % newsecond # Dont change this without referring to self.countActiveTripsByMode first
    self.cur.execute(query)
    nominallyrunning = self.cur.fetchall()
    
    todaystrips = [trip.trip_id for trip in self.getAllTrips()] # Trips that are actually running on self (Day)
    testtrips = [trip_id[0] for trip_id in nominallyrunning] # Trips that have a vehicle at operation at <second> on whatever Day they run
 
    # Return trips that run at <second> AND run on self (Day), as a list of PTTrip objects
    return [PTTrip(self.database, str(trip)) for trip in list(set(todaystrips).intersection(set(testtrips)))]
  
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

  def animateDay(self, start, end):
    '''
    Animates the public transport system for self day.

    Psuedo code:
    Pre: get the maximum and minimum x and y of all the data in the database?
    1. Get all XYs of vehicles that operate in the first second
    2. Display them
    3. Get the next XYs
    4. But do the above with basemap
    '''
    matplotlib.rcParams['backend'] = "Qt4Agg"
    from mpl_toolkits.basemap import Basemap
    from shapely.geometry import Polygon
    import pylab

    self.cur.execute('SELECT MAX(stop_lat), MIN(stop_lat), MAX(stop_lon), MIN(STOP_lon) FROM stops')
    boundary = self.cur.fetchall()[0]
    maxy, miny, maxx, minx = boundary[0], boundary[1], boundary[2], boundary[3]

    #boundary = Polygon([(minx, maxy), (maxx, maxy), (maxx, miny), (minx, miny)])
    #centrex, centrey = boundary.centroid.x, boundary.centroid.y
    centrex, centrey = 174.777222, -41.2888889
    maxy, minx, miny, maxx = -41, 174.6, -41.5, 175.1

    for i in range(start, end+1):

      m = Basemap(llcrnrlon=minx, llcrnrlat=miny, urcrnrlon=maxx, urcrnrlat=maxy, resolution='f',projection='cass',lon_0=centrex, lat_0=centrey)
      m.drawcoastlines(linewidth=.2)
      m.fillcontinents(color='#CDBC8E',lake_color='#677D6C')
      m.drawmapboundary(fill_color='#677D6C')

      buslats, buslons, tralats, tralons, ccllats, ccllons, frylats, frylons = [], [], [], [], [], [], [], []

      q = Template('SELECT date, lat, lon, route_type_desc FROM intervals WHERE date = "$second"')
      query = q.substitute(second = i)
      self.cur.execute(query)
      active = self.cur.fetchall()

      for vehicle in active:
        if vehicle[3] == "Bus":
          buslons.append(vehicle[1])
          buslats.append(vehicle[2])
        elif vehicle[3] == "Rail":
          tralons.append(vehicle[1])
          tralats.append(vehicle[2])
        elif vehicle[3] == "Ferry":
          frylons.append(vehicle[1])
          frylats.append(vehicle[2])
        elif vehicle[3] == "Cable Car":
          ccllons.append(vehicle[1])
          ccllats.append(vehicle[2])

      try:
        x,y = m(buslons,buslats)
        m.scatter(x,y,c='#BA5F22',s=5, alpha=1, zorder=2, lw=0)
      except:
        x,y = m([0.0],[0.0])
        m.scatter(x,y,c='#BA5F22',s=5, alpha=1, zorder=2, lw=0)

      try:
        x,y = m(frylons,frylats)
        m.scatter(x,y,c='#FFFFFF',s=5, alpha=1, zorder=2, lw=0)
      except:
        x,y = m([0.0],[0.0])
        m.scatter(x,y,c='#FFFFFF',s=5, alpha=1, zorder=2, lw=0)

      try:
        x,y = m(ccllons,ccllats)
        m.scatter(x,y,c='#FF0000',s=5, alpha=1, zorder=2, lw=0)
      except:
        x,y = m([0.0],[0.0])
        m.scatter(x,y,c='#FF0000',s=5, alpha=1, zorder=2, lw=0)

      try:
        x,y = m(tralons,tralats)
        m.scatter(x,y,c='#000000',s=5, alpha=1, zorder=2, lw=0)
      except:
        x,y = m([0.0],[0.0])
        m.scatter(x,y,c='#000000',s=5, alpha=1, zorder=2, lw=0)

      title = "Time=%i" % i
      plt.title(title)

      filename = "TestImages/%i.png" % i
      plt.savefig(filename)

      plt.clf()

    import cv2, cv
    from PIL import Image
    from StringIO import StringIO
    sample = cv2.imread(filename)
    fourcc = cv.CV_FOURCC('D', 'I', 'V', 'X')
    fps = 100 # Note: Chris was doing 10 minutes per second
              # For interval=1, that's 600
    height, width, layers = sample.shape
    video = cv2.VideoWriter('TestImages/Video.avi', fourcc, fps, (width,height), 1);

    for i in range(start, end+1):
      img = "TestImages/%i.png" % i
      cap = cv2.imread(img)
      video.write(cap)

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
    alltripsonroute = [PTTrip(self.database, str(trip[0])) for trip in self.cur.fetchall()]
    alltripsonroutetoday = [trip for trip in alltripsonroute if trip.doesTripRunOn(DayObj)]
      
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
  def __init__(self, database, trip_id):
    '''
    A trip_id is database unique.
    '''
    Database.__init__(self, database)
    self.trip_id = trip_id
    Route.__init__(self, database, self.getRouteID())

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
    
  def getTripStartDay(self, DayObj):
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
      yesterday = Day(self.database, DayObj.yesterdayObj)
      today = DayObj.dayOfWeekStr
      tomorrow = Day(self.database, DayObj.tomorrowObj)
      q = Template('SELECT $yesterday, $today, $tomorrow FROM stop_times_amended WHERE trip_id = "$trip_id" ORDER BY stop_sequence ASC')
      query = q.substitute(yesterday = yesterday.dayOfWeekStr, today = today, tomorrow = tomorrow.dayOfWeekStr, trip_id = self.trip_id)
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
      return
      
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

  def whereIsVehicle(self, second, DayObj):
    '''
    Returns an XY position of the vehicle at a given moment in time (<second>) on <dayObj>.
    If the trip does not run, is yet to run, or has already run, it returns None.
    Vehicle locations are "known" at scheduled arrivals, otherwise position is interpolated along their shape.

    <second> is a datetime.time object.

    Returns a (lon, lat) tuple.
    '''
    # Get all the stops that the trip visits
    q = Template('SELECT ST.*, S.stop_lat, S.stop_lon FROM stop_times AS ST JOIN stops AS S ON S.stop_id = ST.stop_id WHERE trip_id = $trip_id ORDER BY stop_sequence')
    query = q.substitute(trip_id = self.trip_id)
    self.cur.execute(query)
    stop_times = self.cur.fetchall()

    latest = datetime.time(23,59,59)

    # Check if the trip is even operating at <second>
    try:
      overall_start = datetime.time(int(stop_times[0][1][0:2]), int(stop_times[0][1][3:5]), int(stop_times[0][1][6:8]), int(stop_times[0][1][9:12]))
    except ValueError:
      if int(stop_times[0][1][0:2]) >= 24:
        # Then the vehicle is operating beyond midnight
        overall_start = latest
    try:
      overall_end = datetime.time(int(stop_times[-1][2][0:2]), int(stop_times[-1][2][3:5]), int(stop_times[-1][2][6:8]), int(stop_times[-1][2][9:12]))
    except ValueError:
      if int(stop_times[-1][2][0:2]) >= 24:
        # Then the vehicle is operating beyond midnight
        overall_end = latest

    if second >= overall_start and second <= overall_end:
      # Then the trip is operating at <second>
      # Now, refine the precise position using scheduled times.

      i = 0 # index the stop searching so we can query the next stop in the sequence
      for stop in stop_times:

        try:
          arrival1 = datetime.time(int(stop[1][0:2]), int(stop[1][3:5]), int(stop[1][6:8]), int(stop[1][9:12]))
        except ValueError:
          arrival1 = latest
        try:
          departure1 = datetime.time(int(stop[2][0:2]), int(stop[2][3:5]), int(stop[2][6:8]), int(stop[2][9:12]))
        except ValueError:
          departure1 = latest

        if second >= arrival1 and second <= departure1:
          # If the trip dwells at the stop and second is within the dwell time range,
          # Return the X, Y of the current stop because we have found the vehicle.
          return (stop[12], stop[11]) # lon, lat

        try:
          arrival2 = datetime.time(int(stop_times[i+1][1][0:2]), int(stop_times[i+1][1][3:5]), int(stop_times[i+1][1][6:8]), int(stop_times[i+1][1][9:12]))
        except ValueError:
          arrival2 = latest
        try:
          departure2 = datetime.time(int(stop_times[i+1][2][0:2]), int(stop_times[i+1][2][3:5]), int(stop_times[i+1][2][6:8]), int(stop_times[i+1][2][9:12]))
        except:
          departure2 = latest

        if second >= arrival2 and second <= departure2:
          # If the trip dwells at the next stop and second is within the dwell time range,
          # Return the X, Y of the next stop because we have found the vehicle.
          return (stop_times[i+1][12], stop_times[i+1][11]) # lon, lat

        if second > departure1 and second < arrival2:
          # If the vehicle is after the first stop but has not yet arrived at the second stop,
          # Then the vehicle is between the two stops,
          # And the task is to infer its location based on distance and time.

          # How many seconds ahead of the departure from stop 1 is <second>?
          ##secondsahead = datetime.datetime.combine(myDay.datetimeObj, second) - datetime.datetime.combine(myDay.datetimeObj, departure1)
          secondsahead = datetime.datetime.combine(DayObj.datetimeObj, second) - datetime.datetime.combine(DayObj.datetimeObj, departure1)
          secondsahead = float(secondsahead.seconds)

          # How many seconds does it take for the vehicle to travel from stop 1 to stop 2?
          ##timeDelta = datetime.datetime.combine(myDay.datetimeObj, arrival2) - datetime.datetime.combine(myDay.datetimeObj, arrival1) # Computes time difference
          timeDelta = datetime.datetime.combine(DayObj.datetimeObj, arrival2) - datetime.datetime.combine(DayObj.datetimeObj, arrival1) # Computes time difference
          timeDelta = float(timeDelta.seconds) # Returns the value purely in seconds

          # Therefore, as a proportion of the travel time between stop 1 and stop 2,
          # how far has the vehicle progressed?
          time_ans = secondsahead / timeDelta

          # How far is stop 1 from the beginning of the route?
          stop1Dist = stop[10]

          # What is the road distance between stop 1 and stop 2?
          diffDist = stop_times[i+1][10] - stop1Dist

          # Therefore, in distance units, how far along the trip is the vehicle?
          dist_ans = stop1Dist + (time_ans * diffDist)

          # How long is the trip, in total?
          totaltripdist = float(stop_times[-1][10])

          # Finally, what proportion of the route has the vehicle travelled?
          proportionTravelled = dist_ans/totaltripdist

          # With that, we can interpolate the vehicle's XY position
          routeShape = self.getShapelyLine()
          interpolatedPosition = routeShape.interpolate(proportionTravelled * routeShape.length)
          return (interpolatedPosition.x, interpolatedPosition.y) # lon, lat

        i += 1
        # If the vehicle is not at or between 1 or 2, then the for loop proceeds to consider stops 2 and 3, until a
        # solution is found.

    else:
      return None

  def intervalByIntervalPosition(self, DayObj, interval=1, updateDB=True):
    '''
    Returns a dictionary of a few values:
    { "TripID": String
      "Position": List of the form: [[SecondsPastMidnight, Position], [SecondsPastMidnight+<interval>, Position],
                  where Position is itself a Tuple: (lon, lat).
      "Modetype": String
      "Operator": String
      "RouteID": String
      "ShapeID": String
    }

    Position is a list of XY tuples indicating the position of a vehicle at each <interval> along its schedule timetable.

    <interval> is a value in seconds.

    **To do:**
    Also add the parameters: "pickingup" and "droppingoff" which are Boolean and indicate whether the vehicle is picking or
    dropping off passengers at the moment in time (determine from the attributes of the stops it is between at a moment.

    Not sure what happens when asked to extend past midnight...
    >> FIX THIS!

    NEW: Writes to the database, rather than returning the values in memory.
    Return only None, but writes to the database if this is appropriate.
    '''
    if self.doesRouteRunOn(DayObj) == True:
      # Infer the time range of the trip
      stops = self.getStopsInSequence()
      start_time, end_time = stops[0], stops[-1]
      start_time, end_time = start_time.getStopTime(self), end_time.getStopTime(self)

      if len(start_time) == 1 and len(end_time) == 1:
        # Then the route does not end where it starts, like most routes
        start_time, end_time = start_time["arrival_time"], end_time["arrival_time"]

      elif len(start_time) == 2 and len(end_time) == 2:
        # Then the first and last stops are visited twiintervalByIntervalPositionce: a loop route
        # Likely, it is a loop that starts and ends at the same place
        # The earlier one will have a lower stop sequence than the later one

        # For the beginning of the route
        sequences = []
        for stop in start_time:
          sequences.append(stop["stop_sequence"])
        earlier = min(sequences)
        for stop in start_time:
          if stop["stop_sequence"] == earlier:
            start_time = stop["arrival_time"]

        # For the terminus of the route
        sequences = []
        for stop in end_time:
          sequences.append(stop["stop_sequence"])
        later = max(sequences)
        for stop in end_time:
          if stop["stop_sequence"] == later:
            end_time = stop["arrival_time"]

      else:
        # A super loop?
        raise Exception

      # Convert the start_time and end_time strings into seconds to add to DayObj
      begin_seconds_past_midnight = int(start_time[0:2])*60*60 + int(start_time[3:5])*60 + int(start_time[6:8])
      end_seconds_past_midnight = int(end_time[0:2])*60*60 + int(end_time[3:5])*60 + int(end_time[6:8])

      # Check if the same shape has already had its position interpolated!
      # Because if it has, it's only wasting time to re-interpolate the positon over time.
      q = Template('SELECT EXISTS(SELECT 1 FROM intervals WHERE shape_id = "$shape_id")')
      shapeID = self.getShapeID()
      query = q.substitute(shape_id = shapeID)
      self.cur.execute(query)
      if self.cur.fetchone():
        # Then the shape has already been recorded
        # So now we look at the number of stops, and the start and end time to work out if the two trips are the same
        # but just start at different times of the day (e.g. an hourly bus).
        q = Template('SELECT MIN(date), MAX(date), trip_id FROM intervals WHERE shape_id = "$shape_id" GROUP BY trip_id')
        query= q.substitute(shape_id = shapeID)
        self.cur.execute(query)
        rranges = self.cur.fetchall()

        DONOTREWRITE, WRITEANEW = False, True # Assume trip has not been recorded, until shown otherwise
        tripDuration = end_seconds_past_midnight - begin_seconds_past_midnight
        for rrange in rranges:
          recordedDuration = rrange[1] - rrange[0]
          if rrange[2] == self.trip_id:
            # Found a trip has already been recorded.
            # Will occur if being run over the same data more than once.
            # Break
            DONOTREWRITE = True
            break
          elif recordedDuration != tripDuration:
            # Then the trip is new, but the shape is not (e.g. a slower peak service along existing route).
            # However, we need to check all existing cases of this shape before this is confirmed,
            # so there is no break in this branch.
            WRITEANEW = True
          elif recordedDuration == tripDuration:
            # How much after (or even before) is this trip? Need to offset the existing rows by this amount.
            timediff = begin_seconds_past_midnight - rrange[0]
            # Grab the rows to offset then copy back into the table.
            q = Template('SELECT * FROM intervals WHERE trip_id = "$trip_id" ORDER BY date')
            query = q.substitute(trip_id = rrange[2])
            self.cur.execute(query)
            rows = self.cur.fetchall()
            time.sleep(1) # Forces a 1 second wait to stop conflicts

            for row in rows:
              # Copy its rows, just replace the time with the offset time
              offsetTime = row[1] + timediff
              self.cur.execute('INSERT INTO intervals VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (self.trip_id, offsetTime, row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
            self.database.commit()
            WRITEANEW = False
            break

      if WRITEANEW == True and DONOTREWRITE == False:
        # The shape has not yet been recorded in intervals
        # For each <interval> in the trip's duration, add the position of the trip as a (X,Y,) tuple, to a list
        positions = []
        for second in range(begin_seconds_past_midnight, end_seconds_past_midnight+1, interval):
          if second < 86400: # Not at or after midnight
            elapsed = datetime.timedelta(seconds=second)                      # e.g. 24500 seconds
            current_time = (datetime.datetime.min + elapsed).time()           # e.g. 24500 seconds would become
                                                                              # datetime.time(6, 48, 20)=06:48:20.000
            positions.append([second, self.whereIsVehicle(current_time, DayObj)]) # Seconds past midnight, followed by position

        # Once done, if the end time is not divisible by the interval
        # We need to append that special case to ensure the end of the trip is always shown
        # This is important for inferring trip duration from the intervals table
        if end_seconds_past_midnight%interval != 0:
          elapsed = datetime.timedelta(seconds=end_seconds_past_midnight)
          current_time = (datetime.datetime.min + elapsed).time()
          positions.append([end_seconds_past_midnight, self.whereIsVehicle(current_time, DayObj)])

        trip_summary = {"TripID": self.trip_id,
                        "Position": positions,
                        "Modetype": self.getRoute().getMode().modetype,
                        "Operator": self.getAgencyID(),
                        "RouteID": self.getRouteID(),
                        "ShapeID": self.getShapeID()}

        if updateDB == True:
          for position in trip_summary["Position"]:
            if position[0] < 86400:
              # i.e., before midnight, not after it or on it
              # FIXME: Midnight bug in PTTrip.intervalByIntervalPosition
              self.cur.execute('INSERT INTO intervals VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (trip_summary["TripID"], position[0], position[1][0], position[1][1], trip_summary["Modetype"], None, None, trip_summary["Operator"], trip_summary["RouteID"], trip_summary["ShapeID"]))
          self.database.commit()
        return None

    else:
      # The trip does not operate on DayObj, so forget about it.
      # Or it has already been written.
      return None

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
    
  def getShapelyPointProjected(self, source=4326, target=2134):
    '''
    Returns a Shapely point representing the location of the stop,
    projectedd from the <source> GCS to the <target> PCS.
    
    2134 = NZGD2000 / UTM zone 59S (default <target>)
    4326 = WGS84 (default <source>)
    
    Returns a shapely.geometry.point.Point object.
    '''
    to_epsg=target
    from_epsg=source
    
    to_srs = ogr.osr.SpatialReference()
    to_srs.ImportFromEPSG(to_epsg)
    
    from_srs = ogr.osr.SpatialReference()
    from_srs.ImportFromEPSG(from_epsg)
    
    ogr_geom = ogr.CreateGeometryFromWkb(self.getShapelyPoint().wkb)
    ogr_geom.AssignSpatialReference(from_srs)
    
    ogr_geom.TransformTo(to_srs)
    return loads(ogr_geom.ExportToWkb())
    
  def getStopTime(self, TripObj):
    '''
    Returns a dictionary of:
    {"stop_sequence":integer,
    "arrival_time":string,
    "departure_time":string,
    "pickup_type_text":string,
    "drop_off_type_text":string,
    "shape_dist_traveled":float} at the Stop for a given Trip.
    Strings are used for arrival_time and departure_time where
    datetime.time objects would be preferred, because these times can
    exceed 23:59:59.999999, and so cause a value error if instantiated.
    
    TODO: What about trips with the same trip_id that visit the same stop
    more than once?
    '''
    q = Template('SELECT stop_sequence, arrival_time, departure_time, pickup_type_text, drop_off_type_text, shape_dist_traveled FROM stop_times WHERE stop_id = "$stop_id" and trip_id = "$trip_id"')
    query = q.substitute(stop_id = self.stop_id, trip_id = TripObj.trip_id)
    self.cur.execute(query)
    stops = self.cur.fetchall()
    if len(stops) == 1:
      # Then the trip only visits that stop once in its trip
      stop_time = stops[0]
      stop_time = {"stop_sequence":int(stop_time[0]), "arrival_time":stop_time[1], "departure_time":stop_time[2], "pickup_type_text":stop_time[3], "drop_off_type_text":stop_time[4], "shape_dist_traveled":float(stop_time[5])}
      return stop_time
    else:
      # Then the trip makes multiple visits to that stop in its trip
      # e.g. a loop that starts and stops at the same place
      # Such as trips 13, 14 and 15 (N001 Wellington),
      # or a trip that goes over midnight in two consecutive nights.
      # So return a list of stop_times (a list of dictionaries)
      stop_times = []
      for stop_time in stops:
        stop_time = {"stop_sequence":int(stop_time[0]), "arrival_time":stop_time[1], "departure_time":stop_time[2], "pickup_type_text":stop_time[3], "drop_off_type_text":stop_time[4], "shape_dist_traveled":float(stop_time[5])}
        stop_times.append(stop_time)
      return stop_times # A list of dictionaries

  def getStopSnappedToRoute(self, TripObj, projected=True, verbose=False):
    '''
    The Stops listed in the GTFS do not have to intersect the Routes which
    are essentially defined by them. This method returns a Shapely.geometry
    Point object representing the location of the Stop when shifted the
    minimum neccessary distance to intersect the <RouteObj>.
    
    Adapted from:
    http://gis.stackexchange.com/questions/396/nearest-neighbor-between-a-point-layer-and-a-line-layer
    Date: 20140101
    '''
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
      
    if verbose:
      print "Closest point found at: %s, with a distance of %.2f units." % \
       (intersection_point, min_dist)
       
    return stoploc

if __name__ == '__main__':
  ################################################################################
  ########################## Testing Section #####################################
  ################################################################################

  '''
  ## Testing PTTrip.intervalByIntervalPosition -- building the animation database!
  myDatabase = Database(myDB)
  myDay = Day(myDB, datetimeObj=datetime.datetime(2013, 12, 8))

  interval=1 # Temporal resolution, in seconds
  dur() # Initiate timer

  allTrips = myDay.getAllTrips()
  dur('myDay.getAllTrips()') # How long did it take to get all trip objects for myDay?

  endtime = datetime.time(22, 30) # End time for processing
  i = 1

  for trip in allTrips: # For all trips on myDay
    current_time = datetime.datetime.now().time()
    if trip.trip_id >= i and current_time < endtime: # Control start index, and end processing time -- get some sleep!
      dur() # Re-initiate timer, once for each trip
      myDatabase = Database(myDB)
      myDay = Day(myDB, datetimeObj=datetime.datetime(2013, 12, 8))
      trip.intervalByIntervalPosition(myDay, interval=interval)
      process="Trip=%s, i=%i, mode=%s myPTTrip.intervalByIntervalPosition(myDay, interval=%i)" % (trip.trip_id, i, trip.getMode().modetype, interval)
      dur(process) # How long did it take to process the record?
      myDB.commit() # Commit to database
      i += 1 # Next index, in parallel with trip_id

  # When done, play some noise to let me know
  import pygame
  pygame.init()
  pygame.mixer.init()
  sound = pygame.mixer.Sound("test.wav")
  for i in range(0,5):
    sound.play()
    time.sleep(1)
  '''

  '''
  ## Testing Day.plotModeSplit_NVD3
  myDatabase = Database(myDB)
  myDay = Day(myDB, datetimeObj=datetime.datetime(2013, 12, 8))

  myDay.plotModeSplit_NVD3(myDay, "Wellington")
  '''

  '''
  ## Testing Day.animateDay()
  dur()
  myDatabase = Database(myDB)
  myDay = Day(myDB, datetimeObj=datetime.datetime(2013, 12, 8))
  myDay.animateDay(0, 86399)
  dur("myDay.animateDay(0, 86399)")
  '''

  
  ## Trying to fix the placement problem. See the QGIS file
  myDatabase = Database(myDB)
  myTrip = PTTrip(myDB, "16")
  print myTrip.getShapelyLineProjected()
  print ""
  print "stop_id, WKT_point;"
  for stop in myTrip.getStopsInSequence():
    #print stop.getShapelyPointProjected().coords[:],
    print "%s, POINT (%.9f %.9f);" % (stop.stop_id, stop.getStopSnappedToRoute(myTrip, projected=True).x, stop.getStopSnappedToRoute(myTrip, projected=True).y)
      
  #myTrip.cur.execute('SELECT * FROM intervals WHERE trip_id = "16"')
  #print "Seconds, Point;"
  #for i in myTrip.cur.fetchall():
    #print "%i, POINT (%.7f %.7f);" % (i[1], i[2], i[3])
    
  #print ""
  #print myTrip.getShapelyLineProjected()
  #for stop in myTrip.getStopsInSequence():
    #print stop.getShapelyPoint()
  

  '''
  ## Testing bokehFrequencyByMode
  myDatabase = Database(myDB)
  myDay = Day(myDB, datetime.datetime(2013, 12, 8))
  myDay.bokehFrequencyByMode(1*60, Show=True)
  '''
  
  '''
  ## Testing for addressing post-midnight bug with relevant methods
  myDatabase = Database(myDB)
  myDay = Day(myDB, datetime.datetime(2013, 12, 10)) # (2013, 12, 8)
  for T in Route(myDB, "WBAO017O").getTripsInDayOnRoute(myDay): # "WBAO130O", "WRAHVL0I"
    print T.getTripStartTime(myDay), "\t", T.getTripEndTime(myDay), "\t", T.trip_id, "\t", T.getTripDuration(myDay), T.getTripSpeed(myDay)
  print ""
  print ""
  #print myDay.dayOfWeekStr.title(), PTTrip(myDB, "800").getRouteID(), PTTrip(myDB, "800").getTripStartTime(myDay), PTTrip(myDB, "800").getTripEndTime(myDay)
  '''
  
  '''
  myDatabase = Database(myDB)
  myDay = Day(myDB, datetime.datetime(2013, 12, 10)) # (2013, 12, 8)
  myTrip = PTTrip(myDB, 754)
  #print myTrip.getShapelyLineProjected().coords[:]
  for S in myTrip.getStopsInSequence():
    print S.getStopSnappedToRoute(myTrip, projected=False).x, S.getStopSnappedToRoute(myTrip, projected=False).y
  '''
  ################################################################################
  ################################ End ###########################################
  ################################################################################
