# Author - Shivam Kapoor

# Importing libraries
from bs4 import BeautifulSoup
import urllib.request
import os,tldextract
import sys

# Creating Output folder
if (os.path.exists("OutputEng")):
    delete1 = str('rm -r OutputEng')
    delete2 = str('rm logsEng.txt')
    os.system(delete1)
    os.system(delete2)
    os.makedirs("OutputEng")
    os.makedirs("OutputEng/Positive")
    os.makedirs("OutputEng/Negative")
else:
    os.makedirs("OutputEng")
    os.makedirs("OutputEng/Positive")
    os.makedirs("OutputEng/Negative")

# Making a log file
logsEng = open('logsEng.txt','w')
logsEng.write("Following links threw errors. Have to do manually -->\n\n")

#################### Scraping Logic Below ###########################

# Collecting html content.
url = "http://www.123telugu.com/reviews/main/more_reviews.html"
request = urllib.request.Request(url)
response = urllib.request.urlopen(request)

# Using BeautifulSoup to parse html object response.
soup = BeautifulSoup(response.read(),"html5lib")

# Finding Specific "a" tag data
links = []
Tablearea = soup.find("table", {"class": "generalSpace"})
aTag = Tablearea.find_all("a", {"class": "NormalText"})

# Collecting all the links from given webpage
for tag in aTag:
    href = str(tag.get('href'))
    if "../" in href:
        temp = "http://www.123telugu.com/reviews" + href[2:len(href)]
        links.append(temp)
    else:
        links.append(tag.get('href'))

# Saving links in a file
linkfile = open('linksEng.txt', 'w')
for link in links:
    linkfile.write("%s\n" %link)

print ("\t\t>>>>>> Links Scraping Finished <<<<<<")
print ("\t\t>>>>>>>>> No of links - %s <<<<<<<<<" %(len(links)))
print ("\t\t>>>>>Links stored at linksEng.txt<<<<")

#################### Now links list contains all the links to scrape ###########################


count = 1
for link in links:
    try:
        # Just for printing purposes
        print("\n>>> %s. Scraping data from %s" %(count,link))

        # Opening and scraping the data from every page.
        request = urllib.request.Request(link)
        try:
            urllib.request.urlopen(request)
        except urllib.error.URLError as e:
            print("\t>!>!> caught a 404 error - skipping to next link.(Check logsEng.txt)\n")
            logsEng.write("404 Error : %s \n\n" %(link))
            count = count+1
            continue

        response = urllib.request.urlopen(request)
        soup = BeautifulSoup(response.read(),"html5lib")

        # Deciding File Name
        parts = link.split("/")
        name = parts[len(parts)-1].split(".")
        filename1 = str(os.path.abspath("") + '/OutputEng/Positive/Positive-'+ name[0] + ".txt")
        filename2 = str(os.path.abspath("") + '/OutputEng/Negative/Negative-'+ name[0] + ".txt")

        # Opening Files
        positivefile = open(filename1,'a')
        negativefile = open(filename2,'a')

        # Finding Specific tag data
        if soup.find("table", {"class": "generalSpace"}) is not None:
            tableTag = soup.find("table", {"class": "generalSpace"})
            data = tableTag.find_all("p")

            # Main logic
            for i in range(0,len(data)):
                if "What is Good" in str(data[i]) or "Plus Points" in str(data[i]) or "Positive Points" in str(data[i]):
                    savepoint1 = i

                if "What is bad" in str(data[i]) or "Minus Points" in str(data[i]) or "Negative Points" in str(data[i]):
                    savepoint2 = i

                if "Technical Aspects" in str(data[i]) or "Technical Departments" in str(data[i]):
                    savepoint3 = i
                    break

            # Saving positive points in respective file
            for i in range(savepoint1,savepoint2):
                temp = str(data[i]).replace('<p>','').replace('</p>','').replace('<strong>','').replace('</strong>','').replace('What is Good:','').replace('What is Good :','').replace('<i>','').replace('</i>','').replace('\n','')
                positivefile.write(temp)
                positivefile.write("\n\n")

            # Saving negative points in respective file
            for i in range(savepoint2,savepoint3):
                temp = str(data[i]).replace('<p>','').replace('</p>','').replace('<strong>','').replace('</strong>','').replace('What is bad:','').replace('What is bad :','').replace('<i>','').replace('</i>','').replace('\n','')
                negativefile.write(temp)
                negativefile.write("\n\n")

        elif soup.find("div", {"class": "post-content"}) is not None:
            tableTag = soup.find("div", {"class": "post-content"})
            data = tableTag.find_all("p")

            for i in range(0,len(data)):
                if "Plus Points" in str(data[i]) or "Positive Points" in str(data[i]):
                    savepoint1 = i

                if "Minus Points" in str(data[i]) or "Negative Points" in str(data[i]):
                    savepoint2 = i

                if "Technical Aspects" in str(data[i]) or "Technical Departments" in str(data[i]):
                    savepoint3 = i
                    break

            # Saving positive points in respective file
            for i in range(savepoint1+1,savepoint2):
                temp = str(data[i]).replace('<p>','').replace('</p>','').replace('Plus Points:-','').replace('Minus Points:-','').replace('<i>','').replace('</i>','').replace('\n','').replace('<strong>','').replace('</strong>','')
                positivefile.write(temp)
                positivefile.write("\n\n")

            # Saving negative points in respective file
            for i in range(savepoint2+1,savepoint3):
                temp = str(data[i]).replace('<p>','').replace('</p>','').replace('Minus Points:-','').replace('Plus Points:-','').replace('<i>','').replace('</i>','').replace('\n','').replace('<strong>','').replace('</strong>','')
                negativefile.write(temp)
                negativefile.write("\n\n")

        else:
            print("\t>!>!> Choice exception caught - skipping to next link.(Check logsEng.txt)\n")
            logsEng.write("Choice error - %s \n\n" %(link))

        # Closing Files
        positivefile.close()
        negativefile.close()

        print("\t>>> DONE : Scraped %s \n" %(count))
        count = count+1

    except Exception:
        print("\t>!>!> Exceptioncaught - skipping to next link.(Check logsEng.txt)\n")
        logsEng.write("Exception error - %s \n\n" %(link))
        count = count+1
        pass

logsEng.close()
