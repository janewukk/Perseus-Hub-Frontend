import json, os
from datetime import datetime
from web.settings import DATABASES
from app.services import email 
from app.models import User, Dataset
from app.services.utils import user_processed_dir, absolute_path, timestamp, create_edges_sql, create_data_sql

def process_finished(message):
	"""
	Handling notification when dataset is has finished processing
	
	Arguments:
		message {Dict} -- Incoming message
	"""
	return

	# in form of [userid datasetid dbname graphname edgesname anomallyname...]
	data = message['data'].split(' ')
	
	# Extract data from the message
	dataset = Dataset.objects.get(id = data[1])
	user = User.objects.get(id = data[0])
	
	# Generate node and edges sql file and import
	db = DATABASES['default']

	tmp_nodes_sql_path = absolute_path('data/tmp/') + timestamp(datetime.now()) + "_nodes.sql"
	tmp_edges_sql_path = absolute_path('data/tmp/') + timestamp(datetime.now()) + "_edges.sql"

	create_data_sql(user_processed_dir(dataset, data[2]), tmp_nodes_sql_path)
	create_edges_sql(user_processed_dir(dataset, data[4]), tmp_edges_sql_path)

	os.system("mysql -u %s -p %s %s < %s" % ( db['USER'], db['PASSWORD'], db['NAME'], tmp_nodes_sql_path ))
	os.system("mysql -u %s -p %s %s < %s" % ( db['USER'], db['PASSWORD'], db['NAME'], tmp_edges_sql_path ))

	# Modify dataset
	dataset.processed = True
	dataset.analyzed_fulldata_file.name = user_processed_dir(dataset, data[2])
	dataset.analyzed_graph_file.name = user_processed_dir(dataset, data[3])
	# TODO... anomally
	dataset.save()
	
	# Send email
	email.send('submission@perseushub.com', user.email, 'Your dataset has finished processing!', html="....")
	