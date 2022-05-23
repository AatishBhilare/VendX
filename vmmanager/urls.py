from django.urls import path

from vmmanager import views

urlpatterns = [
    path('', views.loginuser, name='login'),
    path('index/', views.index, name='index'),
    path('sales/', views.sales, name='sales'),
    path('logout/', views.logoutuser, name='logout'),
    path('item-edit/<int:itmid>/', views.edititem, name='edititem'),
    path('home/', views.home, name='home'),
    path('pay/<int:pitmid>/', views.initiate_payment, name='pay'),
    path('callback/', views.callback, name='callback'),
]