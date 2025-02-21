from django.db import models
from django.shortcuts import reverse

# Create your models here.

class Recipe(models.Model):
    name= models.CharField(max_length=50)
    cooking_time= models.IntegerField()
    ingredients= models.TextField(max_length=255)
    # difficulty= models.CharField(
    #     max_length=20,
    #     choices=[
    #         ('easy', 'Easy'),
    #         ('medium', 'Medium'),
    #         ('intermediate', 'Intermediate'),
    #         ('hard', 'Hard')
    #     ]
    # )
    comments= models.TextField(blank=True, null=True)
    pic = models.ImageField(upload_to='recipes', default='no_picture.jpg')

    def get_absolute_url(self):
        return reverse('recipes:detail', kwargs={'pk': self.pk})

    # calculate difficulty of recipe using cooking time and number of ingredients
    def difficulty(self):
        ingredients = self.ingredients.split(', ')
        if self.cooking_time < 10 and len(ingredients) < 4:
            difficulty = 'Easy'
        elif self.cooking_time < 10 and len(ingredients) >= 4:
            difficulty = 'Medium'
        elif self.cooking_time >= 10 and len(ingredients) < 4:
            difficulty = 'Intermediate'
        elif self.cooking_time >= 10 and len(ingredients) >= 4:
            difficulty = 'Hard'
        return difficulty

    def __str__(self):
        return f"{self.name} - {self.cooking_time}(min)"
