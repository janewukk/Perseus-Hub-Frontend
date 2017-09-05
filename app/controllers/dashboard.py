from django.views import View
from django.db.models import F
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin as LoginRequiredResource

from app.models import Dataset, User, Bookmark
from app.services.graph import *
from app.services.utils import flash_session_message, absolute_path

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
		except Exception as e:
			dataset = None

		# handle error
		if dataset is None:
			raise Http404("Dataset does not exist!")

		# make graph
		# attempt cache first
		graph_data = graph.graph_from_cache(dataset)
		if not graph_data:
			# load from file with cache
			graph_data = graph.graph_from_file(dataset, cache=True)

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
			bookmarks = request.user.bookmark_set
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
		# TODO: Form validation
		# extract attribute
		publicized = False if request.POST['is_publicized'] == "false" else True
		# grab the request data and create dataset
		bookmark = Bookmark(priority = request.POST['priority'], \
							x_coord = request.POST['x_coord'], \
							y_coord = request.POST['y_coord'], \
							prop = request.POST['prop'], \
							dataset = Dataset.objects.get(id = request.POST['dataset_id']),
							creator = request.user
						)
		# save to db
		bookmark.save()

		return JsonResponse({
				'status': "success",
				'message': "Bookmark created successfully!"
			})

