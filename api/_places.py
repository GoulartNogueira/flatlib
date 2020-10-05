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


"""def timezone_offset(lat,lon,dt = None):
	import pytz
	from tzwhere import tzwhere
	# if dt:
	# 	dt = dt.utcnow()
	# 	dt.replace(tzinfo=None)
	print(str(dt))
	tzwhere = tzwhere.tzwhere()
	timezone_str = tzwhere.tzNameAt(lat,lon) # Seville coordinates
	print(timezone_str)
	# local = pytz.timezone(timezone_str)#pytz.timezone ("America/Los_Angeles")
	# print(local)

	tz = pytz.timezone(timezone_str)
	print(tz)
	# tz = pytz.timezone(timezone_str).localize(dt)
	# print(tz)
	utc_offset = dt(tz).utcoffset()
	print(utc_offset)
	return(utc_offset)

	##########################

	offset_seconds = tz.utcoffset(dt).seconds

	offset_hours = offset_seconds / 3600.0

	offset_formated = "{:+d}:{:02d}".format(int(offset_hours), int((offset_hours % 1) * 60))
	return(offset_formated)

	print(tz)
	return(tz)
	naive = dt.replace(tzinfo=tz)
	local_dt = local.localize(naive, is_dst=None)
	#local = pytz.timezone ("America/Los_Angeles")
	#naive = datetime.strptime ("2001-7-3 10:11:12", "%Y-%m-%d %H:%M:%S")
	#local_dt = local.localize(naive, is_dst=None)
	print(pytz.utc.normalize(local_dt))
	#print(pytz.utc.normalize(dt))
	utc_dt = local_dt.astimezone(pytz.utc)
	
	#timezone = pytz.timezone(timezone_str)
	#print(timezone)
	print(utc_dt)
	return(strfdelta(local.utcoffset(dt),"%s%H:%M:%S"))
	#> datetime.timedelta(0, 7200)
"""

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