from http.server import BaseHTTPRequestHandler

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
import json
import numpy as np

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
            #    coord[1] = coord[1][:1]+":" +coord[1][2:]
        #        print(coord[1])
    
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
    #    date = Datetime(date.strftime("%Y/%m/%d"), date.strftime('%H:%M'), timezone)
        timezone = str(get_timezone(pos.lat, pos.lon,date))
        print(timezone)
        #print(date)
    #else:
        #date += timezone
    date = Datetime(date.strftime("%Y/%m/%d"), date.strftime('%H:%M'), timezone)
    #print(date)
    
    
    
    chart = Chart(date, pos)

    astro = {}
    for obj in [chart.get(const.ASC)]:
    #    #print(obj)
        astro[obj.id] = {'sign':obj.sign,'lon':obj.lon}
    
    for obj in chart.houses:
        astro[obj.id] = {'sign':obj.sign,'lon':obj.lon,'signlon':obj.signlon,'size':30-obj.size}

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
        try: astro[obj.id].update({'fast':obj.isFast()})
        except: pass
        for house in chart.houses:
            if house.hasObject(obj):
                astro[obj.id].update({'house':house.id})
    moon_phase = angle_dif(astro['Moon']['lon'],astro['Sun']['lon'])
    astro['Moon'].update({
        'phase':moon_phase,
        'phase_position':(np.sin(moon_phase* np.pi / 180.),np.cos(moon_phase* np.pi / 180.))
    })
    ASC_LON = chart.get(const.ASC).lon
    for obj in astro.keys():
        if 'lon' in astro[obj].keys():
            angle = angle_dif(ASC_LON,astro[obj]['lon'])
            astro[obj].update({'lon':angle,'position':(np.sin(angle* np.pi / 180.),np.cos(angle* np.pi / 180.))})
    return(astro)

import dateutil.parser
x = get_astrological(dateutil.parser.parse('1991-May-01 08:35AM'),[23.6713029,-46.5690634],"-03:00")

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(x.encode())
        return
