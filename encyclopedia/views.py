from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from random import randrange
from os import listdir, path
import re

import markdown2

from . import util


# Displays the home page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Display an entry page
def entry(request, entry_name):

    # Get an entry and then convert the content from markdown to HTML
    entry = util.get_entry(entry_name)
    content = markdown2.markdown(entry)

    # User entered a wrong entry name
    if entry is None:

        # Return an error page
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

    # User entered a correct entry name
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry_name": entry_name,
            "content": content
        })


# Displays a random page
def random(request):

    # Get a random entry and then convert it's content from markdown to HTML
    entries_name = util.list_entries()
    entry_name = entries_name[randrange(0, len(entries_name))]
    entry = util.get_entry(entry_name)
    content = markdown2.markdown(entry)

    return render(request, "encyclopedia/random.html", {
        "entry_name": entry_name,
        "content": content
    })


# Attempt to create a new page, otherwise display the create new page form 
def new_page(request):

    # User attempt to create a new page
    if request.method == "POST":
        title = request.POST["title"].capitalize()

        # Make sure the file is a ".md" file before saving it
        if not title.endswith(".md"):
            title = title + ".md"

        # The user attempts to create a new with a name that alredy exists
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

        # The user's page satisfies all the requirements
        else:

            # Get the content of the submitted form and then save it to the filename the user entered
            content_path = path.join("entries", title)
            output_file = open(content_path, "w")
            content = request.POST["content"]
            output_file.write(content)
            output_file.close()

            return HttpResponseRedirect(reverse("index"))

    # User attempts to get the create new page form
    return render(request, "encyclopedia/new-page.html")


# Displays the results of a search
def search(request):

    # Get the content of the search and then list the file(s) that match the search
    entry_name = request.POST["q"]
    entries = util.list_entries()
    contents = list()

    # Return the file if the search matches a file exactly(case-insensitive)
    if entry_name.casefold() in (entry.casefold() for entry in entries):
        content = util.get_entry(entry_name)
        
        return HttpResponseRedirect(reverse("entry", kwargs={"entry_name": entry_name.capitalize()}))

    # Get the files that contain a substring of the search(case-insensitve)
    for string in entries:
        if re.search(entry_name, string, re.IGNORECASE):
            contents.append(string)

    return render(request, "encyclopedia/search.html", {
        "contents": contents
    })


# Allows the user to edit an entry
def edit_page(request, filename):

    # User attempts to submit an edited entry
    if request.method == "POST":

        # Get the content of the edited entry and then overwrite whatever was already there
        content = request.POST["content"]
        file_path = path.join("entries", filename + ".md")
        fileptr = open(file_path, "w")
        fileptr.write(content)
        fileptr.close()

        return HttpResponseRedirect(reverse("entry", kwargs={"entry_name": filename}))

    # User attempt to display the "edit page" page
    else:

        # Identify the filename and then read it's content
        file_path = path.join("entries", filename + ".md")
        fileptr = open(file_path, "r")
        content = fileptr.read()
        fileptr.close()

        return render(request, "encyclopedia/edit-page.html", {
            "filename": filename,
            "content": content
        })
