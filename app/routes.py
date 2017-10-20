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
from app.controllers.settings import SettingsController
from app.controllers.auth import LoginController, LogoutController, RegisterController
from app.controllers.pages import DashboardViewController, DatasetViewController, BookmarkViewController
from app.controllers.dataset import DatasetSearchController, DatasetUploadController, DatasetUpdateController, DatasetDeleteController
from app.controllers.bookmark import BookmarkCreateController, BookmarkValidateController, BookmarkDeleteController, BookmarkUpdateController

# Graph apis
from app.controllers.graph import *

urlpatterns = [
    url(r'^$', DashboardViewController.as_view()),
	url(r'^login', LoginController.as_view()),
    url(r'^logout', LogoutController.as_view()),
	url(r'^register', RegisterController.as_view()),
    url(r'^dashboard', DashboardViewController.as_view()),
    url(r'^settings', SettingsController.as_view()),
    url(r'^upload', DatasetUploadController.as_view()),
    url(r'^bookmarks/(?P<id>\d+)/update', BookmarkUpdateController.as_view()),
    url(r'^bookmarks/(?P<id>\d+)/delete', BookmarkDeleteController.as_view()),
    url(r'^bookmarks/create', BookmarkCreateController.as_view()),
    url(r'^bookmarks/validate', BookmarkValidateController.as_view()),
    url(r'^bookmarks/$', BookmarkViewController.as_view()),
    url(r'^search', DatasetSearchController.as_view()),
    url(r'^datasets/(?P<id>\d+)/update', DatasetUpdateController.as_view()),
    url(r'^datasets/(?P<id>\d+)/delete', DatasetDeleteController.as_view()),
    url(r'^datasets/(?P<id>\d+)', DatasetViewController.as_view()),

    url(r'^ClickPlot',ClickPlot),
    url(r'^GetEgonet',GetEgonet),
    url(r'^ExpandEgonet',ExpandEgonet),
    url(r'^GetAdjMatrix', GetAdjMatrix),
    url(r'^GetGFADD', GetGFADD),
    url(r'^GetABOD', GetABOD),
    url(r'^GetCombAnScore', GetCombAnScore),
    url(r'^SearchNodeID',SearchNodeID),
]
