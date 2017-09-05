from django.views import View
from django.db.models import F
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin as LoginRequiredResource

from app.models import Dataset, User, Bookmark
from app.services.graph import *
from app.services.utils import flash_session_message, absolute_path

class BookmarkCreateController(LoginRequiredResource, View):
	"""
	Handle the creation of bookmarks
	
	Extends:
		LoginRequiredResource
		View
	"""
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def post(self, request):
		# TODO: Form validation
		# extract attribute
		publicized = False if request.POST['is_publicized'] == "false" else True
		# grab the request data and create dataset
		bookmark = Bookmark(priority = request.POST['priority'], \
							x_coord = request.POST['x_coord'], \
							y_coord = request.POST['y_coord'], \
							prop = request.POST['prop'], \
							dataset = Dataset.objects.get(id = request.POST['dataset_id']),
							creator = request.user
						)
		# save to db
		bookmark.save()

		return JsonResponse({
				'status': "success",
				'message': "Bookmark created successfully!"
			})

class BookmarkValidateController(LoginRequiredResource, View):
	"""
	Handle the check of bookmark existence
	
	Extends:
		LoginRequiredResource
		View
	"""
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def post(self, request):
		# extract request attributes
		x_coord = request.POST['x_coord']
		y_coord = request.POST['y_coord']
		prop = request.POST['prop']
		dataset_id = request.POST['dataset_id']

		# check bookmark existence
		bookmark = request.user.bookmark_set.filter(x_coord=x_coord, y_coord=y_coord, \
													prop=prop, dataset_id=dataset_id)

		if bookmark:
			json = {
				"status": "success",
				"message": "Bookmark exists!",
				"data": {
					'exists': True
				}
			}
		else:
			json = {
				"status": "success",
				"message": "Bookmark not exists!",
				"data": {
					"exists": False
				}
			}
		
		return JsonResponse(json)
