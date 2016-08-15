from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
from src.view.movieView import movieView
import udpConversation_pb2 as udpCon
import uuid

PORT_NUMBER = 60001


#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests


	def do_GET(self):
		def bail(a):
			return "Nothing", "Nothing" 
		a = movieView()
		if self.path=="/":
			self.path="/index.html"

		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			code = 200
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True
			if sendReply == True:
				f = open(curdir + sep + self.path)
				senddata = f.read()
				f.close()
			if self.path.__contains__("cmd"):
				mimetype='application/json'
				sendReply = True
				it = self.path.split("?")
				code = 400
				if len(it) == 2:
					c = it[1].split("=")
					if len(c) == 2:
						cmd = c[0]
						data = c[1]
						get_functions = {'find_by_genre': a.perform_find_genre, 'find_by_director':
		                      a.perform_find_director, 
		                     'find_by_actor': a.perform_find_actor, 
		                     'list_movies': a.perform_list,  
		                     'get_movie': a.perform_get_movie}
		        		op, action = get_functions.get(cmd, bail)(data)
		        		code = 200
		        	else:
		        		op, action = "Invalid cmd", "Invalid cmd"
		        else:
		        	op, action = "Invalid URL", "Invalid URL"
		        res = udpCon.Response()
		        res.id = str(uuid.uuid4()) + "-response"
		        res.data = op
		        res.result = action
		        senddata = res.SerializeToString()


			if sendReply == True:
				#Open the static file requested and send it 
				self.send_response(code)
				self.send_header('Content-type', mimetype)
				self.end_headers()
				self.wfile.write(senddata)
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	#Handler for the POST requests
	def do_POST(self):
		if self.path == "/cmd":
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'application/text':
				length = int(self.headers.getheader('content-length'))
				dat = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
				print "record %s is added successfully" % recordID
			else:
				data = ""
	        	req = udpCon.Request()
	        	req.ParseFromString(dat)
	        	cmd = req.cmd
	        	data = req.data
	        	post_functions = {'add': a.perform_add_pro, 'update': a.perform_update_pro, 'delete': a.perform_delete}
			op, action = post_functions.get(cmd, bail)(data)
			res = udpCon.Response()
			res.id = req.id + "-response"
			res.data = op
			res.result = action
			senddata = res.SerializeToString()
			self.send_response(200)
			self.end_headers()
			self.wfile.write(senddata)
		return			
			
			
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
