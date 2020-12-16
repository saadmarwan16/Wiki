from django.shortcuts import render
from django.http import Http404

from random import randrange

import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry_name):
    entry = util.get_entry(entry_name)

    content = markdown2.markdown(entry)

    if entry is None:
        raise Http404
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry_name": entry_name,
            "content": content
        })


def random(request):
    entries_name = util.list_entries()
    entry_name = entries_name[randrange(0, len(entries_name))]
    entry = util.get_entry(entry_name)

    content = markdown2.markdown(entry)

    return render(request, "encyclopedia/random.html", {
        "entry_name": entry_name,
        "content": content
    })


def new_page(request):
    if request.method == "POST":
        pass

    return render(request, "encyclopedia/new-page.html")
