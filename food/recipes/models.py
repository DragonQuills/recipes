from django.db import models

# Create your models here.
class Recipe(models.Model):
    food_name = models.CharField(max_length=200)
    link = models.URLField(max_length=2083, blank = True)
    image_link = models.URLField(max_length=2083, blank = True)

    # genres will be a list, it will need
    # to be decoded using json
    genres = models.CharField(max_length = 500)
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

    def __str__(self):
        return self.food_name
