from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util

from markdown2 import Markdown

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


