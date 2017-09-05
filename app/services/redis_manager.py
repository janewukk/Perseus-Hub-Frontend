import redis, time, thread
from app.models import Dataset

# instantiate redis
r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pubsub()

def handle_process_finished(message):
	"""
	Handling notification when dataset is processed
	
	Arguments:
		message {String} -- Incoming message
	"""
	print message['data']

def check_redis_messages():
	while True:
		message = p.get_message()

def bootstrap():
	"""
	Boostrap the app with some stuff
	"""
	p.subscribe(**{ 'perseus:process_finished': handle_process_finished })

	try:
		print "Starting thread..."
		thread.start_new_thread(check_redis_messages, ())
	except Exception as e:
		print e
		print "Error: Cannot start pubsub thread"


