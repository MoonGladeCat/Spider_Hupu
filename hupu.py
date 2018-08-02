from requests_html import HTMLSession
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import csv
import time

def getObj(url):
    headers = {'user-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    session = HTMLSession()
    r = session.get(url, headers=headers)
    r.html.render()
    bsobj = BeautifulSoup(r.html.html, "html.parser")
    return bsobj

def getNextPageUrl(startPage, bsObj):
    domain = urlparse(startPage).scheme+"://"+urlparse(startPage).netloc
    nextButton = bsObj.find('a', {'class':'nextPage'})
    if nextButton is not None:
        nextPage = domain + '/' + nextButton.attrs['href']
    else:
        nextPage = None
        print(bsObj.prettify())
    return nextPage


def getTitle(pageUrl, titleList):
    domain = urlparse(pageUrl).scheme+"://"+urlparse(pageUrl).netloc
    bsObj = getObj(pageUrl)
    tilteBox = bsObj.find_all('div', {'class':'titlelink box'})
    for box in tilteBox:
        truetit      = box.find('a', {'class':'truetit'})
        truetitName  = truetit.string
        ansour       = box.find_next_sibling('span', {'class':'ansour box'}).string    
        listItem = {'title':truetitName, 'ansour':ansour}
        if listItem not in titleList:
            titleList.append(listItem)
    
    nextPageUrl = getNextPageUrl(pageUrl, bsObj)
    
    return nextPageUrl
    
if __name__ == '__main__':
    titleList = []
    pageUrl = 'https://bbs.hupu.com/bxj'
    csvfile = open('hupuTitle.csv', 'w')
    fieldnames = ['title', 'ansour']
    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    csvwriter.writeheader()
    while pageUrl is not None:
        print('now is analysis :' + pageUrl)
        pageUrl = getTitle(pageUrl, titleList)
        time.sleep(5)

    
    for title in titleList:
        csvwriter.writerow(title)

    csvfile.close() 
	
