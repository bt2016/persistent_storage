import pymongo
import datetime
from data import computer_action_sample0, computer_action_sample1, computer_action_sample2, computer_action_sample3, computer_action_sample4

uri = 'mongodb://dbUser:X574@ds045031.mongolab.com:45031/x574t'

# This class wraps very basic mongodb operations such as
# build/close connection, connection Status, basic insert/query
class MongoDBInstance:
	def __init__(self, uri):
		self.MONGODB_URI = uri
		self.client = None
		self.db = None

	def connect(self):
		print "Connecting..."
		try:
			self.client = pymongo.MongoClient(self.MONGODB_URI);
			print "Connection established"
		except Exception, e:
			print "Connection failed"
			raise e

	def closeConnection(self):
		print "CLosing connection..."
		self.client.close()
		print "Connection closed"

	# Print False if there has been an error communicating with the server, else True
	def isAlive(self):
		print self.client.alive()

	# Current connected host
	def getHostName(self):
		host = self.client.host
		print host

	# Current connected port
	def getPortNumber(self):
		port = self.client.port
		print port

	# Get default database in that instance
	def getDefaultDatabase(self):
		self.db = self.client.get_default_database()
		return self.db

	# Return current database
	def getCurrentDatabase(self):
		print self.db
		return self.db

	# Print all collections(kind of like table in a sql db) in current database
	def getAllCollections(self):
		allCollections = self.db.collection_names(include_system_collections = False)
		print allCollections
		return allCollections

	# Insert JSON style data in to a specific collection
	def insertIntoCollection(self, collection_name, json_data):
		collection = self.db[collection_name]
		collection.insert(json_data)
		return collection;

	# Prints a single document in a collection (or None if there is no such collection)
	def findAny(self, collection_name):
		collection = self.db[collection_name]
		result = collection.find_one();
		print result
		return result

	# Prints all documents matching a query (or None if there are no matches)
	def queryWithCondition(self, collection_name, condition):
		collection = self.db[collection_name]
		result = []
		for post in collection.find(condition):
			print post
			result.append(post)
		return result

    # Prints all documents in a collection (or None if there is no such collection)
	def findAll(self, collection_name):
		collection = self.db[collection_name]
		result = []
		for post in collection.find():
			print post
			result.append(post)
		# return query results as a list
		return result

	def queryCAbyTimeFrame(self, time):
		collection = self.db['Computer_Actions']
		result = []
		for post in collection.find({"Computer_Log.TIMEFRAME": time}):
			print post
			result.append(post)
		return result

	def queryCAStartFromTimeFrame(self, time):
		collection = self.db['Computer_Actions']
		result = []
		for post in collection.find({"Computer_Log.TIMEFRAME": {"$gt": time}}):
			print post
			result.append(post)
		return result

	def queryCAbyUser(self, user_name):
		collection = self.db['Computer_Actions']
		result = []
		for post in collection.find({"Computer_Log.USERID": user_name}):
			print post
			result.append(post)
		return result

	# GET CL/USERID/TIMEFRAME/HOUSEID/
	def query_USERID_TIMEFRAME_HOUSEID(self, userID, timeframe, houseID):
		collection = self.db['Computer_Actions']
		result = []
		for post in collection.find({"Computer_Log.USERID": userID, "Computer_Log.TIMEFRAME": timeframe, "Computer_Log.HOUSEID": houseID}):
			print post
			result.append(post)
		return result

	# GET CL/USERID/TIMEFRAME/HOUSEID/ROOMID
	def query_USERID_TIMEFRAME_HOUSEID_ROOMID(self, userID, timeframe, houseID, roomID):
		collection = self.db['Computer_Actions']
		result = []
		for post in collection.find({"Computer_Log.USERID": userID, "Computer_Log.TIMEFRAME": timeframe, "Computer_Log.HOUSEID": houseID, 
										"Computer_Log.ROOM.ROOMID": roomID}, 
										{"Computer_Log.USERID": 1, "Computer_Log.TIMEFRAME": 1, "Computer_Log.HOUSEID": 1, "Computer_Log.ROOM.$": 1}
									):
			print post
			result.append(post)
		return result

	# GET CT/USERID/TIMEFRAME/DEVICETYPE/HOUSEID/
	def query_USERID_TIMEFRAME_DEVICETYPE_HOUSEID(self, userID, timeframe, deviceType, houseID):
		collection = self.db['Computer_Actions']
		result = collection.aggregate(
			[{	"$match": {
				"Computer_Log.USERID": userID, "Computer_Log.TIMEFRAME": timeframe, "Computer_Log.HOUSEID": houseID, 
										"Computer_Log.ROOM.DEVICE.DEVICETYPE": deviceType}
			},
			{   "$unwind": "$Computer_Log.ROOM" },
			{   "$unwind": "$Computer_Log.ROOM.DEVICE" },
			{	"$match": {
							"Computer_Log.ROOM.DEVICE.DEVICETYPE": deviceType}
			}
			]
			)
		print result
		return result

	# GET CT/USERID/TIMEFRAME/DEVICETYPE/HOUSEID/ROOMID
	def query_USERID_TIMEFRAME_DEVICETYPE_HOUSEID_ROOMID(self, userID, timeframe, deviceType, houseID, roomID):
		collection = self.db['Computer_Actions']
		result = collection.aggregate(
			[{	"$match": {
				"Computer_Log.USERID": userID, "Computer_Log.TIMEFRAME": timeframe, "Computer_Log.HOUSEID": houseID, 
										"Computer_Log.ROOM.ROOMID": roomID,
										"Computer_Log.ROOM.DEVICE.DEVICETYPE": deviceType
										}
			},
			{   "$unwind": "$Computer_Log.ROOM" },
			{	"$match": {
							"Computer_Log.ROOM.ROOMID": roomID}
			},
			{   "$unwind": "$Computer_Log.ROOM.DEVICE" },
			{	"$match": {
							"Computer_Log.ROOM.DEVICE.DEVICETYPE": deviceType}
			}
			]
			)
		print result
		return result

	# GET CI/USERID/TIMEFRAME/DEVICEID/HOUSEID/
	def query_USERID_TIMEFRAME_DEVICEID_HOUSEID(self, userID, timeframe, deviceID, houseID):
		collection = self.db['Computer_Actions']
		result = collection.aggregate(
			[{	"$match": {
				"Computer_Log.USERID": userID, "Computer_Log.TIMEFRAME": timeframe, "Computer_Log.HOUSEID": houseID,
										"Computer_Log.ROOM.DEVICE.DEVICEID": deviceID}
			},
			{   "$unwind": "$Computer_Log.ROOM" },
			{   "$unwind": "$Computer_Log.ROOM.DEVICE" },
			{	"$match": {
							"Computer_Log.ROOM.DEVICE.DEVICEID": deviceID}
			}
			]
			)
		print result
		return result

	# GET CI/USERID/TIMEFRAME/DEVICEID/HOUSEID/ROOMID
	def query_USERID_TIMEFRAME_DEVICEID_HOUSEID_ROOMID(self, userID, timeframe, deviceID, houseID, roomID):
		collection = self.db['Computer_Actions']
		result = collection.aggregate(
			[{	"$match": {
				"Computer_Log.USERID": userID, "Computer_Log.TIMEFRAME": timeframe, "Computer_Log.HOUSEID": houseID,
										"Computer_Log.ROOM.ROOMID": roomID,
										"Computer_Log.ROOM.DEVICE.DEVICEID": deviceID}
			},
			{   "$unwind": "$Computer_Log.ROOM" },
			{	"$match": {
							"Computer_Log.ROOM.ROOMID": roomID}
			},
			{   "$unwind": "$Computer_Log.ROOM.DEVICE" },
			{	"$match": {
							"Computer_Log.ROOM.DEVICE.DEVICEID": deviceID}
			}
			]
			)
		print result
		return result

	# Delete a collection
	def dropCollection(self, collection_name):
		self.db.drop_collection(collection_name)

	# Reset, delete all collections you have
	def resetDatabase(self):
		allCollections = self.getAllCollections();
		for collection_name in allCollections:
			if not 'system' in collection_name:
				print 'delete: ' + collection_name
				self.dropCollection(collection_name)

if __name__ == '__main__':
    mongo = MongoDBInstance(uri)
    mongo.connect()
    mongo.getHostName();
    # get a db from this instance
    # note that this database currently have two collections: newCollection and test_database
    mongo.getDefaultDatabase()
    print "current database:"
    mongo.getCurrentDatabase()
    print "all collections in the database:"
    mongo.getAllCollections()
    # insert
    # mongo.insertIntoCollection("Computer_Actions", computer_action_sample0)
    # mongo.insertIntoCollection("Computer_Actions", computer_action_sample1)
    # mongo.insertIntoCollection("Computer_Actions", computer_action_sample2)
    # mongo.insertIntoCollection("Computer_Actions", computer_action_sample3)
    # mongo.insertIntoCollection("Computer_Actions", computer_action_sample4)

#******************************************
# Some naive query that is not included
# in spec so far
#******************************************
    # All entries in collection
    # mongo.findAll("Computer_Actions")

    # # Query by time frame
    # time = datetime.datetime(2015, 2, 20, 10, 17, 13)
    # mongo.queryCAbyTimeFrame(time)
    # print ""
    # mongo.queryCAStartFromTimeFrame(time)

    # # Query by user
    # query_user = "Harry"
    # mongo.queryCAbyUser(query_user)
    # print ""

#******************************************
# These functions correspond to C tag in
# 4.0 Requests for Accessing Log Files
#******************************************

    # GET CL/USERID/TIMEFRAME/HOUSEID/
    time = datetime.datetime(2014, 11, 14, 9, 46, 2)
    mongo.query_USERID_TIMEFRAME_HOUSEID("Rick", time, "001")
    print ""

    # GET CL/USERID/TIMEFRAME/HOUSEID/ROOMID/
    time = datetime.datetime(2014, 11, 14, 9, 46, 2)
    mongo.query_USERID_TIMEFRAME_HOUSEID_ROOMID("Rick", time, "001", "004")
    print ""

    # GET CT/USERID/TIMEFRAME/DEVICETYPE/HOUSEID/
    time = datetime.datetime(2014, 11, 20, 14, 25, 20)
    mongo.query_USERID_TIMEFRAME_DEVICETYPE_HOUSEID("Jack", time, "Light", "001")
    print ""

    # GET CT/USERID/TIMEFRAME/DEVICETYPE/HOUSEID/ROOMID
    time = datetime.datetime(2014, 11, 14, 9, 46, 2)
    mongo.query_USERID_TIMEFRAME_DEVICETYPE_HOUSEID_ROOMID("Rick", time, "Light", "001", "003")
    print ""

    # GET CI/USERID/TIMEFRAME/DEVICEID/HOUSEID/
    time = datetime.datetime(2014, 11, 14, 9, 46, 2)
    mongo.query_USERID_TIMEFRAME_DEVICEID_HOUSEID("Rick", time, "403", "001")
    print ""

    # GET CI/USERID/TIMEFRAME/DEVICEID/HOUSEID/ROOMID
    time = datetime.datetime(2014, 11, 14, 9, 46, 2)
    mongo.query_USERID_TIMEFRAME_DEVICEID_HOUSEID_ROOMID("Rick", time, "201", "001", "004")
    print ""

    # Drop a specific collection
    # mongo.dropCollection("Computer_Actions")
    # Drop all collections in the database
    # mongo.resetDatabase()
