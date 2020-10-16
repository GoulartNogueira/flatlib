from cowpy import cow
from sanic import Sanic
from sanic.response import json, text
app = Sanic(__name__)


@app.route('/')
@app.route('/<path:path>',methods=["GET","POST"])
async def index(request, path=""):
	user_message = request.args.get('message')
	print(user_message)
	if user_message:
		ans = cow.Cowacter().milk(user_message)
	else:
		ans = cow.Cowacter().milk(path)

	if request.args.get('format') == 'json':
		response = json({'cow': ans})
	else:
		response = text(ans)
	return(response)

if __name__ == '__main__':
	app.debug = True
	app.run()