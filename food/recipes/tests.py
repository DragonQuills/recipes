from django.test import TestCase

from .models import Recipe, Genre
# Create your tests here.

class RecipeModelTests(TestCase):
    def test_convert_genre(self):
        udon = Recipe(food_name = "Pork Udon", link = "https://www.bonappetit.com/recipe/stir-fried-udon-with-pork", image_link = "https://assets.bonappetit.com/photos/58c2c2bcb1bf59134d606c65/16:9/w_2560,c_limit/0317-ba-basics-stir-fried-udon-15.jpg", type = "Entree", cook_time=2, prep_time = 3, freezes_well = False, vegetarian = False, could_be_vegetarian=True, spicy = True, could_be_spicy = True, tags = "")

        udon.save()
        udon.genres.create(name = "Asian")
        udon.genres.create(name = "Chinese")

        genres_string = udon.convert_genres()
        self.assertEqual(genres_string, "Asian, Chinese")
