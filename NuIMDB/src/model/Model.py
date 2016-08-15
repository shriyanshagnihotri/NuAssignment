import bsddb as dbDriver


class Model:
	dbDriverObj = None

	def __init__(self):
		self.dbDriverObj = dbDriver.hashopen('MovieDB.db')


	def read_app(self, appname):
		return self.dbDriverObj.get(appname, None)

	def write_app(self, appname, data):
		self.dbDriverObj[appname] = data
		self.dbDriverObj.sync()
