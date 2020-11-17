from bs4 import BeautifulSoup as sp
import requests
import json
from math import ceil

def getSearchString(searchInput):
	print("from get search string", searchInput)
	searchString = ""
	date = ""
	if 'date' in searchInput.keys():
		date = searchInput['date']
		searchInput.pop('date')
	ind = 0
	for key, val in searchInput.items():
		ind += 1
		print(key, val)
		# &field1=ContribAuthor&text1=markus"
		searchString += '&field' + str(ind) + '=' + key + '&text' + str(ind) + '=' + val 
	if date != "":
		searchString += '&'+ date
	searchString = searchString.replace(' ', '%20')
	return searchString

def getDOI(citation):
	try:
		title = citation.find("span", {"class":"hlFld-Title"})
		for a in title.findAll("a", href=True):
			dois = a['href']
		dois = dois[5:]
		if dois[0] not in {'0','1','2','3','4','5','6','7','8','9'}:
			dois = dois[12:]
	except:
		dois = "Error Finding DOI"
	return dois

def parsed_bibTex(dois):
	# try:
	url = "https://dl.acm.org/action/exportCiteProcCitation"
	data = {'dois':dois,'targetFile':'custom-bibtex','format':'bibTex'}
	try:
		response = requests.post(url,data = data).json()
		bib = {}
		try:
			#	CHAPTER -> inbook
			#	PAPER-CONFERENCE ==> inproceedings
			#	ARTICLE ==> article
			#	REPORT ==> techreport
			typee = response['items'][0][dois]['type']
			if typee == "CHAPTER":
				bib['type'] = "inbook"
			elif typee == "REPORT":
				bib['type'] = "techreport"
			elif typee == "ARTICLE":
				bib['type'] = "article"
			else:
				bib['type'] = "inproceedings"
		except:
			pass
		bib['author'] = ""
		i = False
		imp_response = response['items'][0][dois]
		# print(response['items'][0][dois])
		try:
			for athr in response['items'][0][dois]['author']:
				# print(athr['family'])
				# print(i)
				if(i):
					bib['author'] += " and "
				i = True
				bib['author'] += athr['family']+", "+athr['given']

		except:
			pass
		try:
			bib['title'] = response['items'][0][dois]['title']
		except:
			pass
		try:
			bib['year'] = imp_response['issued']['date-parts'][0][0]
		except:
			pass
		try:
			bib['isbn'] = imp_response['ISBN']
		except:
			pass
		try:
			bib['publisher'] = imp_response['publisher']
		except:
			pass
		try:
			bib['address'] = imp_response['publisher-place']
		except:
			pass
		try:
			bib['url'] = imp_response['URL']
		except:
			pass
		try:
			bib['doi'] = dois
		except:
			pass
		try:
			bib['abstract'] = imp_response['abstract']
		except:
			pass
		try:
			bib['booktitle'] = imp_response['container-title']
		except:
			pass
		try:
			bib['pages'] = imp_response['page'].replace("–","-")
		except:
			pass
		try:
			bib['numpages'] = imp_response['number-of-pages']
		except:
			pass
		try:
			bib['keywords'] = imp_response['keyword']
		except:
			pass
		try:
			bib['location'] = imp_response['event-place']
		except:
			pass
		try:
			bib['series'] = imp_response['collection-title']
		except:
			pass
	except:
		# pass
		bib = "Error Fetching BibTex for doi = "+dois
	return bib


def scrape(parsed_html):
	contents = parsed_html.findAll("div",{"class":"issue-item issue-item--search clearfix"})
	print("no. of contents = ",len(contents))
	bibTex = []
	for citation in contents:
		dois = getDOI(citation)
		print("dois = ",dois)
		bibTex.append(parsed_bibTex(dois))
		# count += 1
		# print("bib = ",json.dumps(bibTex,indent=2))
	return bibTex

def getACMRecords(searchInput, bibs):
	searchString = getSearchString(searchInput)
	print("from get acm records", searchString)
	url = "https://dl.acm.org/action/doSearch?fillQuickSearch=false&expand=dl" + searchString + '&pageSize=50'
	print(url)

	x = requests.get(url)
	parsed_html = sp(x.text,"html.parser")

	totalNumber = int(parsed_html.find("span",{"class":"hitsLength"}).string.strip().replace(',',''))
	totalPages = ceil(totalNumber/50)
	print("Total Results: ",totalNumber)
	print("Total Pages: ",totalPages)

	# Extract first page
	bibs += scrape(parsed_html)
	# return
	for i in range(1,totalPages):
		print("Page ",i)
		next_page = url + "&pageSize=50&startPage="+str(i)
		print(next_page)
		x = requests.get(next_page)
		parsed_html = sp(x.text,"html.parser")
		bibs += scrape(parsed_html)
	print("total bibs from acm", len(bibs))
	return bibs

