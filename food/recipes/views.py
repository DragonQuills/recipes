import requests
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

def load_recipes(request):
    from_sheets = requests.get("https://spreadsheets.google.com/feeds/cells/1MLqtrZ9gQHGK02wAtxmMogOmrhqRsUsAE5eXT1IAzOE/od6/public/values?alt=json")
    recipes_raw = from_sheets.json()
    recipe_cell_data = []
    for recipe in recipes_raw["feed"]["entry"]:
        recipe_cell_data.append(recipe["gs$cell"])
    assignment = {1:"food_name",
                  2:"link",
                  3:"image_link",
                  4:"genres",
                  5:"type",
                  6:"cook_time",
                  7:"prep_time",
                  8:"freezes_well",
                  9:"vegetarian",
                  10:"could_be_vegetarian",
                  11:"spicy",
                  12:"could_be_spicy",
                  13:"tags"}
    index = 0
    recipe_counter = 2
    recipe_model_data = {}
    for x in range(recipe_cell_data.length()+1):
        if recipe_cell_data[index]["row"] == recipe_counter:
            recipe_model_data[assignment[recipe_cell_data[index]["col"]]] = recipe_cell_data[index]["$t"]
        else:
            Recipe.objects.create_recipe(recipe_model_data)
            recipe_counter += 1
            recipe_model_data = {}
            recipe_model_data[assignment[recipe_cell_data[index]["col"]]] = recipe_cell_data[index]["$t"]
        index += 1
    context = {"test": recipes}
    return render(request, 'load_recipes.html', context)
