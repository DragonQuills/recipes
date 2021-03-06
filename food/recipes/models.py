import datetime
import json
import re

from django.db import models
from django.utils import timezone


# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name

class RecipeManager(models.Manager):
    def create_recipe(self, data):
        
        if data.get("image_link") == None:
            image_url = {
                            "Dessert": "/recipes/dessert.png",
                            "Drink": "/recipes/drink.png",
                            "Side": "/recipes/entree_vegetarian.png",
                            "Salad": "/recipes/salad.png",
                            "Soup": "/recipes/soup.png",
                         }
            if data.get("type") == "Entree":
                if data.get("vegetarian") == 'TRUE':
                    image_url["Entree"] = "/recipes/entree_vegetarian.png"
                elif "Fish" in data.get("tags").split(", "):
                    image_url["Entree"] = "/recipes/entree_fish.png"
                else:
                    image_url["Entree"] = "/recipes/entree_meat.png"
            data["image_link"] = image_url[data.get("type")]

        new_recipe, created = self.get_or_create(
            name = data.get("name"),
            link = data.get("link",""),
            image_link = data.get("image_link",""),
            type = data.get("type"),
            cook_time = int(data.get("cook_time",0)),
            prep_time = int(data.get("prep_time",0)),
            freezes_well = data.get("freezes_well") == "TRUE",
            vegetarian = data.get("vegetarian") == "TRUE",
            could_be_vegetarian = data.get("could_be_vegetarian?") == "TRUE",
            spicy = data.get("spicy?") == "TRUE",
            could_be_spicy = data.get("could_be_spicy?") == "TRUE",
            tags = json.dumps(data.get("tags","").split(", ")),
            times_made = int(data.get("times_made",0)),
            last_time_made = data.get("last_time_made",None)
        )

        if created:
            genres = data.get("genres","").split(", ")
            for genre in genres:
                recipe_genre, created = Genre.objects.get_or_create(name = genre)
                new_recipe.genres.add(recipe_genre)
        return new_recipe

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    link = models.URLField(max_length=2083, blank = True)
    image_link = models.URLField(max_length=2083, blank = True)

    genres = models.ManyToManyField(Genre)
    type = models.CharField(max_length = 200)

    cook_time = models.IntegerField()
    prep_time = models.IntegerField()

    freezes_well = models.BooleanField(default = False)
    vegetarian = models.BooleanField(default = False)
    could_be_vegetarian = models.BooleanField(default = False)
    spicy = models.BooleanField(default = False)
    could_be_spicy = models.BooleanField(default = False)

    # tags will be a list, it will need
    # to be decoded (and encodeded?) using json
    tags = models.CharField(max_length = 500, blank = True)

    times_made = models.IntegerField(default = 0)
    last_time_made = models.DateField(null = True, blank = True)

    objects = RecipeManager()

    def __str__(self):
        return self.name

    def convert_cook_time(self):
        cook_time_conversion = {
            0: "No cooking required",
            1: "1 to 15 minutes",
            2: "15 to 30 minutes",
            3: "30 to 45 minutes",
            4: "45 to 75 minutes",
            5: "1 to 2 hours",
            6: "Slow-cooker recipe, anywhere from 2 to 12 hours"
        }
        return cook_time_conversion[self.cook_time]

    def convert_prep_time(self):
        prep_time_conversion = {
            1: "1 to 5 minutes",
            2: "5 to 15 minutes",
            3: "15 to 30 minutes",
            4: "30 to 45 minutes",
            5: "45 to 75 minutes",
            6: "Requires advanced preparation, like marinating for several hours or soaking overnight."
        }
        return prep_time_conversion[self.prep_time]

    def convert_genres(self):
        all_genres = ""
        genres = self.genres.all()
        for counter, genre in enumerate(genres):
            all_genres += genre.name
            if not counter == len(genres)-1:
                all_genres += ", "
        return all_genres

    def get_tags_as_list(self):
        all_tags = []
        if self.vegetarian:
            all_tags.append("Vegetarian")
        elif self.could_be_vegetarian:
            all_tags.append("Vegetarian Option")

        if self.spicy:
            all_tags.append("Spicy")
        elif self.could_be_spicy:
            all_tags.append("Spicy Option")

        if self.tags != "":
            tags = json.loads(self.tags)
            all_tags += tags

        return all_tags

    def get_tags_as_string(self):
        all_tags = self.get_tags_as_list()
        tags_string = ""
        for counter, tag in enumerate(all_tags):
            tags_string += tag
            if not counter == len(all_tags)-1:
                tags_string += ", "
        return tags_string

    def update_times_made(self):
        self.times_made += 1
        self.last_time_made = timezone.now().date()
        self.save()

    def is_static(self):
        if re.search('^/recipes/', self.image_link) == None:
            return False
        return True
