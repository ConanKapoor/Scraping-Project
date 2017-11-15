# Author - Shivam Kapoor

# Importing libraries
from bs4 import BeautifulSoup
import urllib.request
import re

#Collecting html content.
url = "https://gallery.123telugu.com/content/reviews/main/more_reviews_Telugu.html"
request = urllib.request.Request(url)
response = urllib.request.urlopen(request)

#Using BeautifulSoup to parse html object response.
page = BeautifulSoup(response.read(),'html.parser')
