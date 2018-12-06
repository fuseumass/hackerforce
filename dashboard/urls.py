from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='index'),
    path('404', views.page404, name='404'),
]
