from django.views import View
from django.db.models import F
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin as LoginRequiredResource

from app.models import Dataset, User, Bookmark
from app.services.graph import *
from app.services.utils import flash_session_message

graph = Graph()

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

		# sort datasets
		try:
			datasets = datasets.order_by(F('created_at').desc())
		except Exception as e:
			print e

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
			bookmarked = dataset in request.user.dataset_set.all()
		except Exception as e:
			dataset = None
			bookmarked = False
		
		# handle error
		if dataset is None:
			# TODO : Remove the error message after debugging!
			# raise Http404("Dataset does not exist!")
			pass

		# make graph
		# TODO: make the file name dynamic
		graph_data = graph.graph_from_file('combined_data.csv')

		return render(request, 'dashboard/dataset-template.html',{
				'dataset' : dataset,
				'graph_script' : graph_data['graph_script'],
				'graph' : graph_data['graph']
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

		# sort bookmarks
		try:
			bookmarks = bookmarks.order_by(F('created_at').desc()) \
								 .order_by(F('priority').desc())
		except Exception as e:
			print "Bookmark fetch error:", e

		return render(request, 'dashboard/bookmarks.html', {
				'bookmarks' : bookmarks
			})

	def post(self, request):
		# create a bookmark
		# TODO
		pass

