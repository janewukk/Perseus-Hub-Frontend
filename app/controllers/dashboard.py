from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin as LoginRequiredResource

class DashboardController(LoginRequiredResource, View):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get(self, request):
		return render(request, 'dashboard/index.html')