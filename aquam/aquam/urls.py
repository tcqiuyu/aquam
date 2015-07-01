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
    
    url(r"^solutions/water-use-analyzer/$", solutions_views.water_use_analyzer, name="water-use-analyzer"),
    url(r"^solutions/water-use-analyzer/get-water-use/$", solutions_views.get_water_use, name="get-water-use"),
    url(r"^solutions/water-use-analyzer/get-horizontal-length/$", solutions_views.get_horizontal_length, name="get-horizontal-length"),
    url(r"^solutions/water-use-analyzer/get-water-use-per-horizontal-foot/$", solutions_views.get_water_use_per_horizontal_foot, name="get-water-use-per-horizontal-foot"),
    url(r"^solutions/water-use-analyzer/get-annual-water-use/$", solutions_views.get_annual_water_use, name="get-annual-water"),
    url(r"^solutions/water-use-analyzer/get-annual-horizontal-feet-dilled/$", solutions_views.get_annual_horizontal_feet_drilled, name="get-annual-horizontal-feet-dilled"),
    url(r"^solutions/water-use-analyzer/get-annual-bbls-ft-metric/$", solutions_views.get_annual_bbls_ft_metric, name="get-annual-bbls-ft-metric"),
    url(r"^solutions/water-use-analyzer/get_linear_fitting", solutions_views.get_linear_fitting, name="get-linear-fitting"),
    url(r"^solutions/water-use-analyzer/get_quadratic_fitting", solutions_views.get_quadratic_fitting, name="get-quadratic-fitting"),
    url(r"^solutions/water-use-analyzer/get-cubic-fitting", solutions_views.get_cubic_fitting, name="get-cubic-fitting"),
    
    url(r"^solutions/produced-water-modeler/$", solutions_views.produced_water_modeler, name="produced-water-modeler"),
    url(r"^solutions/produced-water-modeler/get-arp-model/$", solutions_views.get_arp_model, name="get-arp-model"),
    url(r"^solutions/produced-water-modeler/get-arp-prediction/$", solutions_views.get_arp_prediction, name="get-arp-prediction"),
]
