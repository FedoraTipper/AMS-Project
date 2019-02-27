from tornado.web import RequestHandler

class SetDefaultHeaders(RequestHandler):
	def set_default_headers(self):	
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Expose-Headers", "Authorization")
		self.set_header("Access-Control-Allow-Methods", "POST, GET, PUT, DELETE, OPTIONS")
		self.set_header("Access-Control-Allow-Headers", "Authorization, Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, Access-Control-Expose-Headers, Access-Control-Allow-Methods")
	
	# def check_origin(self, origin):
		# return True

	def options(self):
		self.set_status(204)
		self.finish()