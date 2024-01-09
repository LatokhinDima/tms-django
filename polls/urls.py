from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>', views.detail, name='detail'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout', LogoutView.as_view(), name='logout'),
]
