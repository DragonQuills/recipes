import requests
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Recipe, Genre

# def index(request):
#     return HttpResponse("You're at the recipes index page.")

class IndexView(generic.ListView):
    model = Recipe
    context_object_name = 'recipes_list'
    template_name = 'recipes/index.html'

class DetailView(generic.DetailView):
    model = Recipe
    template_name = 'recipes/details.html'

class SearchView(generic.ListView):
    model = Genre
    context_object_name = 'genres_list'
    template_name = 'recipes/search.html'
    #TODO: search view assembles query params and then redirects

class ResultsView(generic.ListView):
    #request.GET.get('q', '')
    template_name = 'recipes/results.html'
    context_object_name = 'recipes_list'

    def get_queryset(self):
         """ filter results by query params given by search """
         return Recipe.objects.filter(
                vegetarian=self.request.GET.get('vegetarian', True)
         )

def load_recipes(request):
    # call published google sheets to gather data
    from_sheets = requests.get("https://spreadsheets.google.com/feeds/cells/1MLqtrZ9gQHGK02wAtxmMogOmrhqRsUsAE5eXT1IAzOE/od6/public/values?alt=json")
    recipes_raw = from_sheets.json()
    recipe_cell_data = []
    # initial parse of data into an array, results in an array of dictonaries with row, column and cell text values
    for recipe in recipes_raw["feed"]["entry"]:
        recipe_cell_data.append(recipe["gs$cell"])
    # creating 2 empty dictonaries for header assignment and model data collection. Counter starts at 2 because row 1 is the header.
    assignment = {}
    recipe_model_data = {}
    recipe_counter = 2
    for recipe_cell in recipe_cell_data:
        if int(recipe_cell["row"]) == recipe_counter:
            # iterate through a single row of spreadsheet data, and put that data into a dictonary with key based on headers and the value based on the spreadsheet cell.
            recipe_model_data[assignment[recipe_cell["col"]]] = recipe_cell["$t"].strip()
        elif int(recipe_cell["row"]) == recipe_counter + 1:
            # after the row has finished parsing, create the model based on the data from the above row, reset the accumluator and continue to iterate.
            Recipe.objects.create_recipe(recipe_model_data)
            recipe_counter += 1
            recipe_model_data = {}
            recipe_model_data[assignment[recipe_cell["col"]]] = recipe_cell["$t"].strip()
        elif recipe_cell["row"] == "1":
            # iterate through first rows of cells and assign a key corrisponding to the column number and a value equal to the text.
            assignment[recipe_cell["col"]] = recipe_cell["$t"].strip().lower().replace(" ", "_")
    # pass all newly created objects to the template
    context = {"new_recipes": Recipe.objects.all()}
    return render(request, 'recipes/load_recipes.html', context)
