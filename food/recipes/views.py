from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Recipe

def index(request):
    return HttpResponse("You're at the recipes index page.")

class DetailView(generic.DetailView):
    model = Recipe
    template_name = 'recipes/details.html'
