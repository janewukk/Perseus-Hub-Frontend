from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin as LoginRequiredResource

from app.models import Dataset

class SettingsController(LoginRequiredResource, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request):
		
		return render(request, 'settings/index.html')

	def post(self, request):
		"""
		Handle updated account information
		
		Arguments:
			request {HttpRequest} -- The request object
		"""

		# set the attributes
		if 'email' in request.POST.keys() and request.POST['email'] != "":
			request.user.username = request.POST['email']
			request.user.email = request.POST['email']
		if 'password' in request.POST.keys() and request.POST['password'] != "":
			request.user.set_password(request.POST['password'])
		request.user.save();

		# success response
		return JsonResponse({
				'status' : "success",
				'message' : "Your account info has been updated!"
			})

