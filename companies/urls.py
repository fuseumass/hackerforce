from django.urls import path

from . import views

app_name = 'companies'
urlpatterns = [
    path('', views.companies, name='index'),
    path('new', views.new, name='new')
]