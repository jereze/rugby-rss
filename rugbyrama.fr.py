#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from lxml import etree
import feedgenerator
import requests
import os
import urlparse
import re

# fetching the html page
url = 'http://www.rugbyrama.fr/'
response = requests.get(url)
doc = response.text

# getting the items 
tree = etree.HTML(doc)
items = tree.xpath("//div[contains(@class, 'storylist-latest__main-title')]")

print items

# creating a feed
feed = feedgenerator.Rss201rev2Feed(title="Rugbyrama",
      link=url,
      description="Derniers articles",
      language="fr")

# for each line in the table
for i in items:
    # getting the title
    titles = i.xpath('a/text()')
    title = '(Missing title)' if len(titles) == 0 else titles[0]
    print title

    # getting the link
    links = i.xpath('a/@href')
    link = '' if len(links) == 0 else urlparse.urljoin(url, links[0])
    print link

#   # getting the description
#   descriptions = i.xpath('a/text()')
#   description = '' if len(descriptions) == 0 else descriptions[0]

    # getting the identifier
    id_search = re.search('[a-z]+(\d+)/[a-z]+\.shtml', link, re.IGNORECASE)
    id = link if id_search is not None else id_search.group(1)

    feed.add_item(
            title=title,
            link=link,
            description='',
            unique_id=id
        )

# print ""
# print feed.writeString('utf-8')

with open('rugbyrama.fr.rss', 'w') as fp:
    feed.write(fp, 'utf-8')
