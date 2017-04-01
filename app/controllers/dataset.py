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
		if request.POST['query'] == "":
			# if empty, then simply return every dataset
			datasets = Dataset.objects.all()
		else:
			# search for datasets
			datasets = Dataset.objects.filter(name__icontains = request.POST['query'])

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
		# grab the request data and create dataset
		dataset = Dataset(publicized = request.POST['publicized'], \
						raw_data = request.FILES['file'], \
						uploader = request.user)
		# save the metadata for the dataset 
		# along with file as Django internally saved it
		dataset.save()
		# TODO: Notify spark with dataset raw data path
		# and the dataset id so that later Spark callback
		# can retrieve the user related to this dataset
		return JsonResponse({
				'status' : "success",
				'message' : "Your dataset has been uploaded and processed. \
							we will send you an email once it's done!"
			})