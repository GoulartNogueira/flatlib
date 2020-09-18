from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

from http.server import BaseHTTPRequestHandler
import dateutil.parser
import urllib.parse

	
import json
import numpy as np

import logging

def angle_dif(a,b):
	dif = (b-a+360)%360
	return(dif)


def get_astrological(date,coordinates,timezone=''):
	if isinstance(coordinates, (str,)):
		if "," in coordinates:
			coord = coordinates.split(',')
			coord[0]=coord[0].lstrip()
			coord[1]=coord[1].lstrip()
			# if len(coord[1])>2:
			#	coord[1] = coord[1][:1]+":" +coord[1][2:]
		#		print(coord[1])
	
	elif isinstance(coordinates, (list,)):
		if len(coordinates) != 2:
			return()
		coord = coordinates
	else:
		return()

	pos = GeoPos(coord[0],coord[1])
	
	if timezone == '' or timezone.startswith("m"):
		return()
	#if isinstance(timezone, (str,)):
	#	date = Datetime(date.strftime("%Y/%m/%d"), date.strftime('%H:%M'), timezone)
		timezone = str(get_timezone(pos.lat, pos.lon,date))
		#print(timezone)
		#print(date)
	#else:
		#date += timezone
	date = Datetime(date.strftime("%Y/%m/%d"), date.strftime('%H:%M'), timezone)
	#print(date)
		
	chart = Chart(date, pos)

	astro = {}
	for obj in [chart.get(const.ASC)]:
	#	#print(obj)
		astro[obj.id] = {'sign':obj.sign,'lon':obj.lon}
	
	# for obj in chart.houses:
	# 	astro[obj.id] = {'sign':obj.sign,'lon':obj.lon,'signlon':obj.signlon,'size':30-obj.size}

	for obj in chart.objects: #Planets
		#print(obj.id,obj.sign,obj.lon,obj.signlon,obj.lonspeed)
		astro[obj.id] = {'sign':obj.sign,'lon':obj.lon,'speed':obj.lonspeed}
		try:
			gender = obj.gender()
			astro[obj.id].update({'gender':gender})
		except:
			pass
		try: 
			mean_motion = obj.meanMotion()
			if mean_motion:
				astro[obj.id].update({'speed':obj.lonspeed/mean_motion})
		except: pass
		try: astro[obj.id].update({'fast':str(obj.isFast())})
		except: pass
		for house in chart.houses:
			if house.hasObject(obj):
				astro[obj.id].update({'house':house.id})
	moon_phase = angle_dif(astro['Moon']['lon'],astro['Sun']['lon'])
	astro['Moon'].update({
		'phase':moon_phase,
	})
	ASC_LON = chart.get(const.ASC).lon
	for obj in astro.keys():
		if 'lon' in astro[obj].keys():
			angle = angle_dif(ASC_LON,astro[obj]['lon'])
			astro[obj].update({'lon':angle,'position':[np.sin(angle* np.pi / 180.),np.cos(angle* np.pi / 180.)]})
	return(astro)



def planets_aspects(astrological_data):
	#https://en.wikipedia.org/wiki/Orb_(astrology)
	# ASPECT, ANGLE, Max ORB
	aspects = [
		('Conjunction',0,10),
		('Sextile',60,4),
		('Square',90,10),
		('Trine',120,10),
		('Opposition',180,10),
		('Quincunx',150,3.5),
		('Semi-sextile',30,1.2),
		('Quintile',72,1.2),
		('Semi-Square',45,2),
		
	]
	result = []
	planets = ['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','North Node']#,'South Node']
	p_list = planets
	for planet in planets:
		#print(planet,astrological_data[planet]['lon'])
		if len(p_list):
			p_list = p_list[1:]
		else: continue
		for p in p_list:
			angle = abs(astrological_data[planet]['lon']-astrological_data[p]['lon'])
			if angle > 180: angle = 360 - angle
			#result.update({"aspect "+planet+" X "+p:angle})
			
			if any (aspect_ang-max_orb <= angle <= aspect_ang+max_orb for (aspect, aspect_ang, max_orb) in aspects):
				for (aspect, aspect_ang, max_orb) in aspects:
					if aspect_ang-max_orb <= angle <= aspect_ang+max_orb:
						
						orb = abs(angle-aspect_ang)
						
						#Adicionando um fator de imprecisão:
						plan_speed = astrological_data[planet]['speed'] if 'speed' in astrological_data[planet].keys() else 1
						p_speed = astrological_data[p]['speed'] if 'speed' in astrological_data[p].keys() else 1
						orb += abs(plan_speed - p_speed)*360/24/60*5
						if orb == 0: orb=0.1
						orb = 1/orb
						#Considerando peso de cada fator:
						orb*=max_orb

						result.append( ( [planet,p], aspect, round(orb,4)) )
			else:
						pass
						#result.update({"aspect "+planet+" X "+p:(None,0)})
	
	return(result)


class handler(BaseHTTPRequestHandler):
	def __init__(self, *args, **kwargs):
		super(handler, self).__init__(*args, **kwargs)	
	def do_GET(self):
		parsed_path = urllib.parse.urlparse(self.path)
		query = urllib.parse.parse_qs(parsed_path.query)
		print(query)
		# print(parsed_path)

		#Standard
		datetime_raw = '1991-May-01 08:35AM'
		latlong_raw = [23.6713029,-46.5690634]
		fuso = "-03:00"

		if "datetime" in query:
			datetime_raw = query['datetime'][0]
			print(datetime_raw)
		else:
			print('datetime not found')
		datetime = dateutil.parser.parse(datetime_raw)

		if 'latlong' in query:
			print(query['latlong'])
			try:
				latlong_raw = query['latlong'][0].split(',')
			except:
				print("Oooops, latlong format do not match!")
			latlong = [float(latlong_raw[0]),float(latlong_raw[1])]
		elif ('lat' in query) and ('long' in query):
			lat = query['lat']
			lon = query['long']
			try:
				latlong = [float(lat),float(lon)]
			except:
				print("Oooops, latlong format do not match!")
		else:
			print('lat long not found')
			print("Using",latlong_raw,"as Standard")
			latlong = [float(latlong_raw[0]),float(latlong_raw[1])]

		if "fuso" in query:
			fuso = query['fuso'][0]
			print(fuso)

		print("Getting astrological data for:",datetime,latlong,fuso)
		astro = get_astrological(datetime,latlong,fuso)
		aspect_list = planets_aspects(astro)
		print(aspect_list)
		answer = {"query":query, "planets":astro, "aspects":aspect_list}
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
	print('Starting server, use <Ctrl-C> to stop')
	server.serve_forever()