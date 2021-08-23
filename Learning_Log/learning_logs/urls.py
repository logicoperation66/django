"""Definiuje wzorce adresów URL dla learning_logs."""

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    #Strona główna.
    path('', views.index, name='index'),
    #Wyświetlaie wszystkich tematów.
    path('topics/', views.topics, name='topics'),
    #Strona szczegółowa dotycząca pojędyńczego tematu.
    path('topics/(<int:topic_id>)/', views.topic, name='topic'),
]