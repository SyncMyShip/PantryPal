import pandas as pd
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Recipe
from .forms import RecipesSearchForm, AddRecipeForm
from .utils import get_chart
from django.conf import settings
from django.urls import reverse

@login_required
def home(request):
    return render(request, 'recipes/main.html')

@login_required
def about(request):
    return render(request, 'recipes/about.html')

@login_required
def search(request):
    form = RecipesSearchForm(request.POST or None)
    recipes_df = None
    chart = None

    if request.method == 'POST':
        # Get search criteria
        recipe_name = request.POST.get('recipe_name', '')
        ingredient = request.POST.get('ingredient', '')
        max_cooking_time = request.POST.get('cooking_time', '')
        difficulty = request.POST.get('difficulty', '')
        chart_type = request.POST.get('chart_type', '')

        # Start with all recipes
        qs = Recipe.objects.all()

        # Apply filters if any non-required search parameter is provided
        filter_count = sum([bool(recipe_name), bool(ingredient), bool(max_cooking_time), bool(difficulty)])

        if filter_count > 0:
            if recipe_name:
                qs = qs.filter(name__icontains=recipe_name)
            if ingredient:
                qs = qs.filter(ingredients__icontains=ingredient)
            if max_cooking_time:
                qs = qs.filter(cooking_time__lte=max_cooking_time)
            if difficulty:
                qs = qs.filter(difficulty=difficulty)

        # If there are results, prepare the DataFrame and chart
        if qs:
            recipes_df = pd.DataFrame(qs.values())

            difficulties = [recipe.difficulty for recipe in qs]  # Calculate difficulty for each recipe
            recipes_df['difficulty'] = difficulties
            
            # Generate chart only if the checkbox is checked and a chart type is provided
            if chart_type and recipes_df.shape[0] > 0:
                # Use difficulty counts for the pie chart
                difficulty_counts = recipes_df['difficulty'].value_counts()
                labels = difficulty_counts.index.tolist() 
                values = difficulty_counts.values.tolist()  

                # Generate the chart
                chart = get_chart(chart_type, recipes_df, labels=labels, values=values)

            # Convert to HTML with links
            recipes_df['name'] = '<a href="' + recipes_df['id'].apply(lambda id: reverse('recipes:detail', kwargs={'pk': id})).astype(str) + '">' + recipes_df['name'] + '</a>'
            recipes_df['picture'] = '<img src="' + settings.MEDIA_URL + recipes_df['pic'] + '" alt="Recipe Image" style="width:100px;height:auto;">'
            recipes_df = recipes_df[['name', 'picture', 'ingredients', 'cooking_time', 'difficulty']].to_html(escape=False, index=False)

    # Prepare context data to send to template
    context = {
        'form': form,
        'recipes_df': recipes_df,
        'chart': chart,
        'search_button_label': 'Search'
    }

    return render(request, 'recipes/search.html', context)

@login_required
def add_recipe(request):
    # handle data input and pic file upload
    add_recipe = AddRecipeForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and add_recipe.is_valid():
        recipe_instance = add_recipe.save(commit=False)
        # recipe_instance.difficulty = recipe_instance.calculate_difficulty()
        recipe_instance.save()
        response = redirect("recipes:list")

        if response.status_code == 302:
            messages.success(request, "Recipe successfully added!")
        return response
    
    context = {"add_recipe": add_recipe}
    return render(request, "recipes/add_recipe.html", context)


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipes_home.html'

class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/recipe-details.html'
