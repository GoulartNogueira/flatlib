from http.server import BaseHTTPRequestHandler

from _flatlib import const
from _flatlib.chart import Chart
from _flatlib.datetime import Datetime
from _flatlib.geopos import GeoPos

date = Datetime('1929/01/15', '12:00', '-06:00')
pos = GeoPos('33n45:01', '84w23:01')

chart = Chart(date, pos)
sun = chart.get(const.SUN)
print(chart.get(const.SUN),chart.get(const.MOON),chart.get(const.ASC))

message = []
for obj in chart.objects:
    message.append(obj)

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(message.encode())
        return


