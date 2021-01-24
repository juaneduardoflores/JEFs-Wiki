# A script that I execute if I ever want to create a new blog entry.
# Steps:
#   1.) Asks me for the title of entry:
#       - creates new directory and directory.md file with template.
#   2.) Adds the html code for this new entry.

import os
import re
import json
import sys
import random
from datetime import date

today = date.today()
blogEntryTitle = "temp"
blogEntryDescription = "temp description"
blogEntryTags = ""
last_modified = str(today)
tags = []
inputTitle = ""


def main():
    global blogEntryTitle, blogEntryDescription, blogEntryTags, last_modified, tags, inputTitle

    # If an argument was passed, we are updating, else we are creating
    if (len(sys.argv) > 1):
        inputTitle = str(sys.argv[1])
        updateEntry()
        sys.exit(0)

    else:
        blogEntryTitle = input("Enter new blog entry title: ")
        blogEntryDescription = input(
            "Enter a short description for {}: ".format(blogEntryTitle))
        blogEntryTags = input("Enter any tags followed by comma: ")
        tags = blogEntryTags.split(",")
        print("tags: " + str(tags))
        os.mkdir(blogEntryTitle)
        os.mkdir(blogEntryTitle + "/cover_img")
        print("created directory called " + blogEntryTitle)
        f = open("{}/{}.md".format(blogEntryTitle, blogEntryTitle), "w+")

        addEntrytoHTML()

        # with open('entries.json', 'r') as json_file:
        #     data = json_file.read()

        # objs = json.loads(data)
        # obj_keys = objs.keys()
        # for key in objs:
        #     print("key: " + key + " " + str(objs[key]))


def updateEntry():
    global blogEntryTitle, blogEntryDescription, blogEntryTags, last_modified, tags

    htmlFile = open("../blog.html", "r").read()
    entries_raw = re.findall(
        '<!-- BLOG ENTRIES -->(.*?)<!-- BLOG ENTRIES END -->', htmlFile, re.DOTALL)
    lineiterator = iter(entries_raw[0].splitlines())
    entries = []
    cur_entry = ""
    found_entry = False
    modifying_date = False
    for l in lineiterator:
        if (found_entry):

            if (modifying_date):
                if (re.match('.*\d{4}-\d{2}-\d{2}.*', l)):
                    print("CHANGING ENTRY MODIFIED DATE")
                    today = date.today()
                    l = re.sub("\d{4}-\d{2}-\d{2}", str(today), l)

            if (re.match('\w*', l)):
                print("appending!")
                print(l)
                cur_entry += str(l)

            if (l == ""):
                print("ADDING TO LIST..")
                cur_entry += "\n"
                entries.append(cur_entry)
                cur_entry = ""
                found_entry = False
                modifying_date = False

        if (re.search('<!--', l)):
            print("LOOK AT ME: " + l)
            if (re.match('.*<!-- {} -->'.format(inputTitle), l)):
                modifying_date = True
            cur_entry += str(l)
            found_entry = True

        # if (re.search('.*</p>', l)):
        #     print("FOUND PARAGRAPH")
        #     if (len(tags) > 0):
        #         tagHTML = ""
        #         for tag in tags:
        #             newtag = "<span class='uk-label' style='background-color: {}'>{}</span>\n".format("green",
        #                                                                                               tag)
        #             tagHTML += newtag
        #         cur_entry += tagHTML

    sep = '<!-- BLOG ENTRIES -->'
    stripped = htmlFile.split(sep, 1)[
        0] + sep + "<div class='uk-container uk-margin-remove uk-padding-remove'>"

    for entry in entries:
        print(entry)
        stripped += entry + "\n"

    stripped += "\n\n<!-- BLOG ENTRIES END -->"

    print(stripped)
    f = open("../blog.html", "w")
    f.write(stripped)
    f.close()

    # run prettier on file.
    os.system("npx prettier --write ../blog.html")


def addEntrytoHTML():
    global blogEntryTitle, blogEntryDescription, blogEntryTags, last_modified, tags

    htmlFile = open("../blog.html", "r").read()
    entries_raw = re.findall(
        '<!-- BLOG ENTRIES -->(.*?)<!-- BLOG ENTRIES END -->', htmlFile, re.DOTALL)
    lineiterator = iter(entries_raw[0].splitlines())
    entries = []
    cur_entry = ""
    found_entry = False
    for l in lineiterator:
        if (found_entry):
            if (re.match('\w*', l)):
                print("appending!")
                print(l)
                cur_entry += str(l)

            if (l == ""):
                print("ADDING TO LIST..")
                cur_entry += "\n"
                entries.append(cur_entry)
                cur_entry = ""
                found_entry = False

        if (re.search('<!--', l)):
            print(l)
            cur_entry += str(l)
            found_entry = True

    template = "\n\n<!-- {} -->\n".format(blogEntryTitle)
    if (len(entries) % 2 == 0):
        template += "<a href='./Blog/{}/{}.html'>\n".format(
            blogEntryTitle, blogEntryTitle)
        template += "<div class='uk-card uk-card-default uk-grid-collapse uk-child-width-1-2@s uk-margin' uk-grid >"
        template += "<div class='uk-card-media-left uk-cover-container'>"
        template += "<img src='./Blog/{}/cover/cover.png' alt='' uk-cover />".format(
            blogEntryTitle)
        template += "<canvas width='600' height='400'></canvas>"
        template += "</div>"
        template += "<div> <div class='uk-card-body'> <h3 class='uk-card-title'> {} <span class='uk-text-warning'>(WIP)</span> </h3> <span>last modified: {} </span> <p> {} </p> ".format(
            blogEntryTitle, last_modified, blogEntryDescription)

        # add tags
        template = addTags(template)

        template += "</div> </div>"
        template += "</div> </a>\n\n"
        template += "<!-- BLOG ENTRIES END -->"
        template += "</div></div></body></html>"

    else:
        template += "<a href='./Blog/{}/{}.html'>\n".format(
            blogEntryTitle, blogEntryTitle)
        template += "<div class='uk-card uk-card-default uk-grid-collapse uk-child-width-1-2@s uk-margin' uk-grid >"
        template += "<div> <div class='uk-card-body'> <h3 class='uk-card-title'> {} <span class='uk-text-warning'>(WIP)</span> </h3> <span>last modified: {} </span> <p> {} </p>".format(
            blogEntryTitle, last_modified, blogEntryDescription)

        # add tags
        template = addTags(template)

        template += "</div> </div>"
        template += "<div class='uk-card-media-left uk-cover-container'>"
        template += "<img src='./Blog/{}/cover/cover.png' alt='' uk-cover />".format(
            blogEntryTitle)
        template += "<canvas width='600' height='400'></canvas>"
        template += "</div>"
        template += "</div> </a>\n\n"
        template += "<!-- BLOG ENTRIES END -->"
        template += "</div></div></body></html>"

    entries.append(template)

    sep = '<!-- BLOG ENTRIES -->'
    stripped = htmlFile.split(sep, 1)[
        0] + sep + "<div class='uk-container uk-margin-remove uk-padding-remove'>"

    for entry in entries:
        print(entry)
        stripped += entry + "\n"

    print(stripped)
    f = open("../blog.html", "w")
    f.write(stripped)
    f.close()

    # run prettier on file.
    os.system("npx prettier --write ../blog.html")
    os.system("npx prettier --write ./tags.json")


def addTags(template):
    if (len(tags) > 0):
        for tag in tags:
            tag = tag.strip()

            tag_color = "#FFFFFF"
            with open('tags.json', 'r+') as json_file:
                data = json_file.read()

                objs = json.loads(data)
                keyfound = False
                for key in objs:
                    print("key: " + key + " value: " + str(objs[key]))
                    print("keyUpper: " + key.upper())
                    print("tagUpper: " + tag.upper())
                    if (key.upper() == tag.upper()):
                        keyfound = True
                        tag_color = objs[key]
                        newtag = "<span class='uk-label' style='background-color: {}'>{}</span>\n".format(
                            tag_color, tag)

                if (not keyfound):
                    # random hex color
                    random_number = random.randint(0, 16777215)
                    hex_number = format(random_number, 'x')
                    hex_number = '#'+hex_number

                    objs[tag] = hex_number
                    tag_color = objs[tag]
                    print(objs)
                    json_file.seek(False)
                    json_obj = json.dumps(objs, indent=2)
                    json_file.write(str(json_obj))
                    newtag = "<span class='uk-label' style='background-color: {}'>{}</span>\n".format(
                        tag_color, tag)

            template += newtag

    return template


main()