from django.urls import path

from . import views

app_name = 'emails'
urlpatterns = [
    path('', views.emails, name='emails'),
    path('drafts', views.drafts, name='drafts'),
    path('outbox', views.outbox, name='outbox'),
    path('sent', views.sent, name='sent'),
]