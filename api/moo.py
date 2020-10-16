from cowpy import cow

from flask import Flask, Response, request, json
app = Flask(__name__)

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')

@app.route('/')
def hello():
	response = app.response_class(
		response="Hello World!",
		status=200,
		mimetype='text'
	)
	return response

# @app.route('/<path>')
@app.route('/<path>',methods=["GET","POST"])

def catch_all(path):
	user_message = request.args.get('message', type = str)
	print(user_message)
	if user_message:
		ans = cow.Cowacter().milk(user_message)
	else:
		ans = cow.Cowacter().milk(path)
	response = app.response_class(
		response=json.dumps(ans),
		status=200,
		mimetype='application/json'
	)
	return response

if __name__ == '__main__':
	app.debug = True
	app.run()