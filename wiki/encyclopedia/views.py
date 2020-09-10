from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
import random


from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def search(request):
    query = request.GET["q"]
    entries = util.list_entries()
    if query in entries:
        return HttpResponseRedirect(reverse('entry', kwargs={
            'entry': query
        }))
    else:
        results = []
        for entry in entries:
            if query in entry:
                results.append(entry)
        return render(request, "encyclopedia/search.html", {
            "results": results, "query": query
        })

def entry(request, entry):
    body_md = util.get_entry(entry)
    body = None
    if body_md is not None:
        body = markdown2.markdown(body_md)
    else:
        return render(request, "encyclopedia/error.html", {
            "code": 0, "entry": entry})
    return render(request, "encyclopedia/entry.html", {
        "entry": entry, "body": body
    })
        
def newpage(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["body"]
        entries = util.list_entries()
        if title in entries:
            return render(request, "encyclopedia/error.html", {
                "code": 1, "entry": title
            })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('entry', kwargs={
                'entry': title
            }))
    return render(request, "encyclopedia/newpage.html")
    
def edit(request, title):
    if request.method == "POST":
        body = request.POST["body"]
        util.save_entry(title, body)
        return HttpResponseRedirect(reverse('entry', kwargs={ 
            'entry': title
        }))
    else:
        body = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title":title, "body":body
        })
    
def randompage(request):
    entries = util.list_entries()
    nr_entries = len(entries)
    rand = random.randint(0, nr_entries - 1)
    entry = entries[rand]
    return HttpResponseRedirect(reverse('entry', kwargs={
        'entry': entry
    }))

