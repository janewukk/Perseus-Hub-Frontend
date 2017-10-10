import json, subprocess
from django.views import View
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin as LoginRequiredResource

from app.models import Dataset
from app.services.utils import absolute_path

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
		# Notify spark with dataset raw data path
		# and the dataset id so that later Spark callback
		# can retrieve the user related to this dataset
		filename = dataset.raw_data_file.name.split('/')[-1]
		subprocess.Popen(["bash", absolute_path('runSpark.sh'), filename, str(request.user.id), str(dataset.id)], close_fds=True)

		return JsonResponse({
				'status' : "success",
				'message' : "Your dataset has been uploaded and is being processed. \
							we will send you an email once it's done! Please remember to check your spam folder!"
			})
