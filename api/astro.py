from http.server import BaseHTTPRequestHandler

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

date = Datetime('1929/01/15', '12:00', '-06:00')
pos = GeoPos('33n45:01', '84w23:01')

chart = Chart(date, pos)

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


