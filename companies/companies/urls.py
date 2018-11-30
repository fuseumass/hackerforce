from django.urls import path

from . import views

app_name = 'companies'
urlpatterns = [
    path('', views.companies, name='index'),
    path("new", views.company_new, name="new"),
    path("<int:pk>/edit", views.company_edit, name="edit")
]