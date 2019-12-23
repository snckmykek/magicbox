from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


class Recipes(BoxLayout):
    Builder.load_file(r'contents/recipes/recipes.kv')


RecipesBox = Recipes()
