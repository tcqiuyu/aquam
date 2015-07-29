from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        "page_title": "VODA | Oilfield Water Management",
    }
    return render(request, "index.html", context)


def solutions(request):
    context = {
        "page_title": "VODA | Solutions",
    }
    return render(request, "solutions.html", context)


def geoanalytics(request):
    context = {
        "page_title": "VODA | Geoanalytics",
    }
    return render(request, "geoanalytics.html", context)


def contact(request):
    context = {
        "page_title": "VODA | Contact",
    }
    return render(request, "contact.html", context)


