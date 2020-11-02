from bs4 import BeautifulSoup as sp
import requests
import json

def getDOI(citation):
	try:
		title = citation.find("span",{"class":"hlFld-Title"})
		for a in title.findAll("a", href=True):
			dois = a['href']
		dois = dois[5:]
		if dois[0] not in {'0','1','2','3','4','5','6','7','8','9'}:
			dois = dois[12:]
	except:
		dois = "Error Finding DOI"
	return dois

def parsed_bibText(dois):
	# try:
	url = "https://dl.acm.org/action/exportCiteProcCitation"
	data = {'dois':dois,'targetFile':'custom-bibtex','format':'bibTex'}
	try:
		response = requests.post(url,data = data).json()
		bib = {}
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
		bib = "Error Fetching BibText for doi = "+dois
	return bib


def scrape(parsed_html):
	contents = parsed_html.findAll("div",{"class":"issue-item issue-item--search clearfix"})
	print("no. of contents = ",len(contents))
	for citation in contents:
		dois = getDOI(citation)
		print("dois = ",dois)
		bibText = parsed_bibText(dois)
		# count += 1
		print("bib = ",json.dumps(bibText,indent=2))
		# return

def main():
	myurl = str(input("Search:"))
	myurl.replace(' ','+')
	myurl = "https://dl.acm.org/action/doSearch?fillQuickSearch=false&expand=dl&field1=AllField&text1="+myurl

	x = requests.get(myurl)
	parsed_html = sp(x.text,"html.parser")

	totalNumber = int(parsed_html.find("span",{"class":"hitsLength"}).string.strip().replace(',',''))
	totalPages = int(totalNumber/20)
	print("Total Results: ",totalNumber)
	print("Total Pages: ",totalPages)


	# Extract first page
	scrape(parsed_html)
	# return

	for i in range(1,totalPages+1):
		print("Page ",i)
		try:
			next_page = myurl + "&pageSize=20&startPage="+str(i)
			x = requests.get(next_page)
			parsed_html = sp(x.text,"html.parser")
			scrape(parsed_html)
		except KeyboardInterrupt:
			print("Exiting...")
			return


if __name__ == '__main__':
	main()