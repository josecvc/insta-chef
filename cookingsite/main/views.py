from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import *
from .forms import *
from bs4 import BeautifulSoup
import json, requests


# Create your views here.


def home(response):
    return render(response, "main/home.html")

def recipeSelection(response):
    
    myMeal = Meal.objects.all().order_by("mealName")
    
    
    
    return render(response, "main/recipies.html", {"meals":myMeal})

def recipePage(response, id):      
    myMeal = Meal.objects.get(id = id)
    steps = myMeal.steps
    steps = steps.split(":")
    ingredients = [
        Ingredient.objects.get(id=id) for id in 
                   [
                       method.ingredient_id for method in Method.objects.all().filter(meal_id=id)
                    ]
    ]
  
    return render(response, "main/recipebase.html", {"meal": myMeal,"ingredients": ingredients, "steps":steps})

def about(response):
    return render(response, "main/about.html")

def addRecipe(response):
    if response.method == "POST":
        formRecipe = AddNewRecipe(response.POST)
        formScrape = GetTheURL(response.POST)
        print("HI", formRecipe.is_valid())
        if formRecipe.is_valid():
            
            # Process data
            data = formRecipe
            name = data.cleaned_data["mealName"]
            time = data.cleaned_data["timeToCook"]
            course = getCourse(int(data.cleaned_data["course"]) - 1)
            steps = data.cleaned_data["steps"]
            ingredients = data.cleaned_data["ingredients"]
            
            # Make the mea
            myMeal = Meal.objects.create(mealName=name,    timeToCook=time, 
                                course = course , 
                                steps = steps)
            myMeal.save()
    
            # Parse the ingredients
            ingredients = parseInformation(ingredients)
            
            for ingredient in ingredients: # Make the ingredient
                try:
                    theIngredient = Ingredient.objects.get(ingredientName=ingredient)
                except: # The ingredient may not exist yet
                    theIngredient = Ingredient.objects.create(ingredientName=ingredient)
                    theIngredient.save()

                myMethod = Method.objects.create(meal=myMeal, ingredient=theIngredient) # Make the method
                myMethod.save()
            
            return HttpResponseRedirect(f"recipe/{myMeal.id}")
        elif formScrape.is_valid():
            
            url = formScrape["url"]
            url = url.value()

            impo = scrapeCourse(url)
            
            name = impo["name"]
            
            ingredients = impo["recipeIngredient"]
            

            instructions = ":".join([instruction["text"].replace("\n", "") for instruction in impo["recipeInstructions"]])
            
            # We need to make it so that the website will reload with the information there without saving so that the user can add the time and the course
            context = {}
            
            print(ingredients)
            context["mealName"] = name
            context["ingredients"] = ":".join([ingredient for ingredient in ingredients])
            context["steps"] = instructions
            context["timeToCook"] = ""
            context["course"] = ""
            formRecipe = AddNewRecipe(context)
            formScrape = GetTheURL()
    else:
        formRecipe = AddNewRecipe()
        formScrape = GetTheURL()
        
    return render(response, "main/addrecipe.html", {"formrecipe":
        formRecipe, "formscrape":formScrape})





def parseInformation(info):
    info = info.split(":")
    return info

def getCourse(choice):
    choices = ((1, "Main Course"),
            (2, "Starter"), 
            (3, "Dessert"),
            (4, "Side Dish"),
            (5, "Snack")
            )
    return choices[choice][1]

def scrapeCourse(url):
    parser = "html.parser"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, parser)
        
    file = json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))
    
    return file[1]


