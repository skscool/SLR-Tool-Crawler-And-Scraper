from bs4 import BeautifulSoup as soup
import requests
import json
import math


def getSearchString(searchInput):
  # ranges = '"1872_2021_Year"'
  print("from get search string", searchInput)
  searchString = ""
  for key, val in searchInput.items():
    if len(val) > 0:
      searchString += '&' + key + '=' + val
  searchString = searchString.replace(' ', '+')
  return searchString


def getBibTex(stringToSearch):
	# list of Parsed BibTex dictionary, each item can become vaule part of JSON object
	bibs = []
	# prefix link for search
	springerLink = 'https://www.springer.com/generic/search/results?SGWID=5-40109-24-653415-0&media=book&sortOrder=relevance&searchType=ADVANCED_CDA&searchScope=editions'
	searchLink = springerLink + stringToSearch
	print(searchLink)
	try:
		html = requests.get(searchLink).text
		page_soup = soup(html, 'html.parser')
		# get the number of pages in the search result to loop over
		noOfItemsInResults = int(page_soup.find(
				'span', {'class': 'resultInfo'}).text.split(' ')[2].replace(',', ''))
		print('no of items in search result :', noOfItemsInResults)
		noOfPages = math.ceil(noOfItemsInResults/10)
		print('no of pages in search result :', noOfPages)
	except Exception as e:
		print("No results found")
		return bibs
	# this is id number of the first item in any page.. this would decided which page number to fetch.
	# there are 10 results per pages so this offset is incremented by 10 on each page
	# Example : if pageOffset = 1 then pageNo = 1, if pageOffset = 11 then pageNo = 2.. and so on
	pageOffset = 1

	# for each page and then for each result in the page do bibTex processing
	for page in range(1, noOfPages+1):
		try:
			html = requests.get(
					searchLink + '&resultStart=' + str(pageOffset)).text
			pageOffset += 10
			page_soup = soup(html, 'html.parser')

			# html-container of items in search-result
			result = page_soup.findAll('li', {'class': 'listItemBooks'})
		except Exception as e:
			print("Unable to access this page")
			continue
		# ------------------------------------------------for each search-result item------------------------------------------------------
		for item in result:
			try:
				# link to the item's landing page
				link = item.find('a')['href']
				itemLandingPage = requests.get(link).text
				# get item landing page HTML
				itemSoup = soup(itemLandingPage, "html.parser")
				bibliographySection = itemSoup.find(
						'div', {'class': 'product-bibliographic'})  # this section has DOI
				divDOI = bibliographySection.findAll('dl')[2]
				DOI = divDOI.findAll('dd')[1].string.strip()  # get DOI

				target = 'https://citation-needed.springer.com/v2/references/' + \
						DOI + '_1?format=bibtex&flavour=citation'  # link for BibTex
				bibTex = requests.get(target)  # get BibTex

				# --------------------------------------if request is successful then parse the bibtex to a dictionary----------------------------
				if(bibTex.status_code == 200):
					bibtex = bibTex.text.replace(
							"}", "").strip("\t \n ") + '\n'
					ind = bibtex.index("{")
					# dictionry equivalent of current BibTex object. has fields(type, id, other_attributes...)
					bib_dict = {}
					bib_dict["type"] = bibtex[:ind]  # type, key value
					bibtex = bibtex[ind+1:]
					ind = bibtex.index("\n")
					bib_dict["id"] = bibtex[:ind-1]  # id, key value
					bibtex = bibtex[ind+1:]

					# -------------------get all other attributes, key value from bibtex (text form)---------------------
					while(bibtex != "" and bibtex != "\n"):
						ind = bibtex.index("=")
						key = bibtex[:ind].strip()  # key
						bibtex = bibtex[ind+2:]
						ind = bibtex.index("\"")
						value = bibtex[:ind].replace(
								'\n', '').strip()  # value
						bib_dict[key] = value
						bibtex = bibtex[ind+2:]
					# add current bibtex dictionary to global list
					bibs.append(bib_dict)
					# print(bib_dict)
			except Exception as e:
				print("Unable to get bibTex")
	return bibs


def getSpringerRecords(searchInput, bibTex):
	searchString = getSearchString(searchInput)
	print(searchString)
	bibTex += getBibTex(searchString)
	print("total bibs from springer", len(bibTex))
	return bibTex
