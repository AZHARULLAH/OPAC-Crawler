import requests
from bs4 import BeautifulSoup
import json

uptoCGIBin = 'http://192.168.240.18'
baseURL = 'http://192.168.240.18/cgi-bin/koha/opac-search.pl?q='
searchPhrase = 'ross'
completeURL = baseURL + searchPhrase

r = requests.get(completeURL)
data = r.text
soup = BeautifulSoup(data, 'html.parser')
eachBookDiv = soup.find_all("td", class_="bibliocol")

booksResult = list()

for bookDetails in eachBookDiv:
    singleBook = dict()
    bookTitleRaw = bookDetails.select('a.title')[0]
    bookTitleRaw.span.unwrap()
    singleBook['bookTitle'] = bookTitleRaw.text.replace(" /", "").replace(";",",")
    singleBook['bookLink'] = uptoCGIBin + bookTitleRaw.get("href")
    bookAvailabilityRaw = bookDetails.select('span.availability')[0]
    # print bookAvailabilityRaw.select('span.available')
    if(bookAvailabilityRaw.select('span.available')):
        singleBook['bookAvailabilityStatus'] = bookAvailabilityRaw.select('span.available b')[0].text.replace(":", "").replace("Items","Book")
        bookRackRaw = bookDetails.select('span.location')[0].select('span.available')[0]
        bookRackRaw.b.unwrap()
        bookRackRaw = bookRackRaw.text.split(" ")[1]
        singleBook['bookRack'] = str(bookRackRaw)
    elif(bookAvailabilityRaw.select('span.unavailable')):
        singleBook['bookAvailabilityStatus'] = "Book not available"
        singleBook['bookRack'] = "NA"
        
    # bookAvailabilityRaw = bookAvailabilityRaw.select('span.available')
    # print singleBook['bookTitle']
    # print singleBook['bookLink']
    # print singleBook['bookAvailabilityStatus']
    # print singleBook['bookRack']
    # print "\n"

    booksResult.append(singleBook.copy())

json.dumps(booksResult)
# print booksResult
print json.dumps(booksResult, indent=4, sort_keys=False)