from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, get_object_or_404
from .models import Recipe
import random

def home(request):
    recipes = Recipe.objects.all()
    random_recipes = random.sample(list(recipes), min(len(recipes), 5))
    return render(request, 'recipes/home.html', {'recipes': random_recipes})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})
