from django.db import models

# Create your models here.

class Ingredient(models.Model):
    ingredientName = models.CharField(max_length = 30)

    def __str__(self):
        return self.ingredientName

class Meal(models.Model):
    mealName = models.CharField(max_length=50)
    timeToCook = models.CharField(max_length=20)
    course = models.CharField(max_length = 20)
    steps = models.TextField()
    
    method = models.ManyToManyField(Ingredient, through="Method")
    
    def __str__(self):
        return self.mealName
    
class Method(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="meal")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="ingredient")

    def __str__(self):
        
        return self.meal.mealName