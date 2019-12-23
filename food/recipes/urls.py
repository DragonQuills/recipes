from django.urls import path

from . import views

app_name = 'recipes'
urlpatterns = [
    #home page at recipes/
    path('', views.index, name='index'),
    path('load_recipes', views.load_recipes, name='load_recipes',
    path('<int:pk>/', views.DetailView.as_view(), name='detail')
]
