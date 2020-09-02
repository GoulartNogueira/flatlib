
from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

date = Datetime('1929/01/15', '12:00', '-06:00')
pos = GeoPos('33n45:01', '84w23:01')

chart = Chart(date, pos)
sun = chart.get(const.SUN)
print(chart.get(const.SUN),chart.get(const.MOON),chart.get(const.ASC))

message = []
for obj in chart.objects:
    message.append(str(obj))
print(str(message).encode())

from cowpy import cow
message = cow.Cowacter().milk('Hello from Python from a Serverless Function!')
print(message.encode())
#self.wfile.write(message.encode())
