from http.server import BaseHTTPRequestHandler
from cowpy import cow

try:
	import urlparse
except ImportError:
	import urllib.parse as urlparse

class handler(BaseHTTPRequestHandler):
	
	def do_GET(self):
		parsed_path = urlparse.urlparse(self.path)

		# message_parts = [
		# 		'CLIENT VALUES:',
		# 		'client_address=%s (%s)' % (self.client_address,
		# 									self.address_string()),
		# 		'command=%s' % self.command,
		# 		'path=%s' % self.path,
		# 		'real path=%s' % parsed_path.path,
		# 		'query=%s' % parsed_path.query,
		# 		'params=%s' % parsed_path.params,
		# 		'request_version=%s' % self.request_version,
		# 		'',
		# 		'SERVER VALUES:',
		# 		'server_version=%s' % self.server_version,
		# 		'sys_version=%s' % self.sys_version,
		# 		'protocol_version=%s' % self.protocol_version,
		# 		'',
		# 		'HEADERS RECEIVED:',
		# 		]
		# for name, value in sorted(self.headers.items()):
		# 	message_parts.append('%s=%s' % (name, value.rstrip()))
		# message_parts.append('')
		# message = '\r\n'.join(message_parts)


		self.send_response(200)
		self.end_headers()

		query = urlparse.parse_qs(parsed_path.query)
		print(query)

		message = 'MMMMMMMOOOOOOOOOOOOOrzão! <3'
		if "message" in query:
			message = str(query['message'][0])
			print(message)
		
		message = cow.Cowacter().milk(message)
		self.wfile.write(message.encode('utf8'))
		return

# if __name__ == '__main__':
# 	from http.server import BaseHTTPRequestHandler, HTTPServer
# 	server = HTTPServer(('localhost', 8080), GetHandler)
# 	print('Starting server, use <Ctrl-C> to stop')
# 	server.serve_forever()