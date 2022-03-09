import imp
from django.urls import path
from . import views
from .forms import LoginForm
from .views import CustomLoginView, CustomLogoutView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns=[
    path('', views.top, name="top"), #トップ画面
    path('privacy', views.privacy, name="privacy"), #利用規約画面
    path('privacy_check', views.privacy_check, name="privacy_check"), #ユーザー登録前の利用規約確認画面
    path('create/', views.create, name="create"), #企画作成画面
    path('add_category/', views.add_category, name="add_category"), #カテゴリー追加画面
    path('<int:plan_id>/', views.detail, name="detail"), #企画詳細画面
    path('<int:plan_id>/like', views.like,name='like'), #イイね機能
    path('api/plans/<int:plan_id>/like', views.api_like), #イイね機能
    path('<int:plan_id>/delete', views.delete, name='delete'), #企画削除機能
    path('signup/', views.signup, name="signup"), #サインアップ画面
    path('regist_save/', views.regist_save, name='regist_save'), #ユーザー登録機能
    path('login/', CustomLoginView.as_view(), name="login"), #ログイン
    path('logout/', CustomLogoutView.as_view(), name="logout"), #ログアウト
]