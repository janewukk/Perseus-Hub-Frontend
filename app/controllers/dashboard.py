from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin as LoginRequiredResource

from app.models import Dataset

class DashboardController(LoginRequiredResource, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request):
		# render the dataset view 
		# with all publicized datasets or user specific
		# TODO: Pagination
		if 'my' in request.GET.keys():
			datasets = request.user.dataset_set
		else:
			datasets = Dataset.objects.filter(publicized = True)

		return render(request, 'dashboard/datasets.html', {
				'datasets' : datasets
			})

class DatasetViewController(LoginRequiredResource, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request, *args, **kwargs):
		# TODO:
		# return a template specifically rendering a dataset
		return HttpResponse(kwargs.get('id'))