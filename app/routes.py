"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

# import controllers
from app.controllers.auth import LoginController
from app.controllers.auth import RegisterController
from app.controllers.dashboard import DashboardController
from app.controllers.file import FileUploadController

urlpatterns = [
	url(r'^login/$', LoginController.as_view()),
	url(r'^register/$', RegisterController.as_view()),
    url(r'^dashboard/$', DashboardController.as_view()),
    url(r'^dataset/upload/$', FileUploadController.as_view())
]
