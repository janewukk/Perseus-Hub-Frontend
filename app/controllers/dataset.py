import json, subprocess
from django.views import View
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin as LoginRequiredResource

from app.models import Dataset
from app.services.utils import absolute_path, base_path

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
		query = request.POST['query']

		# search for datasets
		datasets = Dataset.objects.filter(title__icontains = query, \
										  publicized = True,
										  processed = True,
										  trashed = False)	

		if len(datasets) == 0:
			response = {
				'status' : 'error',
				'message' : 'No matches found'
			}
		else:
			response = {
				'status' : 'success',
				'message' : 'Fetched!',
				'data' : serializers.serialize('json', datasets, fields=('title','id'))
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
		# Notify spark with dataset raw data path
		# and the dataset id so that later Spark callback
		# can retrieve the user related to this dataset
		filename = dataset.raw_data_file.name.split('/')[-1]
		subprocess.Popen(["bash", base_path('/runSpark.sh'), filename, str(request.user.id), str(dataset.id)], close_fds=True)

		return JsonResponse({
				'status' : "success",
				'message' : "Your dataset has been uploaded and is being processed. \
							we will send you an email once it's done! Please remember to check your spam folder!"
			})

class DatasetUpdateController(LoginRequiredResource, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def post(self, request, *args, **kwargs):
		"""
		Handling update of dataset attributes
		
		Arguments:
			request {HTTPRequest} -- Request object
		"""
		# extract dataset id
		dataset_id = kwargs.get('id')

		# check if dataset exists
		dataset = Dataset.objects.get(id = dataset_id)

		if not dataset:
			return JsonResponse({
					'status': "error",
					'message': "Dataset not exists!"
				})

		# update bookmark
		updates = json.loads(request.POST['updates'])

		for key, value in updates.items():
			setattr(dataset, key, value)

		# save updates
		dataset.save(update_fields=['publicized', 'title'])

		return JsonResponse({
				'status': "success",
				'message': "Dataset updated successfully!"
			})

class DatasetDeleteController(LoginRequiredResource, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def post(self, request, *args, **kwargs):
		"""
		Handling deletion of dataset
		
		Basically mark the dataset as trashed, and let worker clean it up later
		
		Arguments:
			request {HTTPRequest} -- Request objects
		"""
		# extract dataset id
		dataset_id = kwargs.get('id')

		dataset = Dataset.objects.get(id = dataset_id)

		if not dataset:
			return JsonResponse({
					'status': "error",
					'message': "Dataset does not exist!"
				})

		# mark as trashed
		dataset.trashed = True
		dataset.save()

		return JsonResponse({
				'status': "success",
				'message': "Dataset has been marked as delete!"
			})
