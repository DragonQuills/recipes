import requests
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Recipe

# def index(request):
#     return HttpResponse("You're at the recipes index page.")

class IndexView(generic.ListView):
    model = Recipe
    context_object_name = 'recipes_list'
    template_name = 'recipes/index.html'

class DetailView(generic.DetailView):
    model = Recipe
    template_name = 'recipes/details.html'

def load_recipes(request):
    from_sheets = requests.get("https://spreadsheets.google.com/feeds/cells/1MLqtrZ9gQHGK02wAtxmMogOmrhqRsUsAE5eXT1IAzOE/od6/public/values?alt=json")
    recipes_raw = from_sheets.json()
    recipe_cell_data = []
    for recipe in recipes_raw["feed"]["entry"]:
        recipe_cell_data.append(recipe["gs$cell"])
    assignment = {}
    recipe_counter = 2
    recipe_model_data = {}
    for recipe_cell in recipe_cell_data:
        if recipe_cell["row"] == "1":
            assignment[recipe_cell["col"]] = recipe_cell["$t"].strip().lower().replace(" ", "_")
        elif int(recipe_cell["row"]) == recipe_counter:
            recipe_model_data[assignment[recipe_cell["col"]]] = recipe_cell["$t"].strip()
        elif int(recipe_cell["row"]) == recipe_counter + 1:
            Recipe.objects.create_recipe(recipe_model_data)
            recipe_counter += 1
            recipe_model_data = {}
            recipe_model_data[assignment[recipe_cell["col"]]] = recipe_cell["$t"].strip()
    context = {"new_recipes": Recipe.objects.all()}
    return render(request, 'recipes/load_recipes.html', context)
