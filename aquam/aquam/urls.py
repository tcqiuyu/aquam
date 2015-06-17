"""aquam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from . import views as aquam_views
from apps.solutions import views as solution_views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    
    url(r"^$", aquam_views.index, name="index"),
    url(r"^index/$", aquam_views.index, name="index"),
    url(r"^solutions/$", aquam_views.solutions, name="solutions"),
    url(r"^geoanalytics/$", aquam_views.geoanalytics, name="geoanalytics"),
    url(r"^contact/$", aquam_views.contact, name="contact"),
    
    url(r"^solutions/water-use-analyzer/$", solution_views.water_use_analyzer, name="water-use-analyzer"),

]
