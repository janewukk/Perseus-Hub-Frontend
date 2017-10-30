import json
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
							note = request.POST['note'], \
							node_id = request.POST['node_id'], \
							publicized = publicized, \
							dataset = Dataset.objects.get(id = request.POST['dataset_id']),
							creator = request.user
						)
		# save to db
		bookmark.save()

		return JsonResponse({
				'status': "success",
				'message': "Bookmark created successfully!",
				'data': {
					'bookmark_id': bookmark.id
				}
			})

class BookmarkDeleteController(LoginRequiredResource, View):
	"""
	Handle the deletion of bookmarks
	
	Extends:
		LoginRequiredResource
		View
	"""
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def post(self, request, *args, **kwargs):
		# extract bookmark id
		bookmark_id = kwargs.get('id')

		# check if bookmark exists
		bookmark = Bookmark.objects.get(id = bookmark_id)

		if not bookmark:
			return JsonResponse({
					'status': "error",
					'message': "Bookmark not exists!"
				})

		# delete bookmark
		bookmark.delete()

		return JsonResponse({
				'status': "success",
				'message': "Bookmark deleted successfully!"
			})

class BookmarkUpdateController(LoginRequiredResource, View):
	"""
	Handle the deletion of bookmarks
	
	Extends:
		LoginRequiredResource
		View
	"""
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def post(self, request, *args, **kwargs):
		# extract bookmark id
		bookmark_id = kwargs.get('id')

		# check if bookmark exists
		bookmark = Bookmark.objects.get(id = bookmark_id)

		if not bookmark:
			return JsonResponse({
					'status': "error",
					'message': "Bookmark not exists!"
				})

		# update bookmark
		updates = json.loads(request.POST['updates'])

		for key, value in updates.items():
			setattr(bookmark, key, value)

		# save updates
		bookmark.save(update_fields=['priority', 'x_coord', 'y_coord', 'prop', 'publicized', 'note'])

		return JsonResponse({
				'status': "success",
				'message': "Bookmark updated successfully!"
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
		# extract node id and dataset id
		dataset_id = request.POST['dataset_id']
		node_id = request.POST['node_id']

		# check if bookmark exists
		bookmarks = Bookmark.objects.filter(dataset_id = dataset_id, node_id = node_id)

		if len(bookmarks) == 0:
			return JsonResponse({
					'status': "success",
					'data': {
						'exists': False
					}
				})

		return JsonResponse({
				'status': "success",
				'data': {
					'exists': True,
					'bookmark_id': bookmarks[0].id
				}
			})


