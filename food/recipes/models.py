from django.db import models

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    food_name = models.CharField(max_length=200)
    link = models.URLField(max_length=2083, blank = True)
    image_link = models.URLField(max_length=2083, blank = True)

    # genres will be a list, it will need
    # to be decoded using json
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

    def __str__(self):
        return self.food_name
    def convert_cook_time(self):
        if self.cook_time == 0:
            return "No cooking required"
        elif self.cook_time == 1:
            return "1 to 15 minutes"
        elif self.cook_time == 2:
            return "15 to 30 minutes"
        elif self.cook_time == 3:
            return "30 to 45 minutes"
        elif self.cook_time == 4:
            return "45 to 75 minutes"
        elif self.cook_time == 5:
            return "1 to 2 hours"
        else:
            return "Slow-cooker recipe, anywhere from 2 to 12 hours"

    def convert_prep_time(self):
        if self.prep_time == 1:
            return "1 to 5 minutes"
        elif self.prep_time == 2:
            return "5 to 15 minutes"
        elif self.prep_time == 3:
            return "15 to 30 minutes"
        elif self.prep_time == 4:
            return "30 to 45 minutes"
        elif self.prep_time == 5:
            return "45 to 75 minutes"
        else:
            return "Requires advanced preparation, like marinating for several hours or soaking overnight."

    def convert_genres(self):
        all_genres = ""
        genres = self.genres.all()
        for counter, genre in enumerate(genres):
            all_genres += genre.name
            if not counter == len(genres)-1:
                all_genres += ", "
        return all_genres
