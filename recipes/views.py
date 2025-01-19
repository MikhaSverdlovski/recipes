from django.shortcuts import render

# Create your views here.

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
import random
from .models import Recipe, Category
from .forms import RecipeForm, RecipeSearchForm
from django.contrib.auth.decorators import login_required

def home(request):
    recipes = Recipe.objects.all()
    random_recipes = random.sample(list(recipes), min(len(recipes), 5))
    return render(request, 'recipes/home.html', {'recipes': random_recipes})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    instructions = recipe.cooking_steps.split("\\n")
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe, 'instructions': instructions})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически логиним пользователя после регистрации
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'recipes/register.html', {'form': form})


@login_required
def add_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user  # Привязываем автора
            recipe.save()  # Сохраняем рецепт
            form.save_m2m()  # Сохраняем связь с категориями
            return redirect('home')  # Перенаправляем на главную страницу
    else:
        form = RecipeForm()

    return render(request, 'recipes/add_recipe.html', {'form': form})

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user  # Привязываем автора (если редактируем)
            recipe.save()  # Сохраняем рецепт
            form.save_m2m()  # Сохраняем связь с категориями
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipes/edit_recipe.html', {'form': form, 'recipe': recipe})


def recipe_search(request):
    form = RecipeSearchForm(request.GET)
    recipes = Recipe.objects.all()

    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            recipes = recipes.filter(title__icontains=query)

    return render(request, 'recipes/recipe_search.html', {'form': form, 'recipes': recipes})