from bs4 import BeautifulSoup as soup
import requests
import json

NA = "Not Available"
http = 'https://www.springer.com'

#---------------------------------------get the number of pages in the search result to loop over----------------------------------------------------
def getSearchString(searchInput):
  searchString = ""
  return searchString
  stringToSearch = "Sulphur"

def noOfPages(stringToSearch):
  html = requests.get('https://www.springer.com/in/search?dnc=true&facet-type=type__book&query=' + stringToSearch + '&submit=Submit').text
  page_soup = soup(html,'html.parser')
  noOfSearchPages = page_soup.find('span', {'class': 'number-of-pages'}).string.strip()
  return int(noOfSearchPages)+1

#--------------------------------------for each page and then for each result in the page do bibTex processing----------------------------------------

def getBibTex(stringToSearch, noOfSearchPages):
  #list of Parsed BibTex dictionary, each item can become vaule part of JSON object
  bibs = []
  for page in range (1, noOfSearchPages):
    html = requests.get('https://www.springer.com/in/search?dnc=true&facet-type=type__book&page=' + str(page) + '&query=' + stringToSearch +'&submit=Submit').text
    page_soup = soup(html,'html.parser')

    result = page_soup.findAll('div', {'class': 'result-item'})   #html-container of items in search-result
    #------------------------------------------------for each search-result item------------------------------------------------------
    for item in result:
      link = http + item.find('h4').find('a')['href']   #link to the item's landing page
      itemLandingPage = requests.get(link).text
      itemSoup = soup(itemLandingPage, "html.parser")   #get item landing page HTML
      bibliographySection = itemSoup.find('div', {'class':'product-bibliographic'})   #this section has DOI
      divDOI = bibliographySection.findAll('dl')[2]
      DOI = divDOI.findAll('dd')[1].string.strip()      #get DOI

      target = 'https://citation-needed.springer.com/v2/references/' + DOI + '_1?format=bibtex&flavour=citation'  #link for BibTex
      bibTex = requests.get(target)   #get BibTex

      #--------------------------------------if request is successful then parse the bibtex to a dictionary----------------------------
      if(bibTex.status_code == 200):  
        bibtex = bibTex.text.replace("}","").strip("\t \n ") + '\n'
        ind = bibtex.index("{")
        bib_dict = {}                           #dictionry equivalent of current BibTex object. has fields(type, id, other_attributes...)
        bib_dict["type"] = bibtex[:ind]         #type, key value
        bibtex = bibtex[ind+1:]
        ind = bibtex.index("\n")
        bib_dict["id"] = bibtex[:ind-1]         #id, key value
        bibtex = bibtex[ind+1:]

        #-------------------get all other attributes, key value from bibtex (text form)---------------------
        while(bibtex != "" and bibtex != "\n"):
          ind = bibtex.index("=")
          key = bibtex[:ind].strip() #key
          bibtex = bibtex[ind+2:]
          ind = bibtex.index("\"")
          value = bibtex[:ind].replace('\n','').strip() #value
          bib_dict[key] = value
          bibtex = bibtex[ind+2:]
        bibs.append(bib_dict)         #add current bibtex dictionary to global list
  return bibs

def getSpringerRecords(searchInput):
  searchString = getSearchString(searchInput)
  print(searchString)
  noOfSearchPages = getNoOfPages(searchString)
  print(noOfSearchPages)
  bibTex = getBibTex(searchString, noOfSearchPages)
  print(len(bibTex))
  return bibTex

