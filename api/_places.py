"""
requirements.txt:
	geopy==2.0.0
	timezonefinder==4.4.1
"""

from http.server import BaseHTTPRequestHandler
import urllib.parse
	
import json
import numpy as np

import logging

from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

def timezone_offset(lat,lng,date_time):
	tf = TimezoneFinder()
	"""
	returns a location's time zone offset from UTC in minutes.
	"""
	tz_target = pytz.timezone(tf.certain_timezone_at(lng=lng, lat=lat))
	if tz_target is None:
		print("No timezone found in",str((lat,lng)))
		return()
	# ATTENTION: tz_target could be None! handle error case
	#date_time = date_time.tzinfo=None#tzinfo=tz_target)#.utcoffset()
	#print("tzinfo = ",str(date_time.tzinfo))
	dt = date_time
	if dt.tzinfo is None:
		dated_target = tz_target.localize(dt)
		utc = pytz.utc
		dated_utc = utc.localize(dt)
		#return (dated_utc - dated_target).total_seconds() / 60 / 60
		return(strfdelta(dated_utc - dated_target,"%s%H:%M:%S"))
	else:
		print(dt.tzinfo)
		return()


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