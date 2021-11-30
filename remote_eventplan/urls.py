from django.urls import path
from . import views

urlpatterns=[
    path('', views.top, name="top"),
    path('create/', views.create, name="create"),
    path('<int:plan_id>/', views.detail, name="detail"),
    path('<int:plan_id>/like', views.like,name='like'),
    path('api/plans/<int:plan_id>/like', views.api_like),
    path('<int:plan_id>/delete', views.delete, name='delete'),
]