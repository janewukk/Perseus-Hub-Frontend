from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render
from django.contrib.auth import authenticate
from app.models import User

"""
Helper to login in a user
"""
def login_with_authentication(request, email, password):
	# authenticate user
	user = authenticate(username = email, password = password)
	if user is not None:
		# login the user with session
		login(request, user)
		# redirect to dashboard with success message
		return render(request, 'dashboard/index.html', {
				'status' : 'success',
				'message' : 'Welcome!'
			})
	else:
		# user existed, but password is not right
		# redirect to signin page with error message
		return render(request, 'auth/login.html', {
				'status' : 'error',
				'message' : 'Your password is not correct! Please try again!'
			})

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
			return render(request, 'auth/login.html', {
					'status' : 'error',
					'message' : 'Your email does not exist! Please try again!'
				});

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
			return login_with_authentication(request, email, password)
		else:
			# create new user
			user = User.objects.create_user(username = email, password = password)
			# save the user
			user.save()
			# login the user
			login(request, user)
			# redirect to dashboard with success message
			return render(request, 'dashboard/index.html', {
				'status' : 'success',
				'message' : 'Welcome!'
			})
			

