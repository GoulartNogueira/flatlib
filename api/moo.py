from cowpy import cow

from flask import Flask, Response, request
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')

def catch_all(path):
	user_message = request.args.get('message', default = 'Mooooooo', type = str)
	ans = cow.Cowacter().milk(user_message)
	return Response(ans, mimetype="text")