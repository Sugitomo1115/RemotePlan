from django.urls import path
from . import views

urlpatterns=[
    path(r'', views.top, name="top")
]