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

#                         PTTrip(Route)                       ::A PTTrip is a discrete trip made by single mode along a single route::
#                           > __init__(database, trip_id)     ::<database> is a Database object. <trip_id> is an Integer identifying the trip uniquely. See the database::
#                           > getRouteID()                    ::Returns the route_id (String) of the route that the trip follows. Used to construct the Route object which the Trip object inherits.
#                           > getRoute()                      ::Returns the Route object representing the route taken on Trip::
#                           > getService()                    ::Returns the PTService object that includes this trip::
#                           > getShapelyLine()                ::Returns a Shapely Line object representing the shape of the trip::
#                           > plotShapelyLine()               ::Uses matplotlib and Shapely to plot the shape of the trip. Does not plot stops (yet?)::
#                           > getStopsInSequence()            ::Returns a list of the stops (as Stop ibjects) that the trip uses, in sequence::
#                           > animateTrip()                   :Needs improvement:Uses maptplotlib.animate and self.getShapelyLine() to animate the drawing of a trip's route. Does not account for stops (yet?)::

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
from string import Template
import datetime

from shapely.geometry import Point, LineString

import sqlite3 as dbapi
db_str = "GTFSSQL_Wellington_20131112_144855.db" # Name of database
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
    return self.cur.fetchall()[0][0]
  
  def getShapelyLine(self):
    '''
    Returns a Shapely Line object representing the trip.
    '''
    try:
      shape_id = self.getShapeID().replace('\n','') # Metlink includes line breaks
    except:
      shape_id = self.getShapeID()
    q = Template('SELECT shape_pt_lon, shape_pt_lat FROM shapes WHERE shape_id = "$shape_id" ORDER BY shape_pt_sequence')
    query = q.substitute(shape_id = shape_id)
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

# Testing Objects
myDatabase = Database(myDB)
myDay = Day(myDB, datetimeObj=datetime.datetime(2013, 11, 17))
myPTService = PTService(myDB, service_id=1)
myPTTrip = PTTrip(myDB, trip_id=4650) # 4650=A 130 bus # 6434=A HVL train
##myRoute = Route(myDB, route_id="WBBO047O") # Not working correctly, because this service only runs during trimester times.
##myRoute = Route(myDB, route_id="WBBO300O") # Not working correctly, because this service only runs on the last Sunday of each month, but this says it runs once each Sunday.
myRoute = Route(myDB, route_id="WBAO023O")
myMode = Mode(myDB, "Bus")
myAgency = Agency(myDB, "RAIL")
myStop = Stop(myDB, 10619) # Petone Station Stop B (A = 22118; Train station (PETO) = 11709; Petone Wharf = 22940)

'''
# Examples of each object, and a sample method.
print "myDay: cancelled services: ", myDay.getCanxServices()
print "myPTService: routes: ", myPTService.getRoutes_PTService()
print "myPTTrip: Agency name: ", myPTTrip.getAgencyName()
print "myDatabase: Agencies: ", myDatabase.getAgencies()
print "myRoute: Trips in myDay: ", myRoute.getTripsInDay(myDay)
print "myRoute: Count of Trips in myDay: ", myRoute.countTripsInDay(myDay)
print "myRoute: Agency ID: ", myRoute.getAgencyID()
print "myMode: count of the trips of this mode in myDay: ", myMode.countTripsModeInDay(myDay)
print "myAgency: Agency name: ", myAgency.getAgencyName()
for route in myAgency.getRoutes_Agency():
  print myAgency.getAgencyName() + " runs " + route.getShortName() + " " + route.inboundOrOutbound() + " (" + str(route.countTripsInDay(myDay)) + " trips on myDay) " + route.getLongName()
print "myMode: Agency objects with the same mode: ", myMode.getAgencies()
print "myAgency: Service objects that the Agency participates  in: ", myAgency.getServices()
print "myStop: stop_id, stop_code: ", myStop.stop_id, myStop.getStopCode(), myStop.getStopName(), myStop.getStopDesc(), myStop.getLocationType(), myStop.getShapelyPoint().wkt
print len(myPTTrip.getShapelyLine().coords)

myPTTrip.plotShapelyLine()
for i in myPTTrip.getStopsInSequence():
  print i.getStopTime(myPTTrip)["arrival_time"], i.getStopName()
  

# For each day in November 2013, reports how many routes are in operation, broken down by mode.
for i in range(1, 30):
  myDay = Day(myDB, datetimeObj=datetime.datetime(2013, 11, i))
  for mode in myDatabase.getAllModes():
    if mode.modetype == "Cable Car":
      print "%s\t%s\t%s" % (mode.modetype, myDay.dayOfWeekStr.title(), mode.countRoutesModeInDay(myDay))
    else:
      print "%s\t\t%s\t%s" % (mode.modetype, myDay.dayOfWeekStr.title(), mode.countRoutesModeInDay(myDay))
  print ""
'''
'''
myDay.plotModeSplit_NVD3(myDatabase, "Greater Wellington")
print "finished"
'''

# Animate with matplotlib
myPTTrip.animateTrip()

################################################################################
################################ End ###########################################
################################################################################