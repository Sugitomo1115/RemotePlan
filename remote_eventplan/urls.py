from django.urls import path
from . import views
from .forms import LoginForm
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns=[
    path('', views.top, name="top"),
    path('privacy', views.privacy, name="privacy"),
    path('privacy_check', views.privacy_check, name="privacy_check"),
    path('create/', views.create, name="create"),
    path('<int:plan_id>/', views.detail, name="detail"),
    path('<int:plan_id>/like', views.like,name='like'),
    path('api/plans/<int:plan_id>/like', views.api_like),
    path('<int:plan_id>/delete', views.delete, name='delete'),
    path('signup/', views.signup, name="signup"),
    path('regist_save/', views.regist_save, name='regist_save'),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]