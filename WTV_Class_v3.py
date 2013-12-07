#-------------------------------------------------------------------------------
# Name:         WTV_Class_v1.py
# Purpose:      Classes for methods to be called for accessing the TransportViewer.db
#                              
#                       Classes and completed methods:

#                         Database(Object)                    ::A GTFS feed transformed into a SQLite database::
#                           > __init__(database)              ::<database> is a SQLite3 database, constructed by the use of WTV_GTFStoSQL_v*.py::
#                           > getFeedInfo()                   ::Returns cur.fetchall() of the feed_info table::
#                           > feedEndDate()                   ::Returns a datetime object representing the end date of the GTFS feed::
#                           > feedStartDate()                 ::Returns a datetime object representing the start date of the GTFS feed::
#                           > feedDateRange()                 ::Returns a tuple of two datetime objects, representing [0] the start date of the feed and [1] the end date of the feed::
#                           > getAllModes()                   ::Returns a list of Mode objects, one for each type of route_type_desc in the GTFS (routes table)::
#                           > getAgencies()                   ::Returns cur.fetchall() of the agency table::
#                           > getAllTrips(DayObj)             ::Returns a list of PTTrip objects representing those trips that run at least once on <DayObj>::
#                           > getSittingStops(second, DayObj) ::Returns a list of dictionaries which give information about any public transport stops which currently (<second>) have a vehicle sitting at them, on <DayObj>::

#                         Day(Database)                       ::A date. PT runs by daily schedules, considering things like whether it is a weekday, etc::
#                           > __init__(database, datetimeObj) ::<database> is a Database object. <datetimeObj> is a datetime object::
#                           > getCanxServices()               :CAUTION:Returns a list of PTService objects that are cancelled according to the calendar_dates table. For Wellington I suspect this table is a little dodgy::
#                           > getServices()                   :Returns a list of PTService objects that are scheduled to run on the day represented by datetimeObj. Currently set to ignore the information in the calendar_dates table::

#                         Mode(Database)                      ::A vehicle class, like "Bus", "Rail", "Ferry" and "Cable Car"::
#                           > __init__(database, modetype)    ::<database> is a Database object. <modetype> is a string (as above) of the mode of interest::
#                           > getRoutesOfMode                 ::Returns a list of route objects that are of the same mode type as self::
#                           > getRoutesModeInDay(DayObj)      ::Same as Mode.getRoutesModeInDay, but only returns those routes that run on DayObj::
#                           > countRoutesModeInDay(DayObj)    ::A count of the returned values from Mode.getRoutesModeInDay(DayObj)::
#                           > countTripsModeInDay(DayObj)     :INEFFICIENT:A count of the number of discrete trips made on the routes returned from Mode.getRoutesModeInDay(DayObj)::
#                           > getAgencies()                   ::Return a list of Agency objects that have routes of the same <modetype> as Mode::

#                         PTService(Database)                 ::A "service" in GTFS parlance, is used to identify when a service is available for one or more routes, when these are run, and what trips they represent::
#                           > __init__(database, service_id)  ::<service_id> is an Integer. See database::
#                           > getRoutes_PTService()           ::Returns a list of all of the Route objects based on the route_id or route_ids (plural) that the PTService object represents::

#                         Agency(Database)                    ::An Agency is an opertor usually contracted to run one or more routes with vehicles that they own. They are subject to performance measurements and re-tendering, etc::
#                           > __init(Database, agency_id)     ::<database> is a Database object. <agency_id> is a String representing the abbreviation of the agency name::
#                           > getAgencyName()                 ::Returns a string of the full Agency name::
#                           > getRoutes_Agency()              ::Returns a list of the Route objects representing the routes that the agency is contracted to operate on::
#                           > getServices()                   ::Returns a list of the PTService objects representing the services that the agency's routes represent::

#                         Route(Agency)                       ::A Route is a path that a trip takes. It has a shape, including vertices and end points. Each route is operated by a single Agency::
#                           > __init__(database, route_id)    ::<database> is a Database object. <route_id> is a String (e.g. 'WBAO001I' for the incoming Number 1 bus)::
#                           > getAgencyID()                   ::Returns a String of the Agency (agency_id) that operates the route. Used to construct the Agency object that the Route object inherits from.::
#                           > getShortName()                  ::Returns a String of the route_short_name attribute from the routes table representing the name displayed to passengers on bus signage etc., e.g. "130"::
#                           > getLongName()                   ::Returns a String of the route_long_name attribute from the routes table representing the full name of the route::
#                           > getTripsInDay(DayObj)           ::Returns a list of PTTrip objects that run along the entire route. <DayObj> is a Day object:: 
#                           > countTripsInDay(DayObj)         ::Returns an Integer count of the trips that run on the route on <DayObj> (a la Route.getTripsInDay())::
#                           > doesRouteRunOn(DayObj)          ::Returns a Boolean according to whether the Route has a trip on <DayObj>::
#                           > inboundOrOutbound()             ::Returns Strings "Incoming" or "Outgoing" according to whether the Route is such::
#                           > getMode()                       ::Returns the mode of the route, as a Mode object::

#                         PTTrip(Route)                       ::A PTTrip is a discrete trip made by single mode along a single route::
#                           > __init__(database, trip_id)     ::<database> is a Database object. <trip_id> is an Integer identifying the trip uniquely. See the database::
#                           > getRouteID()                    ::Returns the route_id (String) of the route that the trip follows. Used to construct the Route object which the Trip object inherits.
#                           > getRoute()                      ::Returns the Route object representing the route taken on Trip::
#                           > getService()                    ::Returns the PTService object that includes this trip::
#                           > getShapelyLine()                ::Returns a Shapely Line object representing the shape of the trip::
#                           > plotShapelyLine()               ::Uses matplotlib and Shapely to plot the shape of the trip. Does not plot stops (yet?)::
#                           > getStopsInSequence()            ::Returns a list of the stops (as Stop ibjects) that the trip uses, in sequence::
#                           > animateTrip()                   :Needs improvement:Uses maptplotlib.animate and self.getShapelyLine() to animate the drawing of a trip's route. Does not account for stops (yet?)::
#                           > whereIsVehicle(second, DayObj)  ::Returns a tuple (x, y) or (lon, lat) of the location of the vehicle at a given moment in time, <second>. <second> is a datetime.time object. <DayObj> is a Day object::
#                           > intervalByIntervalPosition(DayObj, interval=1) ::::

#                         Stop(Object)                        ::A place where PT vehicles stop within a route::
#                           > __init__(database, stop_id)     ::<database> is a Database object. <stop_id> is an Integer identifying the trip uniquely, able to link it to stop_times. See the database::
#                           > getStopCode()                   ::Returns the stop_code, a short(er) integer version similar to stop_id, but published on signs and used in passenger text alerts::
#                           > getStopName()                   ::Returns the stop_name, a long name of the stop (String)::
#                           > getStopDesc()                   ::Returns the stop_desc, a short but textual name for the stop::
#                           > getLocationType()               ::Returns location_type_desc from the stops table: ["Stop", "Station", "Hail and Ride"]. For Metlink: ["Stop", "Hail and Ride"]::
#                           > getShapelyPoint()               ::Returns a shapely Point object representing the location of the stop::
#                           > getStopTime(TripObj)            ::Returns a dictionary of {"stop_sequence":integer, "arrival_time":string, "departure_time":string, "pickup_type_text":string, "drop_off_type_text":string, "shape_dist_traveled":float} at the Stop for a given Trip. Strings are used for arrival_time and departure_time where datetime.time objects would be preferred, because these times can exceed 23:59:59.999999, and so cause a value error if instantiated::


# Tasks for next iteration/s:
#                > [COMPLETE] Comment existing code thoroughly and ensure that class structure is logical, abstract and modular.
#                > KEEP CODE DOCUMENTED THROUGHOUT
#                > Database method: return all stop objects
#                > Work out how Git works and start using it for version control.
#                > Continue building class structure and start working on some interesting statistical presentations.
#                > Install Python-nvd3 at home
#                > Develop methods for using Py-nvd3 within existing class structure
#                > Develop the HTML and CSS for the website and embed the JavaScript graphs
#                > Work on the visualisation of the network in real time (based on that guy...)
#                > Work on the server//Django side of things to get an actual website!
#                > Have the first version of the website up and running (one city)!
#                > Expand to multiple cities
#                > Consider how fare information can be added
#                
#
# Author:        Richard Law.
#
# Inputs:        Database written by WTV_GTFStoSQL_v*.py
#
#
# Created:            20131107
# Last Updated:       20131108
# Comments Updated:   20131110
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
import numpy as np

from shapely.geometry import Point, LineString

import sqlite3 as dbapi
#db_str = "GTFSSQL_Wellington_20131112_144855.db" # Name of database
db_str = "GTFSSQL_Wellington_20131207_212134__SUBSET__.db"
#db_pathstr = "G:\\Documents\\WellingtonTransportViewer\\Data\\Databases\\" + db_str # Path and name of DB, change to necessary filepath
db_pathstr = "/media/alphabeta/RESQUILLEUR/Documents/WellingtonTransportViewer/Data/Databases/" + db_str # Path and name of DB, change to necessary filepath
myDB = dbapi.connect(db_pathstr) # Connect to DB
myDB.text_factory = dbapi.OptimizedUnicode

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
        return False
      else:
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

  def getAllTrips(self, dayObj):
    '''
    Given a particular <DayObj>, returns a list of PTTrip objects that run on that day.
    '''
    self.cur.execute('SELECT DISTINCT trip_id FROM trips')

    trips = []
    for trip in self.cur.fetchall():
      pttrip = PTTrip(self.database, trip[0])
      if pttrip.doesRouteRunOn:
        trips.append(pttrip)
    return trips
  
  def getSittingStops(self, second, dayObj):
    '''
    Given a particular <second> (hh:mm:ss) in a <dayObj>, returns a list of the XY positions of any
    public transport stops that any vehicle is currently sitting at.
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

    sittingstops = []
    q = Template('SELECT S.stop_lat, S.stop_lon, ST.trip_id, ST.stop_id, ST.pickup_type_text, ST.drop_off_type_text FROM stop_times AS ST JOIN stops AS S ON ST. stop_id = S.stop_id WHERE arrival_time = "$second" OR departure_time = "$second" OR (arrival_time  < "$second" AND departure_time > "$second")')
    query = q.substitute(second = hour + ":" + mins + ":" + secs + "." + ssecs)
    self.cur.execute(query)
    for sittingstop in self.cur.fetchall():
      if PTTrip(self.database, str(sittingstop[2])).doesRouteRunOn(dayObj): # If the route actually runs on the day 
        sittingstop = {"stop_lat":sittingstop[0], "stop_lon":sittingstop[1], "trip_id":sittingstop[2], "stop_id":sittingstop[3], "pickup_type_text":sittingstop[4], "drop_off_type_text":sittingstop[5]}
        sittingstops.append(sittingstop)
    return sittingstops

  def animateSystem(self, DayObj, starttime=datetime.time(8), endtime=datetime.time(8, 1), interval=60):
    '''
    Displays (and can save) a video of the entire PT system, at intervals of <interval> (in seconds).
    Use interval=1 for best results, as scheduled stops are recorded to the nearest second.
    By default, visualises the system between 8am and 9am.

    Uses matplotlib, matplotlib.basemap, and matplotlib.animate.

    ATM: IT'S FUCKED
    '''
    alltrips = self.getAllTrips(DayObj)
    def xylims():
      '''
      Gets the X and Y limits of the graph,
      defined as the max/min XY of all trips on the day.
      '''
      minx, miny, maxx, maxy = None, None, None, None
      for trip in alltrips:
        bounds = trip.getShapelyLine().bounds # (minx, miny, maxx, maxy)
        if bounds[0] < minx or minx is None:
          minx = bounds[0]
        if bounds[1] < miny or miny is None:
          miny = bounds[1]
        if bounds[2] > maxx or maxx is None:
          maxx = bounds[2]
        if bounds[3] > maxy or maxy is None:
          maxy = bounds[3]
      return (minx, miny, maxx, maxy)

    import numpy as np
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    stopx, stopy, vehiclex, vehicley = [], [], [], []

    # range = seconds between start and endtimes
    for t in range(0, 10):
      if t == 0:
        points, = ax.plot(stopx, stopy, marker='.', linestyle='None')
        points2, = ax.plot(vehiclex, vehicley, marker='o', color='r', linestyle='None')

        ## (minx, miny, maxx, maxy)
        ##bounds = xylims()
        ##bounds = (174.7212282, -41.34865225, 175.6846043, -38.84426454)
        bounds = (174.7212282, -41.34865225, 175, -41.0)
        ax.set_xlim(bounds[0], bounds[2])
        ax.set_ylim(bounds[1], bounds[3])

      else:
        currenttime = (datetime.datetime.combine(DayObj.datetimeObj, starttime) + datetime.timedelta(seconds=interval*(t-1)))
        #currentTime = starttime + datetime.timedelta(seconds=interval)
        # while starttime < endtime

        for stop in self.getSittingStops(datetime.time(currenttime.hour, currenttime.minute, currenttime.second, currenttime.microsecond), DayObj):
          stopx.append(stop['stop_lon'])
          stopy.append(stop['stop_lat'])
        new_x = np.array(stopx)
        new_y = np.array(stopy)

        i = 0
        for trip in alltrips:
          if i > 10:
            break
          if trip.doesRouteRunOn(DayObj):
            position = trip.whereIsVehicle((datetime.time(currenttime.hour, currenttime.minute, currenttime.second, currenttime.microsecond)), DayObj)
            if position is not None:
              vehiclex.append(position[0])
              vehicley.append(position[1])
              i += 1
        new_vehiclex = np.array(vehiclex)
        new_vehicley = np.array(vehicley)

        points.set_data(new_x, new_y)
        points2.set_data(new_vehiclex, new_vehicley)

        stopx, stopy, vehiclex, vehicley = [], [], [], []

        print currenttime, t, points
      plt.pause(0.01)

class Day(Database):
  '''
  A date. PT runs by daily schedules, considering things like whether it is a weekday, etc.
  Today is gonna be a good day!
  '''
  def __init__(self, database, datetimeObj):
    '''
    <database> is a Database object.
    <datetimeObj> is a datetime object.
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

  def getServices(self):
    '''
    Returns a list of PTService objects representing services that are running on self.day.
    Takes into account the day of the week, and the cancelled services on Day.**

    **No longer takes into account "cancelled" services, due to the unreliability of this information.
    The code that achieved this has been commented out within the function, rather than removed.
    '''
    # Fill template, including use of today's day of the week.

    # Old template, uses CD.date <> "$today2", which seemed to give wrong answer
    ##q = Template('SELECT DISTINCT C.service_id FROM calendar AS C LEFT OUTER JOIN calendar_dates AS CD ON CD.service_id = C.service_id WHERE C.start_Date <= "$today1" AND C.end_date >= "$tomorrow" AND C.$DayOfWeek = 1 AND CD.date <> "$today2"')
    ##query = q.substitute(today1 = self.isoDate[0:10], tomorrow = self.tomorrow[0:10], DayOfWeek = self.dayOfWeekStr, today2 = self.isoDate[0:10])

    # New template
    q = Template('SELECT DISTINCT C.service_id FROM calendar AS C LEFT OUTER JOIN calendar_dates AS CD ON CD.service_id = C.service_id WHERE C.start_Date <= "$today1" AND C.end_date >= "$tomorrow" AND C.$DayOfWeek = 1')
    query = q.substitute(today1 = self.isoDate[0:10], tomorrow = self.tomorrow[0:10], DayOfWeek = self.dayOfWeekStr)    
    self.cur.execute(query)

    # Data structure to return
    gotServices = []
    services = self.cur.fetchall()
    for service in services:
      gotServices.append(str(service[0]))
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

  def getRoutesModeInDay(self, DayObj):
    '''
    Same as Mode.getRoutesModeInDay, but only returns those Route objecys that run on DayObj.
    Has its own query.
    '''
    # Get service_id of services that are running on DayObj
    services = DayObj.getServices()

    # Distinct route/service pairs of the same modetype as self.Mode.
    q = Template('SELECT DISTINCT T.route_id, T.service_id FROM trips AS T JOIN routes AS R ON T.route_id = R.route_id WHERE R.route_type_desc = "$modetype"')
    query = q.substitute(modetype = self.modetype)
    self.cur.execute(query)

    # Append to set if the service runs on DayObj
    RoutesModeInDay = set()
    for tripservice in self.cur.fetchall():
      route_id = tripservice[0]
      service_id = tripservice[1]
      if str(service_id) in services:
        RoutesModeInDay.add(Route(self.database, route_id))

    return RoutesModeInDay # Route objects

  def countRoutesModeInDay(self, DayObj):
    '''
    Returns an integer representing the count of the returned values from Mode.getRoutesModeInDay(DayObj).
    '''
    return len(self.getRoutesModeInDay(DayObj))

  def countTripsModeInDay(self, DayObj):
    '''
    Like countRoutesModeInDay, but counts trips made, not routes.
    Unfinished.
    '''
    count = 0
    # Could be more efficient with a dedicated query.
    for route in self.getRoutesModeInDay(DayObj):
      count += route.countTripsInDay(DayObj)
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

  def getTripsInDay(self, DayObj):
    '''
    Given a Day object, this method returns all of the trips of this route on that Day, as a list of PTTrip objects.
    '''
    q = Template('SELECT DISTINCT T.trip_id FROM routes AS R JOIN trips AS T ON R.route_id = T.route_id JOIN calendar AS C ON T.service_id = C.service_id WHERE R.route_id ="$route_id" AND C.start_Date <= "$today" AND C.end_date >= "$nextday" AND C.$dayText = 1')
    query = q.substitute(route_id = self.route_id, today = DayObj.isoDate[0:10], nextday = DayObj.isoDate[0:10], dayText = DayObj.dayOfWeekStr)

    tripsInDay = []
    for trip_id in self.cur.execute(query):
      tripsInDay.append(PTTrip(self.database, trip_id[0]))
    return tripsInDay

  def countTripsInDay(self, DayObj):
    '''
    Given a Day object, <DayObj>, this method returns an Integer count of all the trips of this route on that Day.
    '''
    q = Template('SELECT COUNT (DISTINCT T.trip_id) FROM routes AS R JOIN trips AS T ON R.route_id = T.route_id JOIN calendar AS C ON T.service_id = C.service_id WHERE R.route_id ="$route_id" AND C.start_date <= "$day" AND C.end_date >= "$nextday" AND C.$dayText = 1')
    query = q.substitute(route_id = self.route_id, day = DayObj.isoDate[0:10], nextday = DayObj.tomorrow[0:10], dayText = DayObj.dayOfWeekStr)
    self.cur.execute(query)
    return self.cur.fetchall()[0][0]

  def doesRouteRunOn(self, DayObj):
    '''
    Returns a Boolean variable (True or False) according to whether the Route has a trip on <DayObj>.
    '''
    if self.countTripsInDay(DayObj) > 0:
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

  def getShapelyLine(self):
    '''
    Returns a Shapely Line object representing the trip.
    '''
    q = Template('SELECT shape_pt_lon, shape_pt_lat FROM shapes WHERE shape_id = "$shape_id" ORDER BY shape_pt_sequence')
    query = q.substitute(shape_id = self.getShapeID())
    self.cur.execute(query)

    vertices = []
    for vertex in self.cur.fetchall():
      vertices.append(vertex)

    line = LineString(vertices)

    return line

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

  def getStopsInSequence(self):
    '''
    Returns a list of stop objects that the trip uses, in sequence.
    '''
    q = Template('SELECT stop_id FROM stop_times WHERE trip_id = "$trip_id" ORDER BY stop_sequence')
    query = q.substitute(trip_id = self.trip_id)
    self.cur.execute(query)

    stops = []
    for stop_time in self.cur.fetchall():
      stops.append(Stop(self.database, stop_time[0]))
    return stops

  def whereIsVehicle(self, second, DayObj):
    '''
    Returns an XY position of the vehicle at a given moment in time (<second>) on <dayObj>.
    If the trip does not run, is yet to run, or has already run, it returns None.
    Vehicle locations are "known" at scheduled arrivals, otherwise position is interpolated along their shape.

    <second> is a datetime.time object.

    Returns a (lon, lat) tuple.
    '''
    try:
      # First, check if the trip even operates on <DayObj>
      if self.doesRouteRunOn(DayObj):

        # Get all the stops that the trip visits
        q = Template('SELECT ST.*, S.stop_lat, S.stop_lon FROM stop_times AS ST JOIN stops AS S ON S.stop_id = ST.stop_id WHERE trip_id = $trip_id ORDER BY stop_sequence')
        query = q.substitute(trip_id = self.trip_id)
        self.cur.execute(query)
        stop_times = self.cur.fetchall()

        # Check if the trip is even operating at <second>
        overall_start = datetime.time(int(stop_times[0][1][0:2]), int(stop_times[0][1][3:5]), int(stop_times[0][1][6:8]), int(stop_times[0][1][9:12]))
        overall_end = datetime.time(int(stop_times[-1][2][0:2]), int(stop_times[-1][2][3:5]), int(stop_times[-1][2][6:8]), int(stop_times[-1][2][9:12]))
        if second >= overall_start and second <= overall_end:
          # Then the trip is operating at <second>
          # Now, refine the precise position using scheduled times.

          i = 0 # index the stop searching so we can query the next stop in the sequence
          for stop in stop_times:
            arrival1 = datetime.time(int(stop[1][0:2]), int(stop[1][3:5]), int(stop[1][6:8]), int(stop[1][9:12]))
            departure1 = datetime.time(int(stop[2][0:2]), int(stop[2][3:5]), int(stop[2][6:8]), int(stop[2][9:12]))
            if second >= arrival1 and second <= departure1:
              # If the trip dwells at the stop and second is within the dwell time range,
              # Return the X, Y of the current stop because we have found the vehicle.
              return (stop[12], stop[11]) # lon, lat
            arrival2 = datetime.time(int(stop_times[i+1][1][0:2]), int(stop_times[i+1][1][3:5]), int(stop_times[i+1][1][6:8]), int(stop_times[i+1][1][9:12]))
            departure2 = datetime.time(int(stop_times[i+1][2][0:2]), int(stop_times[i+1][2][3:5]), int(stop_times[i+1][2][6:8]), int(stop_times[i+1][2][9:12]))
            if second >= arrival2 and second <= departure2:
              # If the trip dwells at the next stop and second is within the dweel time range,
              # Return the X, Y of the next stop because we have found the vehicle.
              return (stop_times[i+1][12], stop_times[i+1][11]) # lon, lat
            if second > departure1 and second < arrival2:
              # If the vehicle is after the first stop but has not yet arrived at the second stop,
              # Then the vehicle is between the two stops,
              # And the task is to infer its location based on distance and time.

              # How many seconds ahead of the departure from stop 1 is <second>?
              secondsahead = datetime.datetime.combine(myDay.datetimeObj, second) - datetime.datetime.combine(myDay.datetimeObj, departure1)
              secondsahead = float(secondsahead.seconds)

              # How many seconds does it take for the vehicle to travel from stop 1 to stop 2?
              timeDelta = datetime.datetime.combine(myDay.datetimeObj, arrival2) - datetime.datetime.combine(myDay.datetimeObj, arrival1) # Computes time difference
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
              interpolatedPosition = routeShape.interpolate(proportionTravelled * self.getShapelyLine().length)
              return (interpolatedPosition.x, interpolatedPosition.y) # lon, lat

            i += 1
            # If the vehicle is not at or between 1 or 2, then the for loop proceeds to consider stops 2 and 3, until a 
            # solution is found.

      else:
        return None

    except ValueError:
      # If ValueError, the time is beyond 24:00:000...
      # Address this later.
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
    
    NEW: Writes to the database, rather than returning the values in memory.
    '''
    if self.doesRouteRunOn(DayObj) == True:
      # Infer the time range of the trip
      stops = self.getStopsInSequence()
      start_time, end_time = stops[0], stops[-1]
      start_time, end_time = start_time.getStopTime(self), end_time.getStopTime(self)
      start_time, end_time = start_time["arrival_time"], end_time["arrival_time"]
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
        print begin_seconds_past_midnight, end_seconds_past_midnight
        q = Template('SELECT MIN(date), MAX(date), trip_id FROM intervals WHERE shape_id = "$shape_id" GROUP BY trip_id')
        query= q.substitute(shape_id = shapeID)
        self.cur.execute(query)
        
        DONOTREWRITE, WRITEANEW = False, False # Assume trip has not been recorded, until shown otherwise
        tripDuration = end_seconds_past_midnight - begin_seconds_past_midnight
        for rrange in self.cur.fetchall():
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
            # Then the shape has been seen already, going at the same speed.
            # So we can COPY ITS ROWS.
            # We need to get each of its rows, and simply replace each of the time past midnights with new ones.
            # Commit this to the database
            # Then WRITEANEW = False
            # Then Break
            ## some code! TO DO NEXT
            break
        
      if WRITEANEW == True and DONOTREWRITE == False:
        # The shape has not yet been recorded in intervals
        # For each <interval> in the trip's duration, add the position of the trip as a (X,Y,) tuple, to a list
        positions = []
        for second in range(begin_seconds_past_midnight, end_seconds_past_midnight+1, interval):
          print second
          elapsed = datetime.timedelta(seconds=second)                      # e.g. 24500 seconds
          current_time = (datetime.datetime.min + elapsed).time()           # e.g. 24500 seconds would become
                                                                            # datetime.time(6, 48, 20)=06:48:20.000
          positions.append([second, self.whereIsVehicle(current_time, DayObj)]) # Seconds past midnight, followed by position
        trip_summary = {"TripID": self.trip_id,
                        "Position": positions,
                        "Modetype": self.getRoute().getMode().modetype,
                        "Operator": self.getAgencyID(),
                        "RouteID": self.getRouteID(),
                        "ShapeID": self.getShapeID()}
        
        if updateDB == True:
          for position in trip_summary["Position"]:
            self.cur.execute('INSERT INTO intervals VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (trip_summary["TripID"], position[0], position[1][0], position[1][1], trip_summary["Modetype"], None, None, trip_summary["Operator"], trip_summary["RouteID"], trip_summary["ShapeID"]))
          self.database.commit()
          
        return trip_summary
      
    else:
      # The trip does not operate on DayObj, so forget about it.
      # Or it has already been written.
      return None

  def animateTrip(self, save=False):
    '''
    Uses matplotlib.animate to animate the route a trip takes.
    Needs improvement: at the moment the 'speed' is simply determined by the density of vertices, and nothing else.
    '''
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation

    def update_line(num, data, line):
      '''
      Function that makes the animation happen.
      This is called sequentially, acccording to num
      '''
      line.set_data(data[...,num-1:num])
      # [...,:num]=everything, revealed in sequence 
      # [...,num-1:num]=only the most recent segment, nothing else is shown in each frame

      time_text.set_text("Frame="+str(num))

      # Returns the line object, which is important because this tells the animator
      # which object on the plit to update after each frame.
      # Note that it is returning a tuple of the plot ojects which have been modified
      # (added, in this case), and are therefore animated.
      return line, time_text,

    fig1 = plt.figure() # Create a figure window
    ax = fig1.add_subplot(111, aspect='equal', autoscale_on=True)
    # Text to be updated with the animation
    time_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)

    # Get the x,y data in two parallel lists, and place them in a numpy array
    x, y = [],[]
    for vertex in list(self.getShapelyLine().coords):
      x.append(vertex[0])
      y.append(vertex[1])
    data = np.array([x, y])

    # A line object that will be modified in the animation
    # It first plots an empty line: data is added later
    l, = plt.plot([], [], 'r.') # Color=r, line style=-

    time_text.set_text('')

    plt.xlim(min(data[0])-0.01, max(data[0])+0.01)
    plt.ylim(min(data[1]-0.01), max(data[1])+0.01)
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    plt.title('Test: Naenae-Petone 130 Bus Animation')

    # The line object needs to persist, so it is assigned to a variable, line_ani
    # interval: N miliseconds delay between frames
    # blit: tells the animation to only re-draw the pieces of the plot that have changed...
      # which saves a lot of time and makes the animation display much more quickly.
    line_ani = animation.FuncAnimation(fig1, update_line, len(x), fargs=(data, l),
                                       interval=20, blit=False)
    # For some reason blit=True keeps a zero underneath the text...

    if save == True:
      line_ani.save('test130bus.mp4')

    return plt.show()    

class Stop(Database):
  '''
  A stop is a place where a PT vehicle stops and passengers may board or depart. Routes are essentially comprised of an ordered sequence of Stops.
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
    lat, lon = loc[0], loc[1]
    return Point(lon, lat) # Shapely Point object... try Point.x, Point.y, etc.

  def getStopTime(self, TripObj):
    '''
    Returns a dictionary of {"stop_sequence":integer, "arrival_time":string, "departure_time":string, "pickup_type_text":string, "drop_off_type_text":string, "shape_dist_traveled":float} at the Stop for a given Trip
    Strings are used for arrival_time and departure_time where datetime.time objects would be preferred, because these times can exceed 23:59:59.999999, and so cause a value error if instantiated.
    '''
    q = Template('SELECT stop_sequence, arrival_time, departure_time, pickup_type_text, drop_off_type_text, shape_dist_traveled FROM stop_times WHERE stop_id = "$stop_id" and trip_id = "$trip_id"')
    query = q.substitute(stop_id = self.stop_id, trip_id = TripObj.trip_id)
    self.cur.execute(query)
    stop_time = self.cur.fetchall()[0]
    stop_time = {"stop_sequence":int(stop_time[0]), "arrival_time":stop_time[1], "departure_time":stop_time[2], "pickup_type_text":stop_time[3], "drop_off_type_text":stop_time[4], "shape_dist_traveled":float(stop_time[5])}
    return stop_time

################################################################################
########################## Testing Section #####################################
################################################################################

## Testing PTTrip.SecondBySecondPosition
myDatabase = Database(myDB)
print myDatabase.checkTableEmpty()
myDay = Day(myDB, datetimeObj=datetime.datetime(2013, 12, 3))
myPTTrip = PTTrip(myDB, trip_id=601) # 4650=A 130 bus # 6434=A HVL train
print myPTTrip.doesRouteRunOn(myDay)

dur()
summary = myPTTrip.intervalByIntervalPosition(myDay, interval=90)
dur('myPTTrip.intervalByIntervalPosition(myDay, interval=90)')

################################################################################
################################ End ###########################################
################################################################################