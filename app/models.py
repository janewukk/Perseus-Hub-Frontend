from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User as BaseUser

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
	raw_data = models.FileField(upload_to='uploads/datasets/', default = "")
	# dataset's analyzed json file name
	analyzed_json_filename = models.CharField(max_length = 256, default = "")
	# the user who uploads this dataset
	uploader = models.ForeignKey(User, on_delete = models.CASCADE)
	# timestamps
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

"""
Bookmark user can make on a specific node of a dataset

Extends:
	models.Model
"""
class Bookmark(models.Model):
	# bookmark's creator (User)
	creator = models.ForeignKey(User, on_delete = models.CASCADE)
	# bookmark's associated dataset node
	# associated_node = models.OneToOneField(Node, on_delete = models.CASCADE)
	# a numerical representation of this bookmark's color, assigned by user
	priority = models.IntegerField()
