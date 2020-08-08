from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.http import Http404
from django.core.files.storage import default_storage
from markdown2 import Markdown
from django.contrib import messages
from django import forms
import random

import os

from . import util

class NewEntryForm(forms.Form):
    new_entry = forms.CharField(label="Entry Title")
    new_content = forms.CharField(label="Content", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    if request.method == "GET":
        import markdown2
        entry = util.get_entry(title)
        if title == "newentry":
            newentry(request)
        elif entry is not None:
            mrkdown = markdown2.markdown(entry)
            return render(request, "encyclopedia/otherpages.html", {
                "title": title,
                "body": mrkdown })
        else:
            raise Http404("Page does not exist")
        return render(request, '404.html')
    elif request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        util.save_entry(title, content)
        return HttpResponseRedirect(f"{title}")

  
def newentry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["new_entry"]
            content = form.cleaned_data["new_content"]
            current_entries = util.list_entries()
            if title not in current_entries:
                util.save_entry(title, content)
                return HttpResponseRedirect(f"wiki/{title}")
            else:
                return render(request, 'alreadyexists.html')

                
    else:
        return render(request, "encyclopedia/newpage.html",
        {'form': NewEntryForm})


def editentry(request):
        if request.method == "GET":
            x = request.GET.get('edit')
            entry = util.get_entry(x)
            return render(request, "encyclopedia/editpage.html",
            {'contents': entry , 'existtitle': x})


def randomentry(request):
    currentlist = util.list_entries()
    randomchoice = random.choice(currentlist)
    return HttpResponseRedirect(f"wiki/{randomchoice}")


def search(request):
     x = request.GET.get('q')
     currentlist = util.list_entries()
     if x in currentlist:
        return HttpResponseRedirect(f"wiki/{x}")
            
     if x not in currentlist:
            res = [i for i in currentlist if x in i]
            return render(request, "encyclopedia/search.html",
            {
                "entries": res,
                "subs" : x
            })