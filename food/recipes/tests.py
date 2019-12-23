import datetime
import json

from django.utils import timezone
from django.test import TestCase

from .models import Recipe, Genre
# Create your tests here.
def make_recipes():
    udon = Recipe(food_name = "Pork Udon", link = "https://www.bonappetit.com/recipe/stir-fried-udon-with-pork", image_link = "https://assets.bonappetit.com/photos/58c2c2bcb1bf59134d606c65/16:9/w_2560,c_limit/0317-ba-basics-stir-fried-udon-15.jpg", type = "Entree", cook_time=2, prep_time = 3, freezes_well = False, vegetarian = False, could_be_vegetarian=True, spicy = True, could_be_spicy = True, tags = json.dumps(["Pork", "Noodles"]), times_made = 0)

    udon.save()
    return udon

class RecipeModelTests(TestCase):
    def test_convert_genre(self):
        udon = make_recipes()

        udon.genres.create(name = "Asian")
        udon.genres.create(name = "Chinese")

        genres_string = udon.convert_genres()
        self.assertEqual(genres_string, "Asian, Chinese")

    def test_get_tags_as_string(self):
        udon = make_recipes()

        tags = udon.get_tags_as_string()
        expected = "Vegetarian Option, Spicy, Pork, Noodles"
        self.assertEqual(tags, expected)

    def test_get_tags_as_list(self):
        udon = make_recipes()

        tags = udon.get_tags_as_list()
        expected = ["Vegetarian Option", "Spicy", "Pork", "Noodles"]
        self.assertEqual(tags, expected)

    def test_update_times_made(self):
        udon = make_recipes()

        udon.update_times_made()

        udon = Recipe.objects.get(id = 1)
        self.assertEqual(udon.times_made, 1)
        self.assertEqual(udon.last_time_made, timezone.now().date())
