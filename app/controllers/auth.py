from django.http import HttpResponse
from django.views import View

class LoginController(View):

	def get(self, request):
		return HttpResponse("This is supposed to be login page")

	def post(self, request):
		return HttpResponse("Login status")


class RegisterController(View):

	def get(self, request):
		return HttpResponse("This is supposed to be register page")

	def post(self, request):
		return HttpResponse("Registration status")