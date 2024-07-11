from django.urls import path
import console.views as views
import os
urlpatterns = [
    path("", views.console.as_view())
]
