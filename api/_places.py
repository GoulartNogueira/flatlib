from http.server import BaseHTTPRequestHandler
import urllib.parse
	
import json
import numpy as np

import logging

from geopy.geocoders import Nominatim


def get_location(Location_name):
	geolocator = Nominatim(user_agent="AstroMBTI")
	print(geolocator)
	#print(person,people[person]["Location"])
	try:
		location = geolocator.geocode(Location_name)
		#print(location.raw)
	except:
		print("Error in",Location_name)
		return()
	url = "https://www.google.com.br/maps/@"+str(location.latitude)+","+str(location.longitude)+",13z"
	return([location.latitude,location.longitude,url,location.raw])
	# elif "lat" in location and 'lon' in location:
	# 	return([location.lat,location.lon,location.raw])
	# else:
	# 	return(location.raw)


class handler(BaseHTTPRequestHandler):
	def __init__(self, *args, **kwargs):
		super(handler, self).__init__(*args, **kwargs)	
	def do_GET(self):
		parsed_path = urllib.parse.urlparse(self.path)
		query = urllib.parse.parse_qs(parsed_path.query)
		if 'placename' in query:
			placename = query['placename'][0]
			print(placename)
			latlong = get_location(placename)
			print(str(latlong))
			if isinstance(latlong, (list,)) and len(latlong) >= 2:
				latlong = list(latlong)
			else:
				print("Error on getting location.")
		answer = {
			"query":query,
			"result":latlong,
			}
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.send_header("Access-Control-Allow-Origin", "*")
		self.end_headers()
		self.wfile.write(json.dumps(answer,ensure_ascii=False).encode('utf8'))
		return

if __name__ == '__main__':
	from http.server import BaseHTTPRequestHandler, HTTPServer
	server = HTTPServer(('localhost', 8080), handler)
	print('Serving on http://localhost:8080')
	print('Example: http://localhost:8080/?datetime=1990-May-21%2008:00PM&timezone=-2:00&latlong=-50.00,30.01')
	print('Starting server, use <Ctrl-C> to stop')
	server.serve_forever()