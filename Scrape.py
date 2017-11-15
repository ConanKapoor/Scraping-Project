# Author - Shivam Kapoor

# Importing libraries
from bs4 import BeautifulSoup
import urllib.request
import re

# Collecting html content.
url = "https://gallery.123telugu.com/content/reviews/main/more_reviews_Telugu.html"
request = urllib.request.Request(url)
response = urllib.request.urlopen(request)

# Using BeautifulSoup to parse html object response.
soup = BeautifulSoup(response.read(),'html.parser')

# Finding Specific DIV tag data
links = []
divTag = soup.find_all("a", {"class": "NormalText"})

# Collecting all the links from given webpage
for tag in divTag:
    links.append(tag.get('href'))

#################### Now links list contains all the links to scrape###########################
