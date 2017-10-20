import json, os, time, subprocess, multiprocessing as mp
from datetime import datetime
from web.settings import DATABASES
from app.services import email 
from app.models import User, Dataset
from app.services.utils import user_processed_dir, absolute_path, timestamp, create_edges_sql, create_data_sql

def test_popen(message):
	print("received")
	sum = 0
	for i in range(10000000000):
		sum += sum * i * i
	print("after calc")

def test_receive(message):
	print("received: " + message['data'])

def process_finished(message):
	"""
	Handling notification when dataset is has finished processing
	
	Arguments:
		message {Dict} -- Incoming message
	"""

	print("received message... %s" % message['data'])
	
	try:
		start_time = time.time()
		# in form of [userid datasetid dbname graphname edgesname anomallyname...]
		data = message['data'].split(' ')
		
		# Extract data from the message
		dataset = Dataset.objects.get(id = data[1])
		user = User.objects.get(id = data[0])
		
		# Generate node and edges sql file and import
		db = DATABASES['default']

		tmp_nodes_sql_path = absolute_path('data/tmp/') + timestamp(datetime.now()) + "_nodes.sql"
		tmp_edges_sql_path = absolute_path('data/tmp/') + timestamp(datetime.now()) + "_edges.sql"

		########### Multiprocessing, speed up 2x ###########

		def create_nodes():
			create_data_sql(absolute_path(user_processed_dir(dataset, data[2], False)), tmp_nodes_sql_path)
			os.system("mysql -u%s -p%s %s < \"%s\"" % ( db['USER'], db['PASSWORD'], db['NAME'], tmp_nodes_sql_path ))

		def create_edges():
			create_edges_sql(absolute_path(user_processed_dir(dataset, data[4], False)), tmp_edges_sql_path)
			os.system("mysql -u%s -p%s %s < \"%s\"" % ( db['USER'], db['PASSWORD'], db['NAME'], tmp_edges_sql_path ))

		processes = [ mp.Process(target=create_nodes, args=()), mp.Process(target=create_edges, args=()) ]

		for p in processes:
			p.start()

		for p in processes:
			p.join()
			print("Finished one")

		end_time = time.time()

		print("data generation and import took %ss" % str(end_time - start_time))

		########### End multiprocessing #########

		# Modify dataset
		dataset.processed = True
		dataset.analyzed_fulldata_file.name = user_processed_dir(dataset, data[2], False)
		dataset.analyzed_graph_file.name = user_processed_dir(dataset, data[3], False)

		# TODO... anomally
		dataset.save()

		# remove tmp file
		os.remove(tmp_edges_sql_path)
		os.remove(tmp_nodes_sql_path)
		
		# Send email
		email.send('submission@perseushub.com', user.email, 'Your dataset has finished processing!',\
					html = "You can view your dataset result at <a href='http://perseushub.com/datasets/%s'> here </a>" % dataset.id)
	except Exception as e:
		print e.message
	