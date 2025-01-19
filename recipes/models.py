from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=200)  # Название рецепта
    description = models.TextField()  # Описание рецепта
    ingredients = models.TextField(null=True)  # Ингридиенты
    cooking_steps = models.TextField()  # Шаги приготовления
    cooking_time = models.PositiveIntegerField(help_text="Время приготовления (в минутах)")  # Время приготовления
    image = models.ImageField(upload_to='recipes/images/', blank=True, null=True)  # Изображение
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Автор рецепта
    categories = models.ManyToManyField(Category, related_name='recipes')  # Категории рецепта

    def __str__(self):
        return self.title
