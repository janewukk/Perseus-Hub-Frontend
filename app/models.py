from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User as BaseUser

from app.services.utils import user_upload_dir, user_processed_dir

"""
Abstract representation of a site user

Extends:
	models.User
"""
class User(BaseUser):
	class Meta:
		# map all available function calls 
		# to the super base user class
		proxy = True

	def datasets(self):
		"""
		Helper method to get user's datasets
		
		Returns:
			QuerySet -- datasets
		"""
		return self.dataset_set

	def bookmarks(self):
		"""
		Helper method to get user's bookmarks
		
		Returns:
			QuerySet -- bookmarks
		"""
		return self.bookmark_set

"""
Abstract representation of a dataset 
that will be processed by Spark

Extends:
	models.Model
"""
class Dataset(models.Model):
	# whether this dataset should be publicize
	publicized = models.BooleanField(default = False)
	# whether this dataset has finished processing
	processed = models.BooleanField(default = False)
	# title for this dataset
	title = models.CharField(max_length = 256, default = "")
	# dataset's raw file field
	raw_data_file = models.FileField(upload_to=user_upload_dir, default = "")
	# dataset's analyzed file
	analyzed_fulldata_file = models.FileField(upload_to=user_processed_dir, default = "")
	# dataset's graph data file
	analyzed_graph_file = models.FileField(upload_to=user_processed_dir, default = "")
	# dataset's combined scores file path
	combined_scores_files = models.CharField(max_length = 512, default = "")
	# the user who uploads this dataset
	uploader = models.ForeignKey(User, on_delete = models.CASCADE, default =1)
	# marked as delete
	trashed = models.BooleanField(default = False)
	# timestamps
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	def nodes(self):
		"""Helper to fetch all nodes belong to this dataset
		Returns:
			QuerySet -- Collection of Node models
		"""
		return self.node_set

	def edges(self):
		"""Helper to fetch all edges belong to this dataset
		Returns:
			QuerySet -- Collection of Edge models
		"""
		return self.edge_set

"""
Bookmark user can make on a specific node of a dataset

Extends:
	models.Model
"""
class Bookmark(models.Model):
	# bookmark's creator (User)
	creator = models.ForeignKey(User, on_delete = models.CASCADE)
	# a numerical representation of this bookmark's color, assigned by user
	priority = models.IntegerField()
	# x coordinate the bookmark refers to
	x_coord = models.CharField(max_length = 256, default = "")
	# y coordinate the bookmrk refers to
	y_coord = models.CharField(max_length = 256, default = "")
	# name of the properties that this bookmark refers to
	prop = models.CharField(max_length = 1024, default = "")
	# notes attached
	note = models.CharField(max_length = 2048, default = "")
	# id of the node that is marked
	node_id = models.IntegerField()
	# dataset that this bookmark resides on
	dataset = models.ForeignKey(Dataset, on_delete = models.CASCADE)
	# whether this bookmark should be publicize
	publicized = models.BooleanField(default = False)
	# timestamps
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

"""
Graph node
"""
class Node(models.Model):
	nodeid = models.CharField(default= 0, max_length=30, db_index=True)
	degree = models.CharField(default= 0, max_length=30, db_index=True)
	count = models.CharField(default= 0, max_length=30, db_index=True)
	pagerank = models.FloatField(default= 0, db_index=True)
	pagerank_t = models.FloatField(default= 0, db_index=True)
	pagerank_t_count = models.FloatField(default= 0, db_index=True)
	clustering_coefficient = models.FloatField(default= 0, db_index=True)
	clustering_coefficient_t = models.FloatField(default= 0, db_index=True)
	clustering_coefficient_t_count = models.FloatField(default= 0, db_index=True)
	v_1 = models.FloatField(default= 0, db_index=True)
	v_2 = models.FloatField(default= 0, db_index=True)
	v_3 = models.FloatField(default= 0, db_index=True)
	v_4 = models.FloatField(default= 0, db_index=True)
	v_5 = models.FloatField(default= 0, db_index=True)
	v_6 = models.FloatField(default= 0, db_index=True)
	v_7 = models.FloatField(default= 0, db_index=True)
	v_8 = models.FloatField(default= 0, db_index=True)
	v_9 = models.FloatField(default= 0, db_index=True)
	v_10 = models.FloatField(default= 0, db_index=True)
	v_1_t = models.FloatField(default= 0, db_index=True)
	v_2_t = models.FloatField(default= 0, db_index=True)
	v_3_t = models.FloatField(default= 0, db_index=True)
	v_4_t = models.FloatField(default= 0, db_index=True)
	v_5_t = models.FloatField(default= 0, db_index=True)
	v_6_t = models.FloatField(default= 0, db_index=True)
	v_7_t = models.FloatField(default= 0, db_index=True)
	v_8_t = models.FloatField(default= 0, db_index=True)
	v_9_t = models.FloatField(default= 0, db_index=True)
	v_10_t = models.FloatField(default= 0, db_index=True)

	dataset = models.ForeignKey(Dataset, on_delete = models.CASCADE, default = 1)

"""
Graph edge
"""
class Edge(models.Model):
	fromNode = models.IntegerField(default= 0, db_index=True)
	toNode = models.IntegerField(default= 0, db_index=True)
	weight = models.IntegerField(default= 0, db_index=True)

	dataset = models.ForeignKey(Dataset, on_delete = models.CASCADE, default = 1)