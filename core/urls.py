from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('companies', views.companies, name='companies'),
    path('contacts', views.contacts, name='contacts'),
    path('email', views.email, name='email'),
    path('drafts', views.drafts, name='drafts'),
    path('outbox', views.outbox, name='outbox'),
    path('sent', views.sent, name='sent'),
    path('settings', views.settings, name='settings'),
]