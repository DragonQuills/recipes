from django.urls import path

from . import views

app_name = 'recipes'
urlpatterns = [
    #home page at recipes/
    path('', views.index, name='index'),

]
