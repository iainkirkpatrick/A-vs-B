#-------------------------------------------------------------------------------
# Name:             WTV_GTFStoSQL_v1.py
# Purpose:          A series of idiosyncratic functions for building GTSFtoSQL.db from raw GTFS agency feeds, on a per-agency basis.
# Data source:      http://www.gtfs-data-exchange.com
# Type of database: SQLite3
#
# Tables in the database, and their columns and data types:
#
# agency
## agency_id TEXT
## agency_name TEXT
## agency_url TEXT
## agency_timezone TEXT
## agency_lang TEXT
## agency_phone TEXT
## continent TEXT
## country TEXT
## city TEXT
## PRIMARY KEY(agency_id, city) ON CONFLICT IGNORE)
#
# calendar
## service_id INTEGER REFERENCES trips(service_id)
## monday INTEGER
## tuesday INTEGER
## wednesday INTEGER
## thursday INTEGER
## friday INTEGER
## saturday INTEGER
## sunday INTEGER
## start_date DATETIME
## end_date DATETIME
#
# calendar_dates
## service_id INTEGER REFERENCES trips(service_id)
## date DATETIME
## exception_type INTEGER
## exception_text TEXT
#
# feed_info
## feed_publisher_name TEXT
## feed_publisher_url TEXT
## feed_lang TEXT
## feed_start_date DATETIME
## feed_end_date DATETIME
## feed_version TEXT
#
# routes
## route_id TEXT
## agency_id TEXT REFERENCES agency(agency_id)
## route_short_name TEXT
## route_long_name TEXT
## route_desc TEXT
## route_type INTEGER
## route_type_desc TEXT
## route_url TEXT
## route_color TEXT
## text_color TEXT
#
#shapes
## shape_id TEXT
## shape_pt_lat FLOAT
## shape_pt_lon FLOAT
## shape_pt_sequence INTEGER
## shape_dist_traveled INTEGER
#
#stop_times
## trip_id INTEGER REFERENCES trips(trip_id)
## arrival_time DATETIME
## departure_time DATETIME
## stop_id INTEGER REFERENCES stops(stop_id)
## stop_sequence INTEGER
## stop_headsign TEXT
## pickup_type INTEGER
## pickup_type_text TEXT
## drop_off_type INTEGER
## drop_off_type_text TEXT
## shape_dist_traveled FLOAT

#stop_times_amended
## trip_id INTEGER REFERENCES trips(trip_id)
## arrival_time DATETIME
## departure_time DATETIME
## monday INTEGER
## tuesday INTEGER
## wednesday INTEGER
## thursday INTEGER
## friday INTEGER
## saturday INTEGER
## sunday INTEGER
## stop_id INTEGER REFERENCES stops(stop_id)
## stop_sequence INTEGER
## stop_headsign TEXT
## pickup_type INTEGER
## pickup_type_text TEXT
## drop_off_type INTEGER
## drop_off_type_text TEXT
## shape_dist_traveled FLOAT

# stops
## stop_id INTEGER
## stop_code INTEGER
## stop_name TEXT
## stop_desc TEXT
## stop_lat FLOAT
## stop_lon FLOAT#stop_times_amended
## trip_id INTEGER REFERENCES trips(trip_id)
## arrival_time DATETIME
## departure_time DATETIME
## monday INTEGER
## tuesday INTEGER
## wednesday INTEGER
## thursday INTEGER
## friday INTEGER
## saturday INTEGER
## sunday INTEGER
## stop_id INTEGER REFERENCES stops(stop_id)
## stop_sequence INTEGER
## stop_headsign TEXT
## pickup_type INTEGER
## pickup_type_text TEXT
## drop_off_type INTEGER
## drop_off_type_text TEXT
## shape_dist_traveled FLOAT
## zone_id TEXT
## stop_url TEXT
## location_type INTEGER
## location_type_text TEXT
## parent_station INTEGER
## stop_timezone TEXT
## wheelchair_boarding INTEGER
## wheelchair_boarding_text TEXT

#
# trips
## route_id TEXT REFERENCES routes
## service_id INTEGER
## trip_id INTEGER
## trip_headsign TEXT
## trip_short_name TEXT
## direction_id INTEGER
## direction_id_text TEXT
## block_id INTEGER
## shape_id TEXT REFERENCES shapes(shape_id)
## wheelchair_accessible INTEGER
## wheelchair_accessible_text TEXT

#
# intervals
## trip_id INTEGER REFERENCES trips(trip_id)
## date DATETIME
## lat FLOAT
## lon FLOAT
## route_type_desc TEXT REFERENCES routes(route_type_desc)
## pickup_type_text TEXT REFERENCES stop_times(pickup_type_text)
## drop_off_type_text TEXT REFERENCES stop_times(drop_off_type_text)
## agency_id TEXT REFERENCES agency(agency_id)
## route_id TEXT REFERENCES routes(route_id)
## shape_id TEXT REFERENCES shapes(shape_id)

#
# Author:        Richard Law.
#
# Inputs:        Folders of .txt files downloaded from http://www.gtfs-data-exchange.com/agencies.
#
# Created:            20131104
# Last Updated:       20131207
# Comments Updated:   20131207
#-------------------------------------------------------------------------------

################################################################################
############################### Notes ##########################################
################################################################################

"""
There is NO NEED to run this script if you possess the most recent version of the database file that this produces.

Strings are stored as unicode, so 'tricky' characters in the CSV (as in the o-circumflex in Co^te d'Ivoire) are print-ed with the appropriate non-English characters, if this is appropriate at any point.
"""

################################################################################
############################# Functions ########################################
################################################################################
def createGTSFtoSQL_database(DBName_str):
  '''
  Creates a SQLite3 database from the standard GTFS .txt files.
  This function simply creates empty tables that other functions will populate.
  If any changes need to be made to the structure of the database (including its relationships and primary keys), they need to be made here.
  <DBName_str> (string) the path and desired name of the database to be created. An error will be raised if this already exists, so either delete it when running again, or change the name.
  Suggestion: name the database with the suffix of the current time.

  Author: Richard Law
  Created: 20131104
  Edited: 20131207
  '''
  GTFSDB = dbapi.connect(DBName_str) # Connect/create DB
  cur = GTFSDB.cursor() # Create cursor in DB
  GTFSDB.text_factory = dbapi.OptimizedUnicode

  # Add an agency table
  cur.execute('CREATE TABLE agency(agency_id TEXT, agency_name TEXT, agency_url TEXT, agency_timezone TEXT, agency_lang TEXT, agency_phone TEXT, continent TEXT, country TEXT, city TEXT, PRIMARY KEY(agency_id, city) ON CONFLICT IGNORE)')

  # Add a calendar table
  cur.execute('CREATE TABLE calendar(service_id INTEGER REFERENCES trips(service_id), monday INTEGER, tuesday INTEGER, wednesday INTEGER, thursday INTEGER, friday INTEGER, saturday INTEGER, sunday INTERGER, start_date DATETIME, end_date DATETIME)')
  # yyyy-mm-dd hh:mm:ss.xxx

  # Add a calendar_dates table
  cur.execute('CREATE TABLE calendar_dates(service_id INTEGER REFERENCES trips(service_id), date DATETIME, exception_type INTEGER, exception_text TEXT)')

  # Add a feed_info table
  cur.execute('CREATE TABLE feed_info(feed_publisher_name TEXT, feed_publisher_url TEXT, feed_lang TEXT, feed_start_date DATETIME, feed_end_date DATETIME, feed_version TEXT)')

  # Add a routes table
  cur.execute('CREATE TABLE routes(route_id TEXT, agency_id TEXT REFERENCES agency(agency_id), route_short_name TEXT, route_long_name TEXT, route_desc TEXT, route_type INTEGER, route_type_desc TEXT, route_url TEXT, route_color TEXT, text_color TEXT)')

  # Add a shapes table
  cur.execute('CREATE TABLE shapes(shape_id TEXT, shape_pt_lat FLOAT, shape_pt_lon FLOAT, shape_pt_sequence INTEGER, shape_dist_traveled INTEGER)')

  # Add a stop_times table
  cur.execute('CREATE TABLE stop_times(trip_id INTEGER REFERENCES trips(trip_id), arrival_time DATETIME, departure_time DATETIME, stop_id INTEGER REFERENCES stops(stop_id), stop_sequence INTEGER, stop_headsign TEXT, pickup_type INTEGER, pickup_type_text TEXT, drop_off_type INTEGER, drop_off_type_text TEXT, shape_dist_traveled FLOAT)')

  # Add a stops table
  cur.execute('CREATE TABLE stops(stop_id INTEGER, stop_code INTEGER, stop_name TEXT, stop_desc TEXT, stop_lat FLOAT, stop_lon FLOAT, zone_id TEXT, stop_url TEXT, location_type INTEGER, location_type_text TEXT, parent_station INTEGER, stop_timezone TEXT, wheelchair_boarding INTEGER, wheelchair_boarding_text TEXT)')

  # Add a trips table
  cur.execute('CREATE TABLE trips(route_id TEXT REFERENCES routes, service_id INTEGER, trip_id INTEGER, trip_headsign TEXT, trip_short_name TEXT, direction_id INTEGER, direction_id_text TEXT, block_id INTEGER, shape_id TEXT REFERENCES shapes(shape_id), wheelchair_accessible INTEGER, wheelchair_accessible_text TEXT)')

  # Add a intervals table
  cur.execute('CREATE TABLE intervals(trip_id INTEGER REFERENCES trips(trip_id), date DATETIME, lat FLOAT, lon FLOAT, route_type_desc TEXT REFERENCES routes(route_type_desc), pickup_type_text TEXT REFERENCES stop_times(pickup_type_text), drop_off_type_text TEXT REFERENCES stop_times(drop_off_type_text), agency_id TEXT REFERENCES agency(agency_id), route_id TEXT REFERENCES routes(route_id), shape_id TEXT REFERENCES shapes(shape_id))')

  # Add a stop_times_amended table that doesn't store time beyond 23:59:59.999 like the GTFS does
  cur.execute('CREATE TABLE stop_times_amended(trip_id INTEGER REFERENCES trips(trip_id), service_id INTEGER REFERENCES trips(service_id), arrival_time DATETIME, departure_time DATETIME, monday INTEGER, tuesday INTEGER, wednesday INTEGER, thursday INTEGER, friday INTEGER, saturday INTEGER, sunday INTEGER, stop_id INTEGER REFERENCES stops(stop_id), stop_sequence INTEGER, stop_headsign TEXT, pickup_type INTEGER, pickup_type_text TEXT, drop_off_type INTEGER, drop_off_type_text TEXT, shape_dist_traveled FLOAT)')

  GTFSDB.commit()

  return GTFSDB

def populateRoutes(GTFSLocation, database):
  '''
  Populates the routes table of <database> with the information from routes.txt, as well as the equivalent text representations of route_type.
  <GTFSLocation> is a string of the directory containing a text file called "routes.txt."
  Returns <database>, updated with the routes table filled.

  route_id > ID that uniquely identifes a route (dataset unique). REQUIRED.
  agency_id > Defines an agency for a route, referenced from agency.txt. OPTIONAL if there is only one agency, else REQUIRED.
  route_short_name > Short name of a route, such as a number, acronym, colour or shortened text that riders use to identfy a route. REQUIRED if route_long_name is empty, else OPTIONAL.
  route_long_name > Long name of a route, generally more descriptive that route_short_name. Often indicates origin and terminus as words. REQUIRED if route_short_name is empty, else OPTIONAL.
  route_desc > Description of a route, fully textual, detailed information. OPTIONAL.
  route_type > Values between 0 and 7, indicating the mode of transport on a route (tram, bus, train, ferry, etc.). REQUIRED.
  route_type_text > DEFINED BY RICHARD LAW, the textual values corresponding to route_type integers, from https://developers.google.com/transit/gtfs/reference#routes_fields. REQUIRED.
  route_url > The URL of a Web page about that particular route; should be different from agency_url. OPTIONAL.
  route_color > In systems that have colours assigned to routes; six-character hexadecimal. The default is white (FFFFFF). OPTIONAL.
  route_text_color > Can be used to specify a legible colour to use for text drawn against a background of route_color; six-character hexadecimal. Default is black (000000). OPTIONAL.

  Information: https://developers.google.com/transit/gtfs/reference#routes_fields
  Author: Richard Law
  Created: 20131104
  Edited: 20131104

  '''
  cur = database.cursor()
  routes = GTFSLocation + "routes.txt."
  with open(routes) as f:
    next(f) # skip header
    for line in f:
      route = line.split(",")
      route_id, agency_id, route_short_name, route_long_name, route_desc, route_type, route_url, route_color, route_text_color = route[0], route[1], route[2], route[3], route[4], route[5], route[6], route[7], route[8]

      # Handling null values
      LOV = [route_id, agency_id, route_short_name, route_long_name, route_desc, route_type, route_url, route_color, route_text_color]
      index = 0
      for value in LOV:
        if len(value) == 0:
          # If the value is empty for the column
          LOV[index] = None
        index += 1

      route_id, agency_id, route_short_name, route_long_name, route_desc, route_type, route_url, route_color, route_text_color = LOV[0], LOV[1], LOV[2], LOV[3], LOV[4], LOV[5], LOV[6], LOV[7], LOV[8]

      # Non-string values
      route_type = int(route_type)

      # Get a text representation of route_type
      if route_type == 0:
        route_type_text = "Tram, Streetcar, Light Rail"
        route_color = "006600" # Dark green
      elif route_type == 1:
        route_type_text = "Subway, Metro"
        route_color = "FF6633" # Orange
      elif route_type == 2:
        route_type_text = "Rail"
        route_color = "000000" # Black
      elif route_type == 3:
        route_type_text = "Bus"
        route_color = "660066" # Darkish purple
      elif route_type == 4:
        route_type_text = "Ferry"
        route_color = "3399FF" # Light blue
      elif route_type == 5:
        route_type_text = "Cable Car"
        route_color = "CC0000" # Darkish red
      elif route_type == 6:
        route_type_text = "Gondola, Suspended Cable Car"
        route_color = "669966" # Greyish green
      elif route_type == 7:
        route_type_text = "Funicular"
        route_color = "ff3366" # Pink
      else:
        route_type_text = None

      # Default route colour is white.
      if route_color == None or route_color == "\n":
        route_color = "FFFFFF"

      # Defaul route text is black.
      if route_text_color == None or route_text_color == "\n":
        route_text_color = "000000"

      cur.execute('INSERT INTO routes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (route_id, agency_id, route_short_name, route_long_name, route_desc, route_type, route_type_text, route_url, route_color, route_text_color))

    database.commit()

    return database

def populateAgency(GTFSLocation, database, continent, country, city):
  '''
  Populates the routes table of <database> with the information from agency.txt.
  Forces agency_lang to lower case despite agency.txt.
  <GTFSLocation> is a string of the directory containing a text file called "agency.txt."
  Returns <database>, updated with the routes table filled.
  <continent>, <country> and <city> are all strings; more information follows.

  agency_id > An ID that uniquely identifies a transit agency. Dataset unique. OPTIONAL for feeds with a single agency, else REQUIRED.
  agency_name > Full name of the transit agency. REQUIRED.
  agency_url > URL of the transit agency; must be fullly qualified (http:// or https://). REQUIRED.
  agency_timezone > See http://en.wikipedia.org/wiki/List_of_tz_zones for a list of valid values. REQUIRED.
  agency_lang > Two-letter ISO 639-1 code for the primary language used by this transit agency. OPTIONAL.
  agency_phone > Diallable text is permitted. OPTIONAL.
  agency_fare_url > URL of a web page that allows a rider to purchase tickets or other fare instruments for that agency. OPTIONAL.
  <continent> > DEFINED BY RICHARD LAW: the continent where the agency operates.
  <country> > DEFINED BY RICHARD LAW: the country where the agency operates.
  <city> > DEFINED BY RICHARD LAW: the (primary) city where the agency operates.

  Information: https://developers.google.com/transit/gtfs/reference#agency_fields
  Author: Richard Law
  Created: 20131104
  Edited: 20131104
  '''
  cur = database.cursor()
  agencies = GTFSLocation + "agency.txt."
  with open(agencies) as f:
    next(f) # skip header
    for line in f:
      agency = line.split(",")
      agency_id, agency_name, agency_url, agency_timezone, agency_lang, agency_phone = agency[0], agency[1], agency[2], agency[3], agency[4], agency[5]

      # Handling null values
      arrayOfValues = (agency_id, agency_name, agency_url, agency_timezone, agency_lang, agency_phone)
      for value in arrayOfValues:
        if len(value) == 0:
          # If the value is empty for the column
          header = None

      # Capitalisation
      agency_lang = agency_lang.lower()

      cur.execute('INSERT INTO agency VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (agency_id, agency_name, agency_url, agency_timezone, agency_lang, agency_phone, continent, country, city))

    database.commit()

    return database


def populateCalendar(GTFSLocation, database):
  '''
  Populates the calendar table of <database> with the information from calendar.txt.
  <GTFSLocation> is a string of the directory containing a text file called "calendar.txt."
  Returns <database>, updated with the calendar table filled.

  service_id > ID that uniquely identifes a set of dates when service is available for one or more routes Dataset unique. References trips.txt. REQUIRED.
  monday > A binary value (0 or 1) indicating whether the service is valid for all Mondays. 1: the service is valid for all Mondays in the date range (start_date and end_date). 0: the service is not available on Mondays in the date range. Exceptions for particular dates (e.g. holidays) may be listed in calendar_dates.txt. REQUIRED.
  tuesday > See monday. REQUIRED.
  wednesday > See monday. REQUIRED.
  thursday > See monday. REQUIRED.
  friday > See monday. REQUIRED.
  saturday > See monday. REQUIRED.
  sunday > See monday. REQUIRED.
  start_date > The start date for the service. YYYYMMDD format. REQUIRED.
  end_date > The end date for the service (included in the interval). YYYYMMDD format. REQUIRED.

  Information: https://developers.google.com/transit/gtfs/reference#calendar_fields
  Author: Richard Law
  Created: 20131104
  Edited: 20131104
  '''
  cur = database.cursor()
  calendars = GTFSLocation + "calendar.txt."
  with open(calendars) as f:
    next(f) # skip header
    for line in f:
      calendar = line.split(",")
      service_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, start_date, end_date = calendar[0], calendar[1], calendar[2], calendar[3], calendar[4], calendar[5], calendar[6], calendar[7], calendar[8], calendar[9]

      # Get ISO8601 string datetimes for start_date and end_date
      start_date = start_date[0:4] + "-" + start_date[4:6] + "-" + start_date[6:8] + " 00:00:00.000"
      end_date = end_date[0:4] + "-" + end_date[4:6] + "-" + end_date[6:8] + " 00:00:00.000"

      # Handling null values
      LOV = [service_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, start_date, end_date]
      index = 0
      for value in LOV:
        if len(value) == 0:
          # If the value is empty for the column
          LOV[index] = None
        index += 1

      service_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, start_date, end_date = LOV[0], LOV[1], LOV[2], LOV[3], LOV[4], LOV[5], LOV[6], LOV[7], LOV[8], LOV[9]

      # Non-string values
      monday = int(monday)
      tuesday = int(tuesday)
      wednesday = int(wednesday)
      thursday = int(thursday)
      friday = int(friday)
      saturday = int(saturday)
      sunday = int(sunday)

      cur.execute('INSERT INTO calendar VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (service_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, start_date, end_date))

    database.commit()

    return database

def populateCalendarDates(GTFSLocation, database):
  '''
  Populates the calendar_dates table of <database> with the information from calendar.txt.
  The calendar_dates table allows one to explicitly activate or disable service IDs by date.
  It can be used in two ways:
  1. Recommended: Use calendar_dates.txt in conjunction with calendar.txt, where calendar_dates.txt defines any exceptions to the default service categories defined in the calendar.txt file. If your service is generally regular, with a few changes on explicit dates (for example, to accomodate special event services, or a school schedule), this is a good approach.
  2. Alternate: Omit calendar.txt, and include ALL dates of service in calendar_dates.txt. If your schedule varies most days of the month, or you want to programmatically output service dates without specifying a normal weekly schedule, this approach may be preferable.

  If the a service_id value appears in both the calendar and calendar_dates tables, the information in calendar_dates modifies the service information specified in calendar.

  <GTFSLocation> is a string of the directory containing a text file called "calendar.txt."
  Returns <database>, updated with the calendar table filled.

  service_id > ID that uniquely identifes a set of dates when service is available for one or more routes Dataset unique. Each (service_id, date) pair can only appear once. References trips.txt. REQUIRED.
  date > The date field specifies a particular date when service availability is different than the norm. Format: YYYYMMDD. REQUIRED.
  exception_type > Indicates whether service is available on the date specified in the date field. Values: 1 = the service has been added for date. 2 = the service has been removed for date. REQUIRED.
  exception_text > DEFINED BY RICHARD LAW: Textual correspondance of the values in exception_type.

  Information: https://developers.google.com/transit/gtfs/reference#calendar_dates_fields
  Author: Richard Law
  Created: 20131106
  Edited: 20131106
  '''
  cur = database.cursor()
  dates = GTFSLocation + "calendar_dates.txt."
  with open(dates) as f:
    next(f) # skip header
    for line in f:
      cdate = line.split(",")
      service_id, date, exception_type = cdate[0], cdate[1], cdate[2]

      # Get ISO8601 string datetimes for start_date and end_date
      date = date[0:4] + "-" + date[4:6] + "-" + date[6:8] + " 00:00:00.000"

      # Handling null values
      LOV = [service_id, date, exception_type]
      index = 0
      for value in LOV:
        if len(value) == 0:
          # If the value is empty for the column
          LOV[index] = None
        index += 1

      service_id, date, exception_type = LOV[0], LOV[1], LOV[2]

      # Non-string values
      exception_type = int(exception_type)

      # Textual correspondence to exception_type
      if exception_type == 1:
        exception_text = "Added"
      elif exception_type == 2:
        exception_text = "Removed"

      cur.execute('INSERT INTO calendar_dates VALUES (?, ?, ?, ?)', (service_id, date, exception_type, exception_text))

    database.commit()

    return database

def populateTrips(GTFSLocation, database):
  '''
  Populates the trips table of <database> with the information from trips.txt.
  The trips table details individual PT trips, including the direction, the name and via concordance with routes, shapes, calendar and calendar_dates: the dates, exceptions and spatial representations.

  <GTFSLocation> is a string of the directory containing a text file called "calendar.txt."
  Returns <database>, updated with the calendar table filled.

  route_id > ID that uniquely identifes a route. References routes. REQUIRED.
  service_id > ID that uniquely identifies a set of dates when a service is available for one or more routes. References from calendar or calendar_dates. REQUIRED.
  trip_id > ID that uniqely identifies a trip. Dataset unique. REQUIRED.
  trip_headsign > The text that appears on a sign that identifies the trip's destination to passengers. Distinguishes different patterns of service in the same route. If the headsign changes during a trip, the trip_headsign can be overwritten by reference to value: stop_headsign in table: stop_times. OPTIONAL.
  trip_short_name > The text that appears in schedules and sign boards to identify the trip to passengers, for example, to identify train numbers for commuter rail trips. A trip_short_name value, if provided, should __uniquely identify a trip within a service day__; it should not be used for destination names or limited/express designations. OPTIONAL.
  direction_id > A binary value that indicates the direction of travel for a trip. Use this field to distinguish between bi-directional trips with the same route_id. OPTIONAL.
  direction_id_text > DEFINED BY RICHARD LAW: Textual correspondence of direction_id (outbound/inbound). OPTIONAL.
  block_id > Identifies the block to which the trip belongs. A block consists of two or more sequential trips made using the same vehicle, where a passenger can transfer from one trip to the next just by staying in the vehicle. The block_id must be referenced by two or more trips in table: trips. OPTIONAL.
  shape_id > An ID that defines a shape for the trip. This value is referenced from the table: shapes. OPTIONAL.
  wheelchair_accessible > Integer values corresponding to the ability for riders requiring wheelchairs to ride on the trip. 0 or empty = There is no accesibility information for the trip. 1 = The vehicle used for this trip CAN acomodate at least one wheelchair. 2 = No wheelchairs can be accomodated on this trip. OPTIONAL.
  wheelchair_accessible_text > DEFINED BY RICHARD LAW" Textual correspondence of wheelchair_accessible (0 or empty = Unknown. 1 = Accessible. 2 = Inaccessible.

  Information: https://developers.google.com/transit/gtfs/reference#trips_fields
  Author: Richard Law
  Created: 20131106
  Edited: 20131106
  '''
  cur = database.cursor()
  trips = GTFSLocation + "trips.txt."
  with open(trips) as f:
    next(f) # skip header
    for line in f:
      trip = line.split(",")

      route_id, service_id, trip_id, trip_headsign, direction_id, block_id, shape_id = trip[0], trip[1], trip[2], trip[3], trip[4], trip[5], trip[6]
      # no trip_short_name in Wellington
      trip_short_name = None
      # no wheelchair_accessible in Wellington
      wheelchair_accessible = None

      # Handling null values
      LOV = [route_id, service_id, trip_id, trip_headsign, trip_short_name, direction_id, block_id, shape_id, wheelchair_accessible]
      index = 0
      for value in LOV:
        if value is not None:
          if len(value) == 0:
            # If the value is empty for the column
            LOV[index] = None
        index += 1
      route_id, service_id, trip_id, trip_headsign, trip_short_name, direction_id, block_id, shape_id, wheelchair_accessible = LOV[0], LOV[1], LOV[2], LOV[3], LOV[4], LOV[5], LOV[6], LOV[7], LOV[8]

      # Non-string values
      # Try/excepts are for None types, which are ignored.
      try:
        direction_id = int(direction_id)
      except:
        direction_id = None
      try:
        block_id = int(block_id)
      except:
        block_id = None
      try:
        wheelchair_accessible = int(wheelchair_accessible)
      except:
        wheelchair_accessible = None

      # Textual correspondence to directon_id
      if direction_id == 0:
        # Travel in one direction (e.g. outbound travel)
        direction_id_text = "Outbound"
      elif direction_id == 1:
        # Travel in the opposite direction (e.g. inbound travel)
        direction_id_text = "Inbound"

      # Textual correspondence to wheelchair_accessible
      if wheelchair_accessible == 0 or wheelchair_accessible is None:
        wheelchair_accessible_text = "Unknown"
      elif wheelchair_accessible == 1:
        wheelchair_accessible_text = "Accessible"
      elif wheelchair_accessible == 2:
        wheelchair_accessible_text = "Inaccessible"

      cur.execute('INSERT INTO trips VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (route_id, service_id, trip_id, trip_headsign, trip_short_name, direction_id, direction_id_text, block_id, shape_id, wheelchair_accessible, wheelchair_accessible_text))

    database.commit()

    return database

def populateShapes(GTFSLocation, database):
  '''
  Populates the shapes table of <database> with the information from shapes.txt.
  The shapes table details the spatial representation (ordered vertices) of PT routes, identifiable with shape_id.

  This script also tests whether the agency has genuinely supplied the length of the routes, or just copied the sequence information. If all of the shape_dist_traveled values are equal to shape_pt_sequence (as in Wellington), then shape_dist_traveled is uniformly set to None.

  <GTFSLocation> is a string of the directory containing a text file called "calendar.txt."
  Returns <database>, updated with the calendar table filled.

  shape_id > An ID that uniquely identfies a shape (e.g. a line). NOT DATASET UNIQUE BECAUSE ONE LINE HAS MANY VERTICES. REQUIRED.
  shape_pt_lat > Latitude of the vertex. WGS84. REQUIRED.
  shape_pt_lon > Longitude of the vertex. WGS84. REQUIRED.
  shape_pt_sequence > The sequence order along the shape. Non-negative integers that increase along the trip. REQUIRED.
  shape_dist_traveled > A real distance along the route that the stop occurs. Must increase along the route, and cannot be used to show reverse travel along a route. Begins at 0. Could be in any unit, such as feet or kilometres. OPTIONAL.

  Information: https://developers.google.com/transit/gtfs/reference#shapes_fields
  Author: Richard Law
  Created: 20131106
  Edited: 20131106
  '''
  trueDistance = True # Assume that the agency actually gives distance values.
  countMatches = 0 # Set matches to 0

  cur = database.cursor()
  shapes = GTFSLocation + "shapes.txt."
  with open(shapes) as f:
    next(f) # skip header
    rows = sum(1 for l in f) - 1 # Counts the number of records, which is very large. Subtracts one to correspond to countMatches, which begins at 0.

    # True distance provided?
    for line in f:
      shape = line.split(",")
      shape_pt_sequence, shape_distance_traveled = shape[3], shape[4]
      if shape[4] != '':
        if shape_pt_sequence == shape_distance_traveled:
          countMatches += 1
    if countMatches == rows: # If EVERY row is just the sequence number...
      trueDistance = False # ...confirm that the agency does not give actual distance values.

  with open(shapes) as g:
    next(g) # skip header
    for line in g:
      shape = line.split(",")

      shape_id, shape_pt_lat, shape_pt_lon, shape_pt_sequence, shape_dist_traveled = shape[0], shape[1], shape[2], shape[3], shape[4]

      if trueDistance == False:
        # If the distance field isn't actually distance:
        shape_dist_traveled = None

      # Handling null values
      LOV = [shape_id, shape_pt_lat, shape_pt_lon, shape_pt_sequence, shape_dist_traveled]
      index = 0
      for value in LOV:
        if value is not None:
          if len(value) == 0:
            # If the value is empty for the column
            LOV[index] = None
        index += 1
      shape_id, shape_pt_lat, shape_pt_lon, shape_pt_sequence, shape_dist_traveled = LOV[0], LOV[1], LOV[2], LOV[3], LOV[4]

      # Non-string values
      # Try/excepts are for None types, which are ignored.
      shape_pt_lat = float(shape_pt_lat)
      shape_pt_lon = float(shape_pt_lon)
      shape_pt_sequence = int(shape_pt_sequence)
      try:
        shape_dist_traveled = float(shape_dist_traveled)
      except:
        shape_dist_traveled = None

      cur.execute('INSERT INTO shapes VALUES (?, ?, ?, ?, ?)', (shape_id, shape_pt_lat, shape_pt_lon, shape_pt_sequence, shape_dist_traveled))

    database.commit()

    return database

def populateFeedInfo(GTFSLocation, database):
  '''
  Populates the feed_info table of <database> with the information from feed_info.txt.
  The feed_info table details the agency who created the GTFS feed, including a link to their website for further information.
  Information about the feed itself, rather than the services that the feed describes.
  The publisher of the feed is sometimes a different entity than any of the agencies in the agency table.

  <GTFSLocation> is a string of the directory containing a text file called "calendar.txt."
  Returns <database>, updated with the calendar table filled.

  feed_publisher_name > The full name of the organization that publishes the feed. This may be the same as one of the agency_name values in the agency table. REQUIRED.
  feed_publisher_url > The URL of the feed publishing organization's website. This must be a fully qualified URL that includes http:// or https://, and any special characters in the URL are correctly escaped. REQUIRED.
  feed_lang > IETF BCP 47 language code specifying the default language used for the text in this feed. This setting helps GTFS consumers choose capitalization rules and other language-specific settings for the feed. See http://www.rfc-editor.org/rfc/bcp/bcp47.txt and http://www.w3.org/International/articles/language-tags/. REQUIRED.
  feed_start_date > The feed provides complete and reliable schedule information for service in the period from the beginning of the feed_start_date day to the end of the feed_end_date day. Both days are given as dates in YYYYMMDD format, or left empty if unavailable. Data can be given outside of this range, but it such data carries non-authoritative status. OPTIONAL.
  feed_end_date > The feed provides complete and reliable schedule information for service in the period from the beginning of the feed_start_date day to the end of the feed_end_date day. Both days are given as dates in YYYYMMDD format, or left empty if unavailable. Data can be given outside of this range, but it such data carries non-authoritative status. OPTIONAL.
  feed_version > The feed publisher can specify a string here that indicates the current version of their GTFS feed. GTFS-consuming applications can display this value to help feed publishers determine whether the latest version of their feed has been incorporated. OPTIONAL.

  Information: https://developers.google.com/transit/gtfs/reference#feed_info_fields
  Author: Richard Law
  Created: 20131106
  Edited: 20131106
  '''
  cur = database.cursor()
  feed_infos = GTFSLocation + "feed_info.txt."

  with open(feed_infos) as g:
    next(g) # skip header
    for line in g:
      feed_info = line.split(",")

      feed_publisher_name, feed_publisher_url, feed_lang, feed_start_date, feed_end_date = feed_info[0], feed_info[1], feed_info[2], feed_info[3], feed_info[4]
      # no feed_version in Wellington
      feed_version = None

      # Handling null values
      LOV = [feed_publisher_name, feed_publisher_url, feed_lang, feed_start_date, feed_end_date, feed_version]
      index = 0
      for value in LOV:
        if value is not None:
          if len(value) == 0:
            # If the value is empty for the column
            LOV[index] = None
        index += 1
      feed_publisher_name, feed_publisher_url, feed_lang, feed_start_date, feed_end_date, feed_version = LOV[0], LOV[1], LOV[2], LOV[3], LOV[4], LOV[5]

      # Get ISO8601 string datetimes for feed_start_date and feed_end_date
      feed_start_date = feed_start_date[0:4] + "-" + feed_start_date[4:6] + "-" + feed_start_date[6:8] + " 00:00:00.000"
      feed_end_date = feed_end_date[0:4] + "-" + feed_end_date[4:6] + "-" + feed_end_date[6:8] + " 00:00:00.000"

      # Capitalisation
      feed_lang = feed_lang.lower()

      cur.execute('INSERT INTO feed_info VALUES (?, ?, ?, ?, ?, ?)', (feed_publisher_name, feed_publisher_url, feed_lang, feed_start_date, feed_end_date, feed_version))

    database.commit()

    return database

def populateStops(GTFSLocation, database):
  '''
  Populates the stops table of <database> with the information from stops.txt.
  The stops table has information about PT stops, stations, interchanges and the like that the PT vehicles and passengers coincide at.

  <GTFSLocation> is a string of the directory containing a text file called "calendar.txt."
  Returns <database>, updated with the calendar table filled.

  stop_id > An ID that uniquely identifies a stop or station. Multiple routes may use the same stop. The stop_id is dataset unique. REQUIRED.
  stop_code > Short text or a number that uniquely identifies the stop for passengers, such as for text-based schedule information delivery. OPTIONAL.
  stop_name > The name of a stop or station. A name that people understand in the local and tourist vernacular. REQUIRED.
  stop_desc > A description of a stop. Useful, quality information. Not simply a duplicate of the name of the stop. OPTIONAL.
  stop_lat > The latitude of a stop or station. WGS84. REQUIRED.
  stop_lon > The longitude of a stop or station. WGS84. REQUIRED.
  zone_id > The fare zone for a stop ID. Zone IDs are required if you want to provide fare information using fare_rules.txt. OPTIONAL.
  stop_url > URL of a web page about that particular stop. Different from the feed_url, agency_url and route_url fields of other tables.
  location_type > Identifies whether this stop ID represents a stop or station. Default is that it is a stop. 0 or blank: stop (where passengers board or disembark). 1: station (structure or area that contains one or more stops).. OPTIONAL.
  location_type_text > DEFINED BY RICHARD LAW: Text correspondence of location_type ("Stop", "Station" or "Hail and Ride"). "Hail and Ride" is a custom option added by Richard, and is deemed to exist if the field has no other specification and the name of the stop contains the text "hail and ride". OPTIONAL.
  parent_station > For stops that are physically located inside stations, the parent_station field identifies the station associated with the stop. To use this field, stops.txt must also contain a row where this stop ID is assigned location_type=1. Contains a stop_id if location_type=0 and the stop is INSIDE a station. Is 0 or blacnk if location_type=0 and the stop is not inside a station. Is 1 if it is a station. OPTIONAL.
  stop_timezone > The timezone in which this stop or station is located. See: http://en.wikipedia.org/wiki/List_of_tz_zones. If omitted, the stop is assumed to be located in the timezone specified by agency_timezone in agency.txt. OPTIONAL.
  wheelchair_boarding > Identifies whether wheelchair boardings are possible from the specified stop or station. 0 or empty: there is no accessibility information for the stop. 1: there exists some accessible path from outside the station to the stop/platform. 2: there exists NO accessible path to the stop/platform.
  wheelchair_boarding_text > DEFINED BY RICHARD LAW: Text correspondence of wheelchair_boarding ("Unknown", "Accessible" or "Inaccessible"). OPTIONAL.

  Note: Requires that the agency table has been populated first.

  This script also checks for "hail and ride" stops, and includes them as a custom location_type.

  Information: https://developers.google.com/transit/gtfs/reference#stops_fields
  Author: Richard Law
  Created: 20131106
  Edited: 20131106
  '''
  cur = database.cursor()
  stops = GTFSLocation + "stops.txt."

  print "Note: populateStops() currently gives an incorrect stop_timezone for GTFS feeds outside New Zealand."

  with open(stops) as g:
    next(g) # skip header
    for line in g:
      line = line.replace(", ", " - ") # Replaces ", ", which appears in text descriptions of stop names, with a hyphen surrounded by spaces. For correct parsing.
      stop = line.split(",")

      stop_id, stop_code, stop_name, stop_desc, stop_lat, stop_lon, zone_id, stop_url, location_type, parent_station = stop[0], stop[1], stop[2], stop[3], stop[4], stop[5], stop[6], stop[7], stop[8], stop[9]
      # no wheelchair_boarding in Wellington
      wheelchair_boarding = None

      # stop_timezone
      # For now, I am assuming this remains within New Zealand
      stop_timezone = "Pacific/Auckland"

      # Handling null values
      LOV = [stop_id, stop_code, stop_name, stop_desc, stop_lat, stop_lon, zone_id, stop_url, location_type, parent_station, stop_timezone, wheelchair_boarding]
      index = 0
      for value in LOV:
        if value is not None:
          if len(value) == 0:
            # If the value is empty for the column
            LOV[index] = None
        index += 1
      stop_id, stop_code, stop_name, stop_desc, stop_lat, stop_lon, zone_id, stop_url, location_type, parent_station, stop_timezone, wheelchair_boarding = LOV[0], LOV[1], LOV[2], LOV[3], LOV[4], LOV[5], LOV[6], LOV[7], LOV[8], LOV[9], LOV[10], LOV[11]

      # Non-string values
      # Try/excepts are for None types, which are ignored.
      stop_lat = float(stop_lat)
      stop_lon = float(stop_lon)
      try:
        location_type = int(location_type)
      except:
        location_type = None
      try:
        wheelchair_boarding = int(wheelchair_boarding)
      except:
        wheelchair_boarding = None

      # wheelchair_boarding_text
      if wheelchair_boarding is None or wheelchair_boarding == 0:
        wheelchair_boarding_text = "Unknown"
      elif wheelchair_boarding == 1:
        wheelchair_boarding_text = "Accessible"
      elif wheelchair_boarding == 2:
        wheelchair_boarding == "Inaccessible"

      # location_type_text
      if location_type is None or location_type == 0:
        location_type_text = "Stop"
        # Hail and ride option
        if "hail & ride" in stop_name.lower() or "hail and ride" in stop_name.lower():
          # Location type number itself is NOT changed, due to dependencies of other tables.
          location_type_text = "Hail and Ride"
      elif location_type == 1:
        location_type_text = "Station"

      cur.execute('INSERT INTO stops VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (stop_id, stop_code, stop_name, stop_desc, stop_lat, stop_lon, zone_id, stop_url, location_type, location_type_text, parent_station, stop_timezone, wheelchair_boarding, wheelchair_boarding_text))

    database.commit()

    return database

def populateStopTimes(GTFSLocation, database):
  '''
  Populates the stop_times table of <database> with the information from stop_times.txt.
  This table has information about when each trip stops at each stop (so is VERY large).

  <GTFSLocation> is a string of the directory containing a text file called "calendar.txt."
  Returns <database>, updated with the calendar table filled.

  trip_id > ID that identifies a trip. References trips table.
  arrival_time > The arrival time. Time is noon minus 12h, which is midnight for all days except those for which daylight savings time changes occur. For times occurring after midnight on the service date, enter the time as a value __greater than 24:00:00__ in HH:MM:SS local time for the day on which the trip schedule begins. Stops without arrival times will be empty: not interpolated. Values must be specified for the first and last stops of a trip. HH:MM:SS, or H:MM:SS of the hour begins with 0. REQUIRED, but can be empty in meaningful conditions.
  departure_time > The departure time. See arrival_time. REQUIRED, but can be empty in meanigful conditions.
  stop_id > The stop_id, references stops table.
  stop_sequence > The order of the stoops for the trip. Non-negative intergers that increase with the trip. Does not have to progress in steps of 1 (i += 1 or i++). REQUIRED.
  stop_headsign > Text that appears on a sign that identifies a trip's destination to passengers. Use this field to override the default trip_headsign when the headsign changes between stops. If this headsign is associated with an entire trip, use trip_headsign instead.
  pickup_type > Indicates whether passengers are picked up at a stop as part of the normal schedule, or whether a pickup at the stop is not available or has special conditions. Value=0: Regularly scheduled pickup. Value=1: No pickup available. Value=2: Must phone agency to arrange pickup. Value=3: Must coordinate with driver to arrange pickup. Default is 0. OPTIONAL.
  pickup_type_text > DEFINED BY RICHARD LAW: Text correspondence to pickup_type. "Pickup", "No Pickup" "Agency Pickup", "Coordinate Pickup" correspond to 0 (or empty), 1, 2, 3.
  drop_off_type > Indicates whether passengers are dropped off at a stop as part of the normal schedule, or whether a dropoff at the stop is not available or has special conditions. Value=0: Regularly scheduled dropoff. Value=1: No dropoff available. Value=2: Must phone agency to arrange dropoff. Value=3: Must coordinate with driver to arrange dropoff. Default is 0. OPTIONAL.
  drop_off_type_text > DEFINED BY RICHARD LAW: Text correspondence to drop_off_type. "Drop Off", "No Drop Off" "Agency Drop Off", "Coordinate Drop Off" correspond to 0 (or empty), 1, 2, 3.
  shape_dist_traveled > Positions a stop as adistance from the first stop. The real distance travelled along a route in units such as feet or kilometres. Must increase with sequence, cannot be used to show reverse travel. Must match the units used in shapes table. OPTIONAL.

  Information: https://developers.google.com/transit/gtfs/reference#stop_times_fields
  Author: Richard Law
  Created: 20131106
  Edited: 20131106
  '''
  cur = database.cursor()
  stop_times = GTFSLocation + "stop_times.txt."

  print "Reminder: arrival and departure times in the stops table can permissibly be empty or extend beyond 24h."

  with open(stop_times) as g:
    next(g) # skip header
    for line in g:
      line = line.replace(", ", " - ") # Replaces ", ", which appears in text descriptions of stop names, with a hyphen surrounded by spaces. For correct parsing.
      stop_time = line.split(",")

      trip_id, arrival_time, departure_time, stop_id, stop_sequence, stop_headsign, pickup_type, drop_off_type, shape_dist_traveled = stop_time[0], stop_time[1], stop_time[2], stop_time[3], stop_time[4], stop_time[5], stop_time[6], stop_time[7], stop_time[8]

      # Handling null values
      LOV = [trip_id, arrival_time, departure_time, stop_id, stop_sequence, stop_headsign, pickup_type, drop_off_type, shape_dist_traveled]
      index = 0
      for value in LOV:
        if value is not None:
          if len(value) == 0:
            # If the value is empty for the column
            LOV[index] = None
        index += 1
      trip_id, arrival_time, departure_time, stop_id, stop_sequence, stop_headsign, pickup_type, drop_off_type, shape_dist_traveled = LOV[0], LOV[1], LOV[2], LOV[3], LOV[4], LOV[5], LOV[6], LOV[7], LOV[8]

      # Non-string values
      # Try/excepts are for None types, which are ignored.
      trip_id = int(trip_id)
      stop_id = int(stop_id)
      stop_sequence = int(stop_sequence)
      try:
        pickup_type = int(pickup_type)
      except:
        pickup_type = None
      try:
        drop_off_type = int(drop_off_type)
      except:
        drop_off_type = None
      try:
        shape_dist_traveled = float(shape_dist_traveled)
      except:
        shape_dist_traveled = None

      # Arrival and departure times
      if len(arrival_time) == 0 or arrival_time is None:
        arrival_time = None
        print "## Null arrival time noted for trip_id %i, stop_id %i. ##" % (trip_id, stop_id)
      else:
        arrival_time = arrival_time.split(":")
        hour = arrival_time[0]
        minutes = arrival_time[1]
        seconds = arrival_time[2]
        if len(hour) == 1:
          # Then it is an hour before midday
          hour = "0" + hour
        arrival_time = hour + ":" + minutes + ":" + seconds + ".000"

      if len(departure_time) == 0 or departure_time is None:
        departure_time = None
        print "## Null departure time noted for trip_id %i, stop_id %i. ##" % (trip_id, stop_id)
      else:
        departure_time = departure_time.split(":")
        hour = departure_time[0]
        minutes = departure_time[1]
        seconds = departure_time[2]
        if len(hour) == 1:
          # Then it is an hour before midday
          hour = "0" + hour
        departure_time = hour + ":" + minutes + ":" + seconds + ".000"

      # Drop-off and pickup type correspondence
      if pickup_type is None or pickup_type == 0:
        pickup_type_text = "Pickup"
      elif pickup_type == 1:
        pickup_type_text = "No Pickup"
      elif pickup_type == 2:
        pickup_type_text = "Agency Pickup"
      elif pickup_type == 3:
        pickup_type_text = "Coordinate Pickup"

      if drop_off_type is None or drop_off_type == 0:
        drop_off_type_text = "Drop Off"
      elif drop_off_type == 1:
        drop_off_type_text = "No Drop Off"
      elif drop_off_type == 2:
        drop_off_type_text = "Agency Drop Off"
      elif drop_off_type == 3:
        drop_off_type_text = "Coordinate Drop Off"

      cur.execute('INSERT INTO stop_times VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (trip_id, arrival_time, departure_time, stop_id, stop_sequence, stop_headsign, pickup_type, pickup_type_text, drop_off_type, drop_off_type_text, shape_dist_traveled))

    database.commit()

    return database

def populateStopTimesAmended(database):
  '''
  Because the GTFS recommends that time be stored as post-23:59:59.999
  when the trips originate before midnight (and even when it doesn't),
  this table stores a corrected format of the stop_times table that has
  no time that exceeds "23:59:59.999".
  it manages this by including a series of columns (monday through sunday)
  that mirror the calendar table. Thus a trip may start on Saturday att
  2330pm and end at sunday at 0100m. This table records that more
  sensibly than the GTFS default, which is to say the trip runs on
  Saturday at 2330 and ends on Saturday at 2500.
  '''
  def calendarOffset(weekbinary):
    '''
    <weekbinary> is a list of the form [1,1,1,1,1,0,0] (example)
    where the digits are binary indications of whether the trip runs on
    a given day, where each number refers to the week MTWTFSS
    '''
    origmon, origtue, origwed, origthu, origfri, origsat, origsun = weekbinary[0], weekbinary[1],weekbinary[2], weekbinary[3], weekbinary[4], weekbinary[5], weekbinary[6]
    return [origsun, origmon, origtue, origwed, origthu, origfri, origsat]

  def maxBinary(week1, week2):
    week = []
    i = 0
    for day in week1:
      week.append(max(day, week2[i]))
      i+=1
    return week

  cur = database.cursor()

  # Build a concordance from trip_id to service_id
  cur.execute('SELECT trip_id, service_id FROM trips')
  trip_service = {}
  for tripserv in cur.fetchall():
    trip_id, service_id = tripserv[0], tripserv[1]
    trip_service[trip_id] = service_id

  # Build a concordance from service_id to day of the week
  cur.execute('SELECT service_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday FROM calendar')
  servday = {}
  for servcal in cur.fetchall():
    service_id = servcal[0]
    monday, tuesday, wednesday, thursday, friday, saturday, sunday = servcal[1], servcal[2], servcal[3], servcal[4], servcal[5], servcal[6], servcal[7]
    servday[service_id] = [int(monday), int(tuesday), int(wednesday), int(thursday), int(friday), int(saturday), int(sunday)]

  # Copy the rows of calendar into stop_times_amended
  # For each stop in a trip (record of stop_times), check if it is after midnight
  cur.execute('SELECT * FROM stop_times')
  for stoppedtrip in cur.fetchall():
    trip_id = stoppedtrip[0]
    arrival_time = stoppedtrip[1]
    departure_time = departure_time = stoppedtrip[2]
    stop_id = stoppedtrip[3]
    stop_sequence = stoppedtrip[4]
    stop_headsign = stoppedtrip[5]
    pickup_type = stoppedtrip[6]
    pickup_type_text = stoppedtrip[7]
    drop_off_type = stoppedtrip[8]
    drop_off_type_text = stoppedtrip[9]
    shape_dist_traveled = stoppedtrip[10]

    service_id = trip_service[trip_id]
    week = servday[service_id]

    arriveafter, departafter = False, False
    if int(arrival_time[0:2]) >= 24:
      # Then the trip arrives at the stop after or at midnight
      newarrivaltime = int(arrival_time[0:2])-24
      arrival_time = str(newarrivaltime) + arrival_time[2:]
      # Offset the calendar by one day
      week_arrive = calendarOffset(week)
      arriveafter = True

    if int(departure_time[0:2]) >= 24:
      newdeparturetime = int(departure_time[0:2])-24
      departure_time = str(newdeparturetime) + departure_time[2:]
      # Offset the calendar by one day
      week_depart = calendarOffset(week)
      departafter = True

    if arriveafter == False and departafter == True:
      # Then the trip arrives at a stop, dwells, and then departs
      # and the clock ticks over midnight during the dwell
      # The calendar needs to reflect this
      # I made maxBinary to do something about this, but I don't like it
      ## week = maxBinary[week_arrive, week_depart]
      raise AttributeError

    elif arriveafter == True and departafter == False:
      # This is impossible
      raise AttributeError

    elif arriveafter == True and departafter == True:
      if week_arrive == week_depart:
        # If they're equal, just take the arrive one as authoritative
        week = week_arrive
      else:
        raise Exception

    cur.execute('INSERT INTO stop_times_amended VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (trip_id, service_id, arrival_time, departure_time, week[0], week[1], week[2], week[3], week[4], week[5], week[6], stop_id, stop_sequence, stop_headsign, pickup_type, pickup_type_text, drop_off_type, drop_off_type_text, shape_dist_traveled))

  database.commit()

################################################################################
############################### Script #########################################
################################################################################

# Use SQLlite3 as the database application progamming interface
import sqlite3 as dbapi

# Write a new database?
writeDB = True

# Time is used to name your DB to avoid overwrites
import time
now = time.strftime("%Y%m%d_%H%M%S", time.localtime())

# Which GTFS? Where is this place?
##GTFSLocation = "G:\\Documents\\WellingtonTransportViewer\\Data\\metlink-archiver_20130712_0326\\" # Unzipped folder
##GTFSLocation = "/media/alphabeta/RESQUILLEUR/Documents/WellingtonTransportViewer/Data/metlink-archiver_20130712_0326_subset/"
GTFSLocation = "/media/alphabeta/RESQUILLEUR/Documents/WellingtonTransportViewer/Data/metlink-archiver_20130712_0326/"
continent = "Oceania"
country = "New Zealand"
city = "Wellington"
##db_str = "GTFSSQL_" + city + "_" + now + "__SUBSET__.db"
db_str = "GTFSSQL_" + city + "_" + now + ".db"
db_pathstr = "/media/alphabeta/RESQUILLEUR/Documents/WellingtonTransportViewer/Data/Databases/" + db_str # Path and name of DB

if writeDB == True:

  # Initialise database and write (empty) tables according to database schema
  GTFSDB = createGTSFtoSQL_database(db_pathstr)

  # Routes (20131104)
  populateRoutes(GTFSLocation, GTFSDB)

  # Agencies (20131104)
  populateAgency(GTFSLocation, GTFSDB, continent, country, city)

  # Calendar (20131104)
  populateCalendar(GTFSLocation, GTFSDB)

  # Calendar dates (exceptions) (20131106)
  populateCalendarDates(GTFSLocation, GTFSDB)

  # Trips (20131106)
  populateTrips(GTFSLocation, GTFSDB)

  # Shapes (20131106)
  populateShapes(GTFSLocation, GTFSDB)

  # Feed publisher (20131106)
  populateFeedInfo(GTFSLocation, GTFSDB)

  # Stops (20131106)
  populateStops(GTFSLocation, GTFSDB)

  # Stop times (20131106)
  populateStopTimes(GTFSLocation, GTFSDB)

  # Amended stop times (20131224)
  populateStopTimesAmended(GTFSDB)

  print "Database written: " + db_str + " (" + db_pathstr + ")"

else:

  print "No database written."

################################################################################
################################ End ###########################################
################################################################################
