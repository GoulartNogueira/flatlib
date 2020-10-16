from cowpy import cow

from flask import Flask, Response, request
app = Flask(__name__)

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/<path>')
@app.route('/<path>',methods=["POST"])

def catch_all(path):
	user_message = request.args.get('message', type = str)
	print(user_message)
	if user_message:
		ans = cow.Cowacter().milk(user_message)
	else:
		ans = cow.Cowacter().milk(path)
	return Response(ans, mimetype="text")

if __name__ == '__main__':
    app.run()