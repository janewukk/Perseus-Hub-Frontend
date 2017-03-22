from __future__ import unicode_literals

# base model class
from django.db import models
# just in case we need to customize user
from django.contrib.auth.models import User as BaseUser

"""
Abstract representation of a site user

Extends:
	models.User
"""
class User(BaseUser):
	class Meta:
		# proxy all available function calls 
		# to the super base user class
		proxy = True

	def datasets(self):
		"""
		Helper method to get user's datasets
		
		Returns:
			RelationObject -- datasets
		"""
		return self.dataset_set

	def bookmarks(self):
		"""
		Helper method to get user's bookmarks
		
		Returns:
			RelationObject -- bookmarks
		"""
		return self.bookmark_set

"""
Abstract representation of a dataset 
that will be processed by Spark

Extends:
	models.Model
"""
class Dataset(models.Model):
	# the user who uploads this dataset
	uploader = models.ForeignKey(User, on_delete = models.CASCADE)

"""
Properties associated with specific datasets

Extends:
	models.Model
"""
class Property(models.Model):
	# dataset that this property belongs to
	dataset = models.ForeignKey(Dataset, on_delete = models.CASCADE)

"""
Bookmark user can make on properties/datasets

Extends:
	models.Model
"""
class Bookmark(models.Model):
	# bookmark's creator (User)
	creator = models.ForeignKey(User, on_delete = models.CASCADE)
	# bookmark's associated dataset property
	associated_property = models.OneToOneField(Property, on_delete = models.CASCADE)
	# a numerical reporesentation of this bookmark, assigned by user
	priority = models.IntegerField()
