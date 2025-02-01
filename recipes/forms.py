from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Recipe


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'cooking_steps', 'cooking_time', 'image', 'categories']
        widgets = {
            'categories': forms.SelectMultiple,
        }


class RecipeSearchForm(forms.Form):
    query = forms.CharField(max_length=300, required=False, label='Search Recipes')
