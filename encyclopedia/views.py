from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from random import randrange
from os import listdir, path
import re

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
        def escape(s):
            """
            Escape special characters.

            https://github.com/jacebrowning/memegen#special-characters
            """
            for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                            ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
                s = s.replace(old, new)
            return s
        return render(request, "encyclopedia/apology.html",{
            "top": 404,
            "bottom": escape("The page you tried to acces does not exist")
        })
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
        title = request.POST["title"].capitalize()

        if not title.endswith(".md"):
            title = title + ".md"

        if title in listdir("entries"):
            def escape(s):
                """
                Escape special characters.

                https://github.com/jacebrowning/memegen#special-characters
                """
                for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                                ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
                    s = s.replace(old, new)
                return s
            return render(request, "encyclopedia/apology.html",{
                "top": 404,
                "bottom": escape("This file already exists please enter a different file name")
            })
        else:
            content_path = path.join("entries", title)
            output_file = open(content_path, "w")
            content = request.POST["content"]
            output_file.write(content)
            output_file.close()

            return HttpResponseRedirect(reverse("index"))

    return render(request, "encyclopedia/new-page.html")


def search(request):
    entry_name = request.POST["q"]
    entries = util.list_entries()
    contents = list()

    if entry_name.casefold() in (entry.casefold() for entry in entries):
        content = util.get_entry(entry_name)
        
        return HttpResponseRedirect(reverse("entry", kwargs={"entry_name": entry_name.capitalize()}))

    for string in entries:
        if re.search(entry_name, string, re.IGNORECASE):
            contents.append(string)

    return render(request, "encyclopedia/search.html", {
        "contents": contents
    })

def edit_page(request, filename):
    if request.method == "POST":
        content = request.POST["content"]
        file_path = path.join("entries", filename + ".md")
        print(file_path)
        fileptr = open(file_path, "w")
        fileptr.write(content)
        fileptr.close()

        return HttpResponseRedirect(reverse("entry", kwargs={"entry_name": filename}))
    else:
        file_path = path.join("entries", filename + ".md")
        fileptr = open(file_path, "r")
        content = fileptr.read()
        fileptr.close()

        return render(request, "encyclopedia/edit-page.html", {
            "filename": filename,
            "content": content
        })
