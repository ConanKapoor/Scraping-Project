# Author - Shivam Kapoor

# Importing libraries
from bs4 import BeautifulSoup
import urllib.request
import os,tldextract

# Creating Output folder
if (os.path.exists("Output")):
    delete = str('rm -r Output')
    os.system(delete)
    os.makedirs("Output")
else:
    os.makedirs("Output")

#################### Scraping Logic Below ###########################

# Collecting html content.
url = "https://gallery.123telugu.com/content/reviews/main/more_reviews_Telugu.html"
request = urllib.request.Request(url)
response = urllib.request.urlopen(request)

# Using BeautifulSoup to parse html object response.
page = BeautifulSoup(response.read(),'html.parser')
soup = page.encode('utf-8')

# Finding Specific "a" tag data
links = []
aTag = soup.find_all("a", {"class": "NormalText"})

# Collecting all the links from given webpage
for tag in aTag:
    links.append(tag.get('href'))

# Saving links in a file
linkfile = open('links.txt', 'w')
for link in links:
    linkfile.write("%s\n" %link)

#################### Now links list contains all the links to scrape ###########################

for link in links:
    # Opening and scraping the data from every page.
    request = urllib.request.Request(link)
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response.read(),'html.parser')

    # Deciding File Name
    parts = link.split("/")
    name = parts[len(parts)-1].split(".")
    regex = name[0]
    filename = str(os.path.abspath("") + '/Output/Scraped-'+ regex)

    # Finding Specific DIV tag data
    divTag = soup.find("div", {"class": "post-content"})
    divTag.find(text="")
