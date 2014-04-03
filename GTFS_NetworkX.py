import networkx as nx
from AB_Class import *

class DTI_GTFSGraph(object):
    '''
    A Deterministic, Time-Invariant graph built from a GTFS feed and served
    fresh to you as a NetworkX graph.
    '''
    def __init__(self, AB_Database, date=None, subset={}):
        '''
        AB_Database: A Database object from AB_Class
        subset: A dictionary that restricts the elements of the GTFS to be
                taken into the NetworkX Graph object. A 'limit to'.
                Must be of the following form (with example values):
                {'mode': ['bus'], # Restricts the GTFS to just buses
                'routes', ['001', '002', 'HVL'], # Restricts to these routes
                'DOW', ['Monday']} # Restricts to just Monday
                These are combined for maximum restrictiveness; 
                that is, in the given example, the 'Bus' limit will mean
                that the 'HVL' (a train route) is not included in the result.
                Each element is optional; and the entire parameter is optional,
                if no limit is required.
                
        date: A datetime.datetime object that allows you to account for an
              exact date in a calendar year.
              Example: datetime.datetime(2013, 12, 7)
        '''
        self.database = AB_Database
        if date is not None:
            self.date = Day(self.database.database, date)
        else:
            self.date = date
        self.subset = subset
        self.nxgraph = self.buildSubsetGraph()
        
    def buildSubsetGraph(self, verbose=True):
        '''
        Using self.subset, applies the requested restritions and returns
        a directed and weighted NetworkX Graph.
        
        date: An optional AB_Class Day object that allows you to account for
              special exceptions to the usual schedule on an exact data, such
              as Christmas day. If None, this check is not performed and an
              ordinary [DOW] is assumed.
        '''
        # Apply day of week subset as it does the most work
        try:
            if verbose: print("DOW subset: %s" % self.subset['DOW'][0])
            q = Template('SELECT DISTINCT stop_times_amended.trip_id, trips.route_id, routes.route_type_desc FROM stop_times_amended INNER JOIN trips ON stop_times_amended.trip_id=trips.trip_id INNER JOIN routes ON trips.route_id=routes.route_id WHERE stop_times_amended.$DOW = 1')
            query = q.substitute(DOW = self.subset['DOW'][0].lower())
        except KeyError:
            # No subset to apply
            # Get ALL trips
            query = 'SELECT DISTINCT stop_times_amended.trip_id, trips.route_id, routes.route_type_desc FROM stop_times_amended INNER JOIN trips ON stop_times_amended.trip_id=trips.trip_id INNER JOIN routes ON trips.route_id=routes.route_id'
        self.database.cur.execute(query)
        if verbose: print(query)
        subsettrips = self.database.cur.fetchall()
        if verbose: print("There are %i trips after DOW subset." % len(subsettrips))
        subsettrips = [trip for trip in subsettrips]
        # Apply route subset
        try:
            if verbose: print(self.subset['routes'])
            subsettrips = [trip for trip in subsettrips if trip[1] in self.subset['routes']]
        except KeyError:
            # No subset to apply
            pass
        if verbose: print("There are %i trips after route subset." % len(subsettrips))
        # Apply mode subset
        try:
            if verbose: print(self.subset['mode'])
            subsettrips = [trip for trip in subsettrips if trip[2] in self.subset['mode']]
        except KeyError:
            # No subset to apply
            pass
        if verbose: print("There are %i trips after mode subset." % len(subsettrips))
        if self.date is not None:
            # Do a final subset
            subsettrips = [PTTrip(self.database.database, trip[0], self.date) for trip in subsettrips]
            if verbose: print("There are %i trips after calendar_dates check." % len(subsettrips))

       
if __name__ == '__main__':
    # Prepare database and Database object, using AB_Class
    db_str = "Saturday/GTFSSQL_Wellington_20140402_210506.db"
    db_pathstr = "/media/RESQUILLEUR/Documents/WellingtonTransportViewer/Data/Databases/" + db_str
    myDB = dbapi.connect(db_pathstr) # Connect to DB
    myDB.text_factory = dbapi.OptimizedUnicode
    myDatabase = Database(myDB)
    
    # Create Deterministic & Time-Invariant Graph with subset
    DTIg = DTI_GTFSGraph(myDatabase, date=None, subset={'routes': ['WBAO091I', 'WBAO091O', 'WRAJVL1O', 'WRAJVL1I'], 'DOW': ['Saturday'], 'mode': ['Bus', 'Rail']})
    DTIg.nxgraph

