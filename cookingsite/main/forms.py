from django import forms

choices = (
            (1, "Main Course"),
            (2, "Starter"), 
            (3, "Dessert"),
            (4, "Side Dish"),
            (5, "Snack")
            )

class AddNewRecipe(forms.Form):
    mealName = forms.CharField(max_length=128, widget=forms.TextInput(attrs = {"placeholder": "Your Recipe Name..."}))
    ingredients = forms.CharField(widget=forms.Textarea(attrs = {"placeholder": "Ingredients..."}), )
    steps = forms.CharField(widget=forms.Textarea(attrs = {"placeholder": "The Recipe Instructions..."}), )
    timeToCook = forms.CharField(max_length=10,widget=forms.TextInput(attrs = {"placeholder": "How much time needed..."}) )
    course = forms.ChoiceField(choices=choices)
    
class GetTheURL(forms.Form):
    url = forms.URLField(max_length=2000, widget=forms.URLInput(attrs = {"placeholder": "URL..."}))