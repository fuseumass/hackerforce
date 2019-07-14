from django.urls import path, include

from .views import *


urlpatterns_industries = [
    path("industries", industries, name="index"),
    path("industries/new", industry_new, name="new"),
    path("industries/<int:pk>", industry_edit, name="edit"),
    path("industries/<int:pk>/delete", industry_delete, name="delete"),
]


app_name = 'companies'
urlpatterns = [
    path('', companies, name='index'),
    # path('new', views.new, name='new')
    path("new", company_new, name="new"),
    path("<int:pk>/edit", company_edit, name="edit"),
    path("<int:pk>/delete", company_delete, name="delete"),
    path("<int:pk>/view", company_detail, name="view"),

    path("", include((urlpatterns_industries, "industries"))),


]