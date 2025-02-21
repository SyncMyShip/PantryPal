from django import forms
from .models import Recipe

CHART_CHOICES = (
    ('#1', 'Bar chart'),
    ('#2', 'Pie chart'),
    ('#3', 'Line chart'),
)

class RecipesSearchForm(forms.Form):
    recipe_name = forms.CharField(max_length=120, required=False, label='Recipe Name')
    ingredient = forms.CharField(max_length=120, required=False, label='Ingredient')
    cooking_time = forms.IntegerField(required=False, label='Max Cooking Time (min)')
    difficulty = forms.ChoiceField(
        choices=[
            ('', 'Select Difficulty'),
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('intermediate', 'Intermediate'),
            ('hard', 'Hard')
        ],
        required=False,
        label='Difficulty'
    )
    chart_type = forms.ChoiceField(choices=CHART_CHOICES, required=False, label='Chart Type')


# ensure Form is mapped to model 
class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "name",
            "ingredients",
            "cooking_time",
            "comments",
            "pic"
        ]