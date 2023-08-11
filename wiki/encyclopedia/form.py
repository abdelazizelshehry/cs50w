from django import forms 
from .models import Catagory, Topics
from django.forms import ModelForm

class CatagoryForm(forms.ModelForm):
    class Meta: 
        model = Catagory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={ 
                "placeholder" : "Name", 
                "autofocus" : True, 
                "style" : "width:50%; margin-left:20%;"
            })
        }