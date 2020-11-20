from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
import os
from main import *
from time import time

# Create your views here.
def landing(request):
	return render(request,'landing.html')
	# return HttpResponse("Hello, world. You're at the polls index.")

def acm(request):
	return render(request,'ACM.html')

def ieee(request):
	return render(request,'IEEE.html')

def sciencedirect(request):
	return render(request,'ScienceDirect.html')

def springer(request):
	return render(request,'Springer.html')

def fetchAll(request):
	fileName = 'All-' + str(time()).replace('.', '') + '.txt' 
	print("\n\nfrom fetch all", request.POST)
	getJSONAll(request.POST, fileName)
	return sendDownloadedFile(fileName)

def fetchACM(request):
	fileName = 'ACM-' + str(time()).replace('.', '') + '.txt'
	print("\n\nfrom fetch ACM", request.POST)
	getJSONACM(request.POST, fileName)
	return sendDownloadedFile(fileName)

def fetchIEEE(request):
	fileName = 'IEEE-' + str(time()).replace('.', '') + '.txt'
	print("\n\nfrom fetch IEEE", request.POST)
	getJSONIEEE(request.POST, fileName)
	return sendDownloadedFile(fileName)

def fetchScienceDirect(request):
	fileName = 'ScienceDirect-' + str(time()).replace('.', '') + '.txt'
	print("\n\nfrom fetch Science Direct", request.POST)
	getJSONScienceDirect(request.POST, fileName)
	return sendDownloadedFile(fileName)

def sendDownloadedFile(fileName):
	path = os.getcwd()+ '/' + fileName #"/output.json"
	print("Sending file...")

	response = FileResponse(open(path, 'rb'),as_attachment=True)
	return response

#----------------------------------------------Springer specific code-----------------------------------------------------------------------------

#data structure to convert the search filters to respective url
subCategoryList = list()
categoryToLinkdataDICT = {}

dateFilterList = list()
dateToLinkdataDICT = {}

languageFilterList = list()
languageToLinkdataDICT = {}

typeFilterList = list()					#--------------change 4------------------ create dict of filter values(shown in dropdown menu  
typeToLinkdataDICT = {}					#----------------------to the user)and their actual link metadata (to be able to apply filter)


#fetch the custom filters according to the search string provided
def fetchFilters(request):
	subCategoryList.clear()
	categoryToLinkdataDICT.clear()
	categoryToLinkdataDICT["---- all ----"] = "---- all ----"
	
	dateFilterList.clear()
	dateToLinkdataDICT.clear()
	dateToLinkdataDICT["---- all ----"] = "---- all ----"
	
	languageFilterList.clear()
	languageToLinkdataDICT.clear()
	languageToLinkdataDICT["---- all ----"] = "---- all ----"

	typeFilterList.clear()									#---------change 5-----clear filter value to link dict & add an entry for users 
	typeToLinkdataDICT.clear()								#----------------------who don't wan't to apply that filter
	typeToLinkdataDICT["---- all ----"] = "---- all ----"
		
	searchString = request.GET['searchString']
	print("searchString --> springer /fetchfilter :",searchString)
	from bs4 import BeautifulSoup as soup
	import requests
	import json

	http = 'https://www.springer.com'
	response = ""
	stringToSearch = searchString
	html = requests.get('https://www.springer.com/in/search?dnc=true&facet-type=type__book&query=' + stringToSearch + '&submit=Submit').text
	page_soup = soup(html,'html.parser')
	#get category filter and link for dropdown
	
	categories = page_soup.find('div', {'id': 'facet-subj'}).findAll('span', {'class': 'facet-title'})
	for c in categories:
		temp = c.string.strip()
		subCategoryList.append(temp)
		response += temp
		response += "^"
	
	i=0
	categories = page_soup.find('div', {'id': 'facet-subj'}).findAll('a', {'class': 'facet-link'})
	for c in categories:
		categoryToLinkdataDICT[subCategoryList[i]] = c['onmousedown'].split('\'')[1]
		i+=1
	
	#get date filter and link for dropdown
	dates = page_soup.find('div', {'id': 'facet-pdate'}).findAll('span', {'class': 'facet-title'})
	for d in dates:
		temp = d.string.strip()
		dateFilterList.append(temp)
		response += temp
		response += "$"
  
	i=0
	dates = page_soup.find('div', {'id': 'facet-pdate'}).findAll('a', {'class': 'facet-link'})
	for d in dates:
		dateToLinkdataDICT[dateFilterList[i]] = d['onmousedown'].split('\'')[1]
		i+=1
	
	
	#get language filter and link for dropdown
	languages = page_soup.find('div', {'id': 'facet-lan'}).findAll('span', {'class': 'facet-title'})
	for l in languages:
		temp = l.string.strip()
		languageFilterList.append(temp)
		response += temp
		response += "#"
  
	i=0
	languages = page_soup.find('div', {'id': 'facet-lan'}).findAll('a', {'class': 'facet-link'})
	for l in languages:
		languageToLinkdataDICT[languageFilterList[i]] = l['onmousedown'].split('\'')[1]
		i+=1
	
	#get type filter and link for dropdown				#---------------change 6-------------- fetch filter values and their link info
	types = page_soup.find('div', {'id': 'facet-type'}).findAll('span', {'class': 'facet-title'})
	for t in types:
		temp = t.string.strip()
		typeFilterList.append(temp)
		response += temp
		response += "!"
  
	i=0
	types = page_soup.find('div', {'id': 'facet-type'}).findAll('a', {'class': 'facet-link'})
	for t in types:
		typeToLinkdataDICT[typeFilterList[i]] = t['onmousedown'].split('\'')[1]
		i+=1
	return HttpResponse(response)


#download the BibTex in server-side
def fetchBibTexFromSpringer(request):
	from bs4 import BeautifulSoup as soup
	import requests
	import json
	import math
	
	print("form data =", request.POST)

	#---------------------------------------get the number of pages in the search result to loop over----------------------------------------------------
	stringToSearch = request.POST['searchString']
	
	#prefix link for search
	http = 'https://www.springer.com/in/search?dnc=true&facet-type=type__book&query=' + stringToSearch
	
	
	for x in request.POST:
		if x.startswith('selectSubcategory'):
			filter_subCategory_urldata = categoryToLinkdataDICT[request.POST[x]]
			if(filter_subCategory_urldata != "---- all ----"):
				http = http + '&facet-subj=subj__'+ filter_subCategory_urldata 
		
		elif x.startswith('selectReleaseDate'):
			filter_date_urldata = dateToLinkdataDICT[request.POST[x]]
			if(filter_date_urldata != "---- all ----"):
				http = http + '&facet-pdate=pdate__' + filter_date_urldata
		
		elif x.startswith('selectLanguages'): 			
			filter_language_urldata = languageToLinkdataDICT[request.POST[x]]		
			if(filter_language_urldata != "---- all ----"):
				http = http + '&facet-lan=lan__' + filter_language_urldata	
		
		elif x.startswith('selectLiteratureType'):
			filter_type_urldata = typeToLinkdataDICT[request.POST[x]]
			if(filter_type_urldata != "---- all ----"):							#--------change 8------- update search url if user applies this filter
				http = http + '&facet-type=categorybook__' + filter_type_urldata		
				
	
	
	#http = http + '&submit=Submit'		#this is the full link
	html = requests.get(http + '&submit=Submit').text
	#print("http is ----------------------> /fetchBibTexFromSpringer ")
	#print(http)
	
	page_soup = soup(html,'html.parser')
	noOfSearchPages = page_soup.find('span', {'class': 'number-of-pages'}).string.strip()
	noOfSearchPages = noOfSearchPages.replace(',','')
	noOfSearchPages = int(noOfSearchPages)+1
	print("noOfSearchPages :",noOfSearchPages-1)
	
	#list of Parsed BibTex dictionary, each item can become vaule part of JSON object
	bibs = []

	#--------------------------------------for each page and then for each result in the page do bibTex processing----------------------------------------
	for page in range (1, noOfSearchPages):
		print("fetching results in page --->", page)
		html = requests.get(http + '&page=' + str(page) + '&submit=Submit').text
		page_soup = soup(html,'html.parser')

		result = page_soup.findAll('div', {'class': 'result-item'})   #html-container of items in search-result
		#------------------------------------------------for each search-result item------------------------------------------------------
		for item in result:
			link = 'https://www.springer.com' + item.find('h4').find('a')['href']   #link to the item's landing page
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
				
	#-----------------------------------------------------file writing stuff----------------------------------------------------------------
	itemCount = len(bibs)
	output_json = {}                    #json equivalent of the list of bibtex
	for bib in range(0, len(bibs)):
	  output_json[bib] = bibs[bib]
	
	print("BibTex Collected : ", itemCount)
	
	filename = "output.json"            #write to json file
	with open(filename, 'w') as outfile:
		json.dump(output_json, outfile)

	return sendDownloadedFile(filename)


#Send error message to client if the search result is empty i.e. springer couldn't find result for given query/filter
def isSearchValid(request):
	from bs4 import BeautifulSoup as soup
	import requests
	import json
	import math
	import ast		#for converting byte received from client (form data) to python dictionary
	
	print("checking validity of search in springer!")
	
	byte_str = request.body
	dict_str = byte_str.decode("UTF-8")
	mydata = ast.literal_eval(dict_str)				#form data to validate by visiting link
	print("form data to verify = \n",repr(mydata))
	
	#---------------------------------------get the number of pages in the search result to loop over----------------------------------------------------
	stringToSearch = mydata['searchString']
	
	#prefix link for search
	http = 'https://www.springer.com/in/search?dnc=true&facet-type=type__book&query=' + stringToSearch

	
	for x in mydata:
		if x.startswith('selectSubcategory'):
			filter_subCategory_urldata = categoryToLinkdataDICT[mydata[x]]
			if(filter_subCategory_urldata != "---- all ----"):
				http = http + '&facet-subj=subj__'+ filter_subCategory_urldata 
		
		elif x.startswith('selectReleaseDate'):
			filter_date_urldata = dateToLinkdataDICT[mydata[x]]
			if(filter_date_urldata != "---- all ----"):
				http = http + '&facet-pdate=pdate__' + filter_date_urldata
		
		elif x.startswith('selectLanguages'): 			
			filter_language_urldata = languageToLinkdataDICT[mydata[x]]		
			if(filter_language_urldata != "---- all ----"):
				http = http + '&facet-lan=lan__' + filter_language_urldata	
		
		elif x.startswith('selectLiteratureType'):
			filter_type_urldata = typeToLinkdataDICT[mydata[x]]
			if(filter_type_urldata != "---- all ----"):							#--------change 8------- update search url if user applies this filter
				http = http + '&facet-type=categorybook__' + filter_type_urldata		
				
	
	#http = http + '&submit=Submit'		#this is the full link
	html = requests.get(http + '&submit=Submit').text
	#print("checking if valid search, link = ")
	#print(http)
	
	page_soup = soup(html,'html.parser')
	try:
		noOfSearchPages = page_soup.find('span', {'class': 'number-of-pages'}).string.strip()
		return HttpResponse("valid")
	except:
		return HttpResponse("invalid")

#--------------------------------------------------------Springer specific ends here---------------------------------------------------------------------------------
