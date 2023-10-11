from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("recipe/<int:id>/", views.recipePage, name="recipe"),
    path("add-recipe/", views.addRecipe, name="addrecipe"),
    path("recipes", views.recipeSelection, name="recipes"),
]