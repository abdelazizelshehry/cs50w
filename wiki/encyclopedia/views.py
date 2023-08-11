from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import random
from markdown2 import Markdown
from . import util
from .form import CatagoryForm
from .models import Catagory, Topics


class Search(forms.Form):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={
        "class": "search",
        "placeholder": "Search Encyclopedia"
    }))


class NewPage(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        "class": "input-group-text",
        "placeholder": "title",
    }))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "enter the content of yours"
    }))


class EditPage(forms.Form):
    editcontent = forms.CharField(label="", widget=forms.Textarea(attrs={
        "class": "form-control"
    }))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "form_search": Search(),
        "entries": util.list_entries(),
        "objects" : Catagory.objects.all(),
    })


def reqpage(request, name):

    entry = util.get_entry(name)
    if entry != None:
        convert = Markdown().convert(entry)
        return render(request, "encyclopedia/reqpage.html", {
            "reqpage": convert,
            "title": name
        })
    else: 
        return None

def search(request):
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            entry = util.get_entry(name)
            if entry:
                return HttpResponseRedirect(reverse("encyclopedia:reqpage", args=[name]))
            else:
                related_titles = util.related_titles(name)
                return render(request, "encyclopedia/search.html", {
                    "title": name,
                    "related_titles": related_titles,
                    "search_form": Search()
                })
    else:
        return HttpResponseRedirect(reverse("encyclopedia/index.html"))


def create(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
        else:
            messages.error(request, 'your entry is not valid please try again')
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
        if util.get_entry(title):
            messages.error(request, 'The page Title is already exists')
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
        else:
            util.save_entry(title, content)
            messages.success(request, f"The {title} Created successfully!")
            return HttpResponseRedirect(reverse("encyclopedia:reqpage", args=[title]))
    else:
        return render(request, "encyclopedia/create.html", {
            "form": NewPage()
        })


def edit(request, name):
    entry = util.get_entry(name)
    if request.method == "POST":
        form = EditPage(request.method)
        if form.is_valid():
            content = form.cleaned_data['editcontent']
            if content == entry:
                messages.error(request, "You change none in the Content")
            else:
                util.save_entry(name, content)
                messages.success(request, f"the {name} Edited Successfully!")
                return HttpResponseRedirect(reverse("encyclopedia:reqpage", args=[name]))
    else:
        return render(request, "encyclopedia/edit.html", {
            "title": name,
            "form": EditPage(initial={'editcontent': entry})
        })


def Random(request):
    titles = util.list_entries()
    entry = random.choice((titles))

    return HttpResponseRedirect(reverse("encyclopedia:reqpage", args=[entry]))

def addcatagory(request): 
    if request.method == "POST": 
        form = CatagoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("encyclopedia:index"))
    else : 
        return render(request, "encyclopedia/createcatagory.html", {
            "form" : CatagoryForm()
        })
def catagory(request, name): 
    if request.user: 
        try :
            topics = Topics.objects.get(name=name)
            if not topics : 
                return render(request, "no topics")
            else : 
                return render(request, "encyclopedia/topics.html", {
                    "name" : name, 

                })
        except :
            return HttpResponseRedirect(reverse("encyclopedia:index"))

def deletecatagory(request):
    return render(request)
def editcatagory(request): 
    return render(request)