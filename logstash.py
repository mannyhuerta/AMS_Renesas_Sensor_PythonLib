import httplib, json


def send_event(room, sensor, data):
	try:
		logstash = httplib.HTTPConnection('shitbox.org', 8080)
		headers = {"Content-Type":"application/json"}
		logstash.request("PUT", '/{0}/{1}'.format(room, sensor), json.dumps(data)) 
		logstash.close()
	except:
		print "Unable to connect to logstash."
	

