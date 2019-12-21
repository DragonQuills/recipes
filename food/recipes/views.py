import requests
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

#from .models import Recipe

def index(request):
    return HttpResponse("You're at the recipes index page.")

def load_recipes(request):
    from_sheets = requests.get("https://spreadsheets.google.com/feeds/cells/1MLqtrZ9gQHGK02wAtxmMogOmrhqRsUsAE5eXT1IAzOE/od6/public/values?alt=json")
    recipes_raw = from_sheets.json()
    recipes = []
    for recipe in recipes_raw["feed"]["entry"]:
        recipes.append(recipe["gs$cell"])

    context = {"test": recipes}
    return render(request, 'load_recipes.html', context)
