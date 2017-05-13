import json
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin as LoginRequiredResource

from app.models import Dataset

class DatasetSearchController(LoginRequiredResource, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def post(self, request):
		"""
		A simple search engine based on full text search of dataset names
		
		Arguments:
			request {HTTPRequest} -- Request object
		"""
		# check for request param
		body = json.loads(request.body.decode('utf-8'))
		query = body.get('query', False)

		if query == False:
			# if empty, then simply return empty list
			datasets = []
		else:
			# search for datasets
			datasets = Dataset.objects.filter(title__icontains = query)

		if len(datasets) == 0:
			response = {
				'status' : 'error',
				'message' : 'No matches found'
			}
		else:
			response = {
				'status' : 'success',
				'message' : 'Fetched!',
				'data' : datasets
			}

		# spit out the datasets
		return JsonResponse(response)

class DatasetUploadController(LoginRequiredResource, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request):
		return render(request, 'dashboard/upload-dataset.html')

	def post(self, request):
		"""
		Handle upload of dataset files
		
		Arguments:
			request {HTTPRequest} -- Request object
		"""
		# TODO: form validation
		# extract attribute
		publicized = False if request.POST['is_publicized'] == "false" else True
		# grab the request data and create dataset
		dataset = Dataset(title = request.POST['title'], \
						publicized = publicized, \
						raw_data_file = request.FILES['file'], \
						uploader = request.user,)
		# save the metadata for the dataset 
		# along with file as Django internally saved it
		dataset.save()
		# TODO: Notify spark with dataset raw data path
		# and the dataset id so that later Spark callback
		# can retrieve the user related to this dataset
		return JsonResponse({
				'status' : "success",
				'message' : "Your dataset has been uploaded and is being processed. \
							we will send you an email once it's done!"
			})

class DatasetQueryController(LoginRequiredResource, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request, *args, **kwargs):
		# extract id
		dataset_id = kwargs.get('id')

		# extract adjMatrix param, one of ['adjMatrix', 'egonet']
		param = request.GET['type']
		
		# TODO: find nodes dynamically from database
		if param == 'adjMatrix':
			return JsonResponse({
					'status' : "success",
					'message' : "Your nodes are updated!"
				})
		if param == 'egonet':
			# for now, returning dummy data
			return JsonResponse({
				"Nodes": [
					{
					"Id": "338",
					"Name": "338"
					},
					{
					"Id": "340",
					"Name": "340"
					},
					{
					"Id": "341",
					"Name": "341"
					},
					{
					"Id": "342",
					"Name": "342"
					}
					],
					"Links": [
					{
					"Source": "338",
					"Target": "341",
					"Value": "0"
					},
					{
					"Source": "338",
					"Target": "340",
					"Value": "0"
					},
					{
					"Source": "340",
					"Target": "341",
					"Value": "0"
					},
					{
					"Source": "342",
					"Target": "341",
					"Value": "0"
					}
				]
			})
		return JsonResponse({
				'status' : 'error',
				'message' : "Param is invalid. Try again!"
			})
