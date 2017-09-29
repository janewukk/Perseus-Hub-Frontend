import json
from app.services import email 
from app.models import User, Dataset

def process_finished(message):
	"""
	Handling notification when dataset is processed
	
	Arguments:
		message {Dict} -- Incoming message
	"""
	print message['data']
	
	# TODO: Deal with the incoming data
	# data = json.loads(message['data'])
	# dataset = Dataset.objects.get(id = data['dataset_id'])
	# user = User.objects.get(id = data['user_id'])
	# 
	# TODO: Modify dataset
	# dataset.processed = True
	# ...
	# dataset.save()
	# 
	# TODO: Send email
	# email.send('admin@perseus.com', user.email, 'Your dataset has finished processing!', html="....")
	