from django.forms.forms import Form
from django.forms.formsets import INITIAL_FORM_COUNT
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from . import util
import secrets  

from markdown2 import Markdown

from django import forms

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry title", widget=forms.TextInput(attrs={'class' : 'form-control'}))
    content = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),

    })
def entry(request, entry):
    markdowner = Markdown()
    entrypage = util.get_entry(entry)
    if entrypage is None:
        return render(request, "encyclopedia/Error404.html", {
            "entryTitle"  : entry
        }) 
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry" : markdowner.convert(entrypage),
            "entryTitle" : entry
        })

def search(request):
    value = request.GET.get('q', '')
    if (util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={'entry' : value}))
    else:
        subStringEntries = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                subStringEntries.append(entry)
        
        return render(request, "encyclopedia/index.html", {
            "entries": subStringEntries,
            "search" : True,
            "value"  : value
        })

def newEntry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if (util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry' : title}))
            else: 
                return render(request,"encyclopedia/newEntry.html",{
                    "form" : form,
                    "existing": True,
                    "entry" : title
                })
        else:
            return render(request,"encyclopedia/newEntry.html", {
                "form" : form,
                "existing" : False
            })
    else:
        return render(request,"encyclopedia/newEntry.html",{
            "form" : NewEntryForm(),
            "existing" : False
        })

def edit(request, entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/Error404.html", {
            "entryTitle" : entry
        })
    else:
        form = NewEntryForm()
        form.fields["title"].initial = entry
        form.fields["content"].initial = entryPage
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["edit"].initial = True
        return render(request,"encyclopedia/newEntry.html", {
            "form" : form,
            "edit" : form.fields["edit"].initial,
            "entryTitle": form.fields["title"].initial 
        })

def random(request):
    listofitem = util.list_entries()
    randomentry = secrets.choice(listofitem)
    return HttpResponseRedirect(reverse("entry",kwargs={'entry': randomentry}))

