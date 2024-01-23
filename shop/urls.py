from django.urls import path
from . import views
from .views import signup

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>/', views.detail, name='detail'),
    path('category/<int:category_id>/', views.category, name='category'),
    path('page/', views.index, name='index'),
    path('signup/', signup, name='signup'),
    path('signup/page/', views.index, name='index'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),

]
