from django.views import View
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin as LoginRequiredResource

from app.models import Dataset, User, Bookmark
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
				datasets = users[0].datasets().filter(publicized = True)
		else:
			datasets = Dataset.objects.filter(publicized = True)

		return render(request, 'dashboard/datasets.html', {
				'datasets' : datasets
			})

class DatasetViewController(LoginRequiredResource, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request, *args, **kwargs):
		# extract id
		dataset_id = kwargs.get('id')
		# fetch the dataset
		try:
			dataset = Dataset.objects.get(id = dataset_id)
		except Exception as e:
			dataset = None
		if dataset is None:
			# TODO : Remove the error message after debugging!
			# raise Http404("Dataset does not exist!")
			pass

		return render(request, 'dashboard/dataset-template.html',{
				'dataset' : dataset
			})

class BookmarkViewController(LoginRequiredResource, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request):
		# render the bookmarks view 
		# with all publicized bookmarks or user specific
		# TODO: Pagination
		if 'my' in request.GET.keys():
			bookmarks = request.user.dataset_set
		elif 'user' in request.GET.keys():
			users = User.objects.filter(id = request.GET['user'])
			if len(users) == 0:
				flash_session_message(request, "error", "No bookmarks available")
				bookmarks = []
			else:
				bookmarks = users[0].bookmarks().filter(publicized = True)
		else:
			bookmarks = Bookmark.objects.filter(publicized = True)

		return render(request, 'dashboard/bookmarks.html', {
				'bookmarks' : bookmarks
			})

	def post(self, request):
		# create a bookmark
		# TODO
		pass

