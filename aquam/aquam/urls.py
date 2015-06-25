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
# Core Django imports
from django.conf.urls import include, url
from django.contrib import admin

# Apps imports
import views as aquam_views
import apps.solutions.views as solutions_views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r"^$", aquam_views.index, name="index"),
    url(r"^index/$", aquam_views.index, name="index"),
    url(r"^solutions/$", aquam_views.solutions, name="solutions"),
    url(r"^geoanalytics/$", aquam_views.geoanalytics, name="geoanalytics"),
    url(r"^contact/$", aquam_views.contact, name="contact"),
    
    url(r"^solutions/water-use-analyzer/demo/$", solutions_views.water_use_analyzer_demo, name="water-use-analyzer-demo"),
    url(r"^solutions/water-use-analyzer/demo/water-use-json/$", solutions_views.water_use_json, name="water-use-json"),
    url(r"^solutions/water-use-analyzer/demo/horizontal-length-json/$", solutions_views.horizontal_length_json, name="horizontal-length-json")
]
