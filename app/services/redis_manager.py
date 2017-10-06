import redis, time, thread
from app.models import Dataset
from app.services.notification_handlers import process_finished, test_popen, test_receive

# instantiate redis
r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pubsub()

def check_redis_messages():
	"""
	Read message from redis subscription
	"""
	while True:
		message = p.get_message()
		time.sleep(0.01)

def bootstrap():
	"""
	Boostrap the redis listener
	"""
	p.subscribe(**{ 
		'perseus:process_finished': process_finished,
		'test:popen': test_popen,
		'test:receive': test_receive
	})

	try:
		print "Starting redis listener thread..."
		thread.start_new_thread(check_redis_messages, ())
	except Exception as e:
		print e
		print "Error: Cannot start pubsub thread"


