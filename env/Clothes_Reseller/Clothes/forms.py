from django import forms
from django.urls import reverse_lazy
from .models import Clothing_Post

class CreateClothingList(forms.ModelForm):
    class Meta:
        model = Clothing_Post
        fields = ["id","Name", "Description", "Image", "Price"]
        exclude = ["User"]