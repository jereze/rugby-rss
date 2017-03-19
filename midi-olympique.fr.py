#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from lxml import etree
import feedgenerator
import requests
import os
import urlparse
import re

# fetching the html page
url = 'http://www.midi-olympique.fr'
response = requests.get(url)
doc = response.text

# getting the items 
tree = etree.HTML(doc)
items = tree.xpath("//main//article//div[contains(@class, 'text')]/a")

print items

# creating a feed
feed = feedgenerator.Rss201rev2Feed(title="Midi-Olympique",
      link=url,
      description="Derniers articles",
      language="fr")

# for each line in the table
for i in items:
    # getting the title
    titles = i.xpath("*[@class='title']/text()")
    title = '(Missing title)' if len(titles) == 0 else titles[0]
    print title

    # getting the link
    links = i.xpath("@href")
    link = '' if len(links) == 0 else urlparse.urljoin(url, links[0])
    print link

    # getting the description
    descriptions = i.xpath("*[@class='content']/p/text()")
    description = '' if len(descriptions) == 0 else descriptions[0]
    print description

    # getting the identifier
    ids = i.xpath("@id")
    id = '' if len(ids) == 0 else ids[0]
    print id

    feed.add_item(
            title=title,
            link=link,
            description=description,
            unique_id=id
        )

# print ""
# print feed.writeString('utf-8')

with open('midi-olympique.fr.rss', 'w') as fp:
    feed.write(fp, 'utf-8')
