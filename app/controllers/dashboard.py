from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin as LoginRequiredResource

from app.models import Dataset, User
from app.services.utils import flash_session_message

class DashboardController(LoginRequiredResource, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request):
		# render the dataset view 
		# with all publicized datasets or user specific
		# TODO: Pagination
		if 'my' in request.GET.keys():
			datasets = request.user.dataset_set
		elif 'user' in request.GET.keys():
			users = User.objects.filter(id = request.GET['user'])
			if len(users) == 0:
				flash_session_message(request, "error", "No datasets available")
				datasets = []
			else:
				datasets = users.datasets().filter(publicized = True)
		else:
			datasets = Dataset.objects.filter(publicized = True)

		return render(request, 'dashboard/datasets.html', {
				'datasets' : datasets
			})

class DatasetViewController(LoginRequiredResource, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request, *args, **kwargs):
		# return a template specifically rendering a dataset
		return render(request, 'dashboard/dataset-template.html',{
				'id' : kwargs.get('id')
			})

class BookmarkViewController(LoginRequiredResource, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request):
		# retrieve user bookmarks
		return render(request, 'dashboard/bookmarks.html', {
				'bookmarks' : request.user.bookmark_set
			})

