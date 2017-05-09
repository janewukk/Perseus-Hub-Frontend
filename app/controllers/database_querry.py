from django.views import View
from django.db.models import F
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin as LoginRequiredResource

from app.models import Dataset, User, Bookmark
from app.services.graph import graph_from_file
from app.services.utils import flash_session_message

import json
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin as LoginRequiredResource

from app.models import Dataset

import json

class QuerryController(LoginRequiredResource, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def post(self, request):
		"""
		A simple search engine based on full text search of dataset names
		
		Arguments:
			request {HTTPRequest} -- Request object
		"""
		# check for request param
		# body = json.loads(request.body.decode('utf-8'))
		# query = body.get('query', False)
		print request.body

		response = {
			'test': request
		}

		# if query == False:
		# 	# if empty, then simply return empty list
		# 	datasets = []
		# else:
		# 	# search for datasets
		# 	datasets = Dataset.objects.filter(title__icontains = query)

		# if len(datasets) == 0:
		# 	response = {
		# 		'status' : 'error',
		# 		'message' : 'No matches found'
		# 	}
		# else:
		# 	response = {
		# 		'status' : 'success',
		# 		'message' : 'Fetched!',
		# 		'data' : datasets
		# 	}

		# spit out the datasets
		return JsonResponse({
				'status' : "request",
				'message' : "Your dataset has been uploaded and is being processed. \
							we will send you an email once it's done!"
		})



	# def post(self, request):
	#     # print("Post request in Querry Called")
	#     # print(request)
	#     return redirect('/dashboard/')