import datetime
import json

from django.utils import timezone
from django.test import TestCase

from .models import Recipe, Genre
# Create your tests here.
def make_recipes():
    udon = {"name":"Pork Udon",
            "link":"https://www.bonappetit.com/recipe/stir-fried-udon-with-pork",
            "image_link": "https://assets.bonappetit.com/photos/58c2c2bcb1bf59134d606c65/16:9/w_2560,c_limit/0317-ba-basics-stir-fried-udon-15.jpg",
            "genres": "Asian, Chinese",
            "type":"Entree",
            "cook_time":2,
            "prep_time":3,
            "freezes_well":"FALSE",
            "vegetarian?":"FALSE",
            "could_be_vegetarian?":"TRUE",
            "spicy?":"TRUE",
            "could_be_spicy?":"TRUE",
            "tags":"Pork, Noodles",
            "times_made":0}

    salmon = {"name":"Tuscan Butter Salmon",
            "link":"https://www.delish.com/cooking/recipe-ideas/recipes/a58412/tuscan-butter-salmon-recipe/",
            "genres": "Italian",
            "type":"Entree",
            "cook_time":3,
            "prep_time":2,
            "freezes_well":"FALSE",
            "vegetarian?":"FALSE",
            "could_be_vegetarian?":"FALSE",
            "spicy?":"FALSE",
            "could_be_spicy?":"FALSE",
            "tags":"Fish, Salmon",
            "times_made":0}

    b_squash_soup  = {"name":"Butternut Squash Soup",
            "link":"",
            "genres": "Basic",
            "type":"Soup",
            "cook_time":3,
            "prep_time":3,
            "freezes_well":"TRUE",
            "vegetarian?":"TRUE",
            "could_be_vegetarian?":"TRUE",
            "spicy?":"FALSE",
            "could_be_spicy?":"TRUE",
            "tags":"Vegetables",
            "times_made":0}
    new_recipes = [Recipe.objects.create_recipe(udon), Recipe.objects.create_recipe(salmon), Recipe.objects.create_recipe(b_squash_soup)]
    return new_recipes

class RecipeModelTests(TestCase):
    def test_convert_genre(self):
        udon = make_recipes()[0]

        genres_string = udon.convert_genres()
        self.assertEqual(genres_string, "Asian, Chinese")

    def test_get_tags_as_string(self):
        udon = make_recipes()[0]

        tags = udon.get_tags_as_string()
        expected = "Vegetarian Option, Spicy, Pork, Noodles"
        self.assertEqual(tags, expected)

    def test_get_tags_as_list(self):
        udon = make_recipes()[0]

        tags = udon.get_tags_as_list()
        expected = ["Vegetarian Option", "Spicy", "Pork", "Noodles"]
        self.assertEqual(tags, expected)

    def test_update_times_made(self):
        udon = make_recipes()[0]

        udon.update_times_made()

        udon = Recipe.objects.get(id = 1)
        self.assertEqual(udon.times_made, 1)
        self.assertEqual(udon.last_time_made, timezone.now().date())

    def test_replaces_image_link(self):
        udon, salmon, squash_soup = make_recipes()
        self.assertEqual(udon.image_link, "https://assets.bonappetit.com/photos/58c2c2bcb1bf59134d606c65/16:9/w_2560,c_limit/0317-ba-basics-stir-fried-udon-15.jpg")
        self.assertEqual(salmon.image_link, "/recipes/entree_fish.png")
        self.assertEqual(squash_soup.image_link, "/recipes/soup.png")

    def test_is_staic(self):
        udon, salmon, squash_soup = make_recipes()
        self.assertEqual(udon.is_static(), False)
        self.assertEqual(salmon.is_static(), True)
