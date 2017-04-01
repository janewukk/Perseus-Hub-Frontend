from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from app.models import User
from app.services.utils import flash_session_message

"""
Helper to login in a user
"""
def login_with_authentication(request, email, password):
	# authenticate user
	user = authenticate(username = email, email = email, password = password)
	if user is not None:
		# login the user with session
		login(request, user)
		# redirect to dashboard with success message
		flash_session_message(request, 'success', "Welcome!")
		return redirect('/dashboard/')
	else:
		# user existed, but password is not right
		# redirect to signin page with error message
		flash_session_message(request, 'error', 'Your password is not correct! Please try again!')
		return redirect('/login/')


class LoginController(View):

	def get(self, request):
		"""
		Show the login page
		
		Arguments:
			request {HTTPRequest} -- Request object
		"""
		return render(request, 'auth/login.html') 

	def post(self, request):
		"""
		Login an existing user
		
		Arguments:
			request {HTTPRequest} -- Request object
		"""
		# retrieve auth credentials
		email = request.POST['email']
		password = request.POST['password']
		# check if user already exists
		user = User.objects.filter(email = email)
		if len(user) > 0:
			return login_with_authentication(request, email, password)
		else:
			# user does not exist, redirect to signin page with error message
			flash_session_message(request, 'error', "Your email does not exist!")

			return redirect('/login');

class LogoutController(View):

	def get(self, request):
		"""
		Logout the current user
		
		Arguments:
			request {HTTPRequest} -- Request Object
		
		Returns:
			HTTPResponse -- Redirect request
		"""
		logout(request)
		flash_session_message(request, 'info', 'Logged out!')
		return redirect('/login/')


class RegisterController(View):

	def get(self, request):
		"""
		Show the registration page
		
		Arguments:
			request {HTTPRequest} -- Request object
		"""
		return render(request, 'auth/register.html')

	def post(self, request):
		"""
		Create an user from registration page
		
		Arguments:
			request {HTTPRequest} -- HTTP Request object
		"""
		# retrieve auth credentials
		email = request.POST['email']
		password = request.POST['password']

		# check if user already exists
		user = User.objects.filter(email = email)

		if len(user) > 0:
			flash_session_message(request, 'warning', "Please login instead")
			return redirect('/login/')
		else:
			# create new user
			user = User.objects.create_user(email = email, password = password, username = email)
			# save the user
			user.save()
			# login the user
			login(request, user)
			# redirect to dashboard with success message
			flash_session_message(request, 'success', 'Welcome!')
			return redirect('/dashboard/')
