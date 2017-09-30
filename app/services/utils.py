import sys
import time
import calendar
import pandas as pd
from datetime import datetime
from django.contrib import messages
from web.settings import MEDIA_ROOT

"""
Flash a one-time short message to session
"""
def flash_session_message(request, status, message):
	# convert status to message tag level
	if status == 'success':
		message_level = messages.SUCCESS
	elif status == 'error':
		message_level = messages.ERROR
	elif status == 'warning':
		message_level = messages.WARNING
	else:
		message_level = messages.INFO

	# add message to session
	messages.add_message(request, message_level, message)

"""
Define the custom user upload directory
"""
def user_upload_dir(dataset, filename):
	return 'data/uploads/user_{0}/{1}'.format(dataset.uploader.id, \
		str(time.time()) + filename)

"""
Define the custom user processed file directory
"""
def user_processed_dir(dataset, filename):
	return 'data/processed/user_{0}/{1}'.format(dataset.uploader.id, \
		str(time.time()) + filename)

"""
Helper to load the absolute file path
"""
def absolute_path(app_path):
	return MEDIA_ROOT + app_path

"""
Convert datetime object to unix UTC timestamp
"""
def timestamp(dt):
	return str(calendar.timegm(dt.utctimetuple()))

"""
Redis key name for dataset cache
"""
def dataset_cache_keys(dataset):
	ts = timestamp(dataset.updated_at)
	return {
		'graph' : ts + '_' + str(dataset.id) + '_' + 'html',
		'script' : ts + '_' + str(dataset.id) + '_' + 'script'
	}


"""
Generate SQL statements for edges to import
"""
def create_edges_sql(edges_input_filename, edges_sql_filename):
	data = pd.read_csv(edges_input_filename, sep='\t', skipinitialspace=True, escapechar="\\", header=None)

	edges_sql = open(edges_sql_filename, 'w')
		
	edges_sql.write("INSERT INTO app_edge (fromNode, toNode, weight, dataset_id) VALUES")
	
	for (fromNode, toNode, weight, dataset_id) in zip(data[0], data[1], data[2], data[3]):
		
		insert_string = "(" + str(fromNode) + "," + str(toNode) + "," + str(weight) + "," + str(dataset_id) + "),\n"
		edges_sql.write(insert_string)
	
	edges_sql.seek(-2, os.SEEK_CUR)
	edges_sql.write(";")
	edges_sql.close()

"""
Generate SQL statements for nodes to import
"""
def create_data_sql(data_input_filename, data_sql_filename):
	data = pd.read_csv(data_input_filename, sep=',', skipinitialspace=True, escapechar="\\", header=None, dtype=str)

	data_sql = open(data_sql_filename, 'w')
	
	columnNames = """(nodeid, degree, count, pagerank, pagerank_t, pagerank_t_count, clustering_coefficient,
					clustering_coefficient_t, clustering_coefficient_t_count, v_1, v_2, v_3, v_4, v_5, v_6,
					v_7, v_8, v_9, v_10, v_1_t, v_2_t, v_3_t, v_4_t, v_5_t, v_6_t, v_7_t, v_8_t, v_9_t,
					v_10_t, dataset_id)"""
					
	data_sql.write("INSERT INTO app_node " + columnNames + " VALUES ");
	
	arr = [] * 30
	source = zip(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],
					data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15],
					data[16], data[17], data[18], data[19],data[20], data[21], data[22], data[23],
					data[24], data[25], data[26], data[27], data[28], data[29])
				
	for arr in source:
		vals = "("
		vals += ",".join(arr)
		vals += "),\n"
		data_sql.write(vals)
	
	data_sql.seek(-2, os.SEEK_CUR)
	data_sql.write(";")
	
	data_sql.close()