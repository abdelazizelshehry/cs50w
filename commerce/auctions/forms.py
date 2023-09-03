from django import forms
from .models import AuctionsListing, Bid, Comment
from django.forms import ModelForm
class ListingForm(forms.ModelForm):
    class Meta:
        model = AuctionsListing
        exclude = ('user',)
        fields = ['title', 'imageurl', 'starting_bid', 'catagory', 'discription'] 
        widgets = {
    'title' : forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Title",
        "autofocus": True
    }),
    'imageurl' : forms.URLInput(attrs={
        "class": "form-control",
        "placeholder": "ImageURL",
        "autofocus": True,
    }),
    
    'starting_bid' : forms.NumberInput(attrs={
        "class": "form-control",
        "placeholder": "Starting Bid",
        "autofocus": True,
        "min": "15.00",
        "max": "9999999.99",
        "step": "00.05",
    }),
    'catagory' : forms.Select(attrs={
        "class": "form-control",
        "placeholder": "Which Catagory..!",
        "autofocus": True,
    }),
    'discription' : forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Discripe your Listing..",
        "autofocus": True,
        "rows": '4'
    })
        }
    
class BidForm(forms.ModelForm):
    class Meta: 
        model = Bid
        exclude = ('user', 'listingid')
        fields = ['bid']
        widgets = {
            "bid" : forms.NumberInput(attrs={
                "style" : "width: 20%; height: 40px; background-color:rgb(125, 218, 218); font-weight: bold;",
                "placeholder": "Bid a price",
                "autofocus": True,
            })
        }
class CommentForm(forms.ModelForm):
    class Meta: 
        model = Comment
        exclude = ('user', 'time', 'listingid')
        fields = ['comment']
        widgets = {
            "comment" : forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Write Comment..",
                "autofocus": True,
                "rows": '3'
            })
        }