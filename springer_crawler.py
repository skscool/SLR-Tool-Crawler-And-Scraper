from bs4 import BeautifulSoup as soup
import requests
import json

NA = "Not Available"
http = 'https://www.springer.com'

#---------------------------------------get the number of pages in the search result to loop over----------------------------------------------------
stringToSearch = "Sulphur"
html = requests.get('https://www.springer.com/in/search?dnc=true&facet-type=type__book&query=' + stringToSearch + '&submit=Submit').text
page_soup = soup(html,'html.parser')
noOfSearchPages = page_soup.find('span', {'class': 'number-of-pages'}).string.strip()
noOfSearchPages = int(noOfSearchPages)+1

#list of Parsed BibTex dictionary, each item can become vaule part of JSON object
bibs = []

#--------------------------------------for each page and then for each result in the page do bibTex processing----------------------------------------
for page in range (1, noOfSearchPages):
  html = requests.get('https://www.springer.com/in/search?dnc=true&facet-type=type__book&page=' + str(page) + '&query=' + stringToSearch +'&submit=Submit').text
  page_soup = soup(html,'html.parser')

  result = page_soup.findAll('div', {'class': 'result-item'})   #html-container of items in search-result
  #------------------------------------------------for each search-result item------------------------------------------------------
  for item in result:
    link = http + item.find('h4').find('a')['href']   #link to the book's landing page
    bookLandingPage = requests.get(link).text
    bookSoup = soup(bookLandingPage, "html.parser")   #get book landing page HTML
    bibliographySection = bookSoup.find('div', {'class':'product-bibliographic'})   #this section has DOI
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
#print(bibs)

#-----------------------------------------------------file writing stuff----------------------------------------------------------------
output_json = {}                    #json equivalent of the list of bibtex
for bib in range(0, len(bibs)):
  output_json[bib] = bibs[bib]

filename = "output.json"            #write to json file
with open(filename, 'w') as outfile:
    json.dump(output_json, outfile)
