from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin as LoginRequiredResource

from app.models import Dataset

class DashboardController(LoginRequiredResource, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request):
		# render the default dataset view 
		# with all datasets 
		# TODO: Pagination
		return render(request, 'dashboard/datasets.html', {
				'datasets' : Dataset.object.all()
			})

class DatasetViewController(LoginRequiredResource, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request, *args, **kwargs):
		# TODO:
		# return a template specifically rendering a dataset
		return HttpResponse(kwargs.get('id'))