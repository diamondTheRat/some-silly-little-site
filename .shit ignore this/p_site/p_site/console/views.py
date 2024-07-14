from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView

# Create your views here.


class console(TemplateView):
    template_name = "console/index.html"
