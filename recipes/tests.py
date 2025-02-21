from django.test import TestCase
from .models import Recipe
from .forms import RecipesSearchForm
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class RecipeModelTest(TestCase):

    def setUpTestData():
       # Set up non-modified objects used by all test methods
        Recipe.objects.create(
           name='Pancakes', 
           cooking_time=15,
           ingredients='flour, milk, oil, eggs, vanilla, banking soda, baking powder, sugar, salt',
           difficulty='intermediate',
           comments='test comment'
        )
       
    def test_recipe_name(self):
       # Get a recipe object to test
        # recipe = Recipe.objects.get(name='Pancakes')
        recipe = Recipe.objects.get(id=1)

        # Get the metadata for the 'name' field and use it to query its data
        field_label = recipe._meta.get_field('name').verbose_name

        # Compare the value to the expected result
        self.assertEqual(field_label, 'name')


    def test_ingredients_max_length(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Get the metadata for the 'ingredients' field and use it to query its max_length
        max_length = recipe._meta.get_field('ingredients').max_length

        # Compare the value to the expected result i.e. 255
        self.assertEqual(max_length, 255)


    def test_difficulty_max_length(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Get the metadata for the 'difficulty' field and use it to query its max_length
        max_length = recipe._meta.get_field('difficulty').max_length

        # Compare the value to the expected result i.e. 20
        self.assertEqual(max_length, 20)


    def test_cooking_time_is_integer(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Check that cooking_time has the type int
        self.assertIsInstance(recipe.cooking_time, int)

    def test_difficulty_cal(self):
        recipe = Recipe.objects.get(id=1)

        self.assertEqual(recipe.difficulty, "intermediate")

    def test_get_absolute_url(self):
        recipe = Recipe.objects.get(id=1)

        self.assertEqual(recipe.get_absolute_url(), "/list/1")


class RecipeFormTest(TestCase):
    def test_recipe_name_field(self):
        form_data = {'recipe_name': 'Pancake'}
        form = RecipesSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Exceed max length
        form_data = {'recipe_name': 'A' * 121}
        form = RecipesSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('recipe_name', form.errors)

    def test_ingredient_field(self):
        form_data = {'ingredient': 'Syrup'}
        form = RecipesSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Exceed max length
        form_data = {'ingredient': 'A' * 121}
        form = RecipesSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('ingredient', form.errors)

    def test_cooking_time_field(self):
        form_data = {'cooking_time': 45}
        form = RecipesSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Invalid input value - string
        form_data = {'cooking_time': 'invalid'}
        form = RecipesSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('cooking_time', form.errors)

        # Invalid input value - float
        form_data = {'cooking_time': 15.5}
        form = RecipesSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('cooking_time', form.errors)

    def test_difficulty_field(self):
        form_data = {'difficulty': 'hard'}
        form = RecipesSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Exceed max length
        form_data = {'difficulty': 'invalid difficulty'}
        form = RecipesSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('difficulty', form.errors)


class AddRecipeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_add_recipe_view_get(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('recipes:add_recipe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/add_recipe.html')

    def test_add_recipe_view_post_valid(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('recipes:add_recipe'), {
            'name': 'Pancakes',
            'ingredients': 'flour, milk, oil, eggs, vanilla, banking soda, baking powder, sugar, salt',
            'cooking_time': 15,
            'difficulty': 'Intermediate',
            'pic': ''
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recipes:list'))
        self.assertTrue(Recipe.objects.filter(name='Pancakes').exists())

    def test_add_recipe_view_post_invalid(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('recipes:add_recipe'), {
            # test with empty request
            'name': '',
            'ingredients': '',
            'cooking_time': '',
            'difficulty': '',
            'pic': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/add_recipe.html')
