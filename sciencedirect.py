from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import csv
import sys
import urllib
from urllib.error import HTTPError
from requests_html import HTMLSession
import requests

def getSearchString(searchInput):
  print("from get search string", searchInput)
  searchString = ""
  for key,val in searchInput.items():
    print(key, val)
    if len(val) > 0:
        searchString += key +'=' + val + '&' 
  searchString = searchString[:-1]
  searchString = searchString.replace(' ', '%20')
  return searchString

def getUrls(searchString):
  print("\nfrom getUrls", searchString)
  individual_urls = []
  try:
    session = HTMLSession()
    off = 0
    show = '&show=100'
    sd_url = 'https://www.sciencedirect.com/search?' + searchString
    print(sd_url)
    # https://www.sciencedirect.com/search?qs=data%20science&authors=divya&tak=star
    r = session.get(sd_url)
  except Exception as e:
    print(repr(e), 'First page accessing error')
    return individual_urls
  page_soup = soup(r.text, "html.parser")
  result_count = 0
  results = "0"
  try:
    results = page_soup.find("span", {"class" : "search-body-results-text"}).text
  except:
    try:
      results = page_soup.find("h1", {"class" : "search-body-results-text"}).text
    except:
      return individual_urls
  result_count = int((results.strip().split()[0]).replace(',', '').replace('+', ''))
  print("results", result_count)
  while(off<result_count):
    print(off)
    offset = "&offset=" + str(off)
    off += 100
    sd_url = 'https://www.sciencedirect.com/search?' + searchString + show + offset
    print(sd_url)
    try:
      r = session.get(sd_url)
      page_soup = soup(r.text, "html.parser")
      containers = page_soup.findAll("a", {"class" : "result-list-title-link"})
    except Exception as e:
      print(repr(e), 'Page accessing error :', off/100+1)
      continue
    url_prefix = "https://www.sciencedirect.com"
    for container in containers:
      try:
        container = container["href"];
        paper_url = url_prefix + container
        individual_urls.append(paper_url)
        # print(paper_url)
      except Exception as e:
          print(repr(e), 'Document link not available')
  print(len(individual_urls))
  return individual_urls


# url = 'https://www.sciencedirect.com/sdfe/arp/cite'
# suffix = '?pii=S0264410X18315482&format=text%2Fx-bibtex&withabstract=true'


def getBibTex(individual_urls):
  headers = {
      'user-agent': 'My User Agent 1.0',
  }
  sd_url = 'https://www.sciencedirect.com/sdfe/arp/cite'
  params = {
      'pii': None,
      'format': 'text/x-bibtex',
      'withabstract': 'true',
  }

  bibs_responses = []
  for url in individual_urls:
    ind = len(url) - 1 - url[::-1].index('/')
    pii = url[ind+1:]
    print(pii)
    params['pii'] = pii
    # print(params)
    bibs_responses.append(requests.get(sd_url, headers=headers, params=params).text)
    # print(response.text)

  print(len(bibs_responses))
  bibs = []
  for bib in bibs_responses:
    # print(bib)
    try:
      bibtex = bib.strip("}").strip("\t ") + '\n'
      # print(bibtex)
      ind = bibtex.index("{")
      bib_dict = {}
      bib_dict["type"] = bibtex[:ind]
      bibtex = bibtex[ind+1:]
      ind = bibtex.index("\n")
      bib_dict["id"] = bibtex[:ind-1]
      bibtex = bibtex[ind+1:]
      while(bibtex != "" and bibtex != "\n"): #len(bibtext) > 3):
        # print(bibtex)
        # print("bib", bibtex, len(bibtex))
        ind = bibtex.index("\n")
        if bibtex[:8] == 'abstract':
          ind = len(bibtex)
          bibtex = bibtex.replace('\n', '')
        attribute = bibtex[:ind].strip("\t,")
        ind_attr = attribute.index("=")
        # print(attribute)
        bib_dict[attribute[:ind_attr].strip()] = attribute[ind_attr+1:].strip()
        bibtex = bibtex[ind + 1:]
      # pprint.p
      # print(bib_dict)
      bibs.append(bib_dict)
    except Exception as e:
      print(e, attribute)
      break
      # print(e, bib)
      continue
  return bibs

def getScienceDirectRecords(searchInput, bibTex):
  searchString = getSearchString(searchInput)
  print(searchString)
  recordIds = getUrls(searchString)
  bibTex += getBibTex(recordIds)
  print("total bibs from scienceDirect", len(bibTex))
  return bibTex

# getScienceDirectRecords("hgf")
