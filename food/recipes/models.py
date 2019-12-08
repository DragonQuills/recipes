from django.db import models

# Create your models here.
class Recipe(models.Model):
    recipe_name = models.CharField(max_length=200)
    link = models.URLField(max_length=2083)
    vegetarian = models.BooleanField()
    cook_time = models.IntegerField()
    def __str__(self):
        return self.recipe_name
