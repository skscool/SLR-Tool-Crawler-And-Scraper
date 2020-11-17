import csv
import sys
import requests
import math

ranges = ""
def getSearchString(searchInput):
  ranges = '"1872_2021_Year"'
  print("from get search string", searchInput)
  searchString = ""
  flag = False
  prefix = ""
  l = len('(\\"Document Title\\":')
  for key,val in searchInput.items():
    print(key, val)
    if len(val) > 0:
      if key == 'ranges':
        ranges = val
        continue
      if len(key)> l and key[:l] == '(\\"Document Title\\":':
        prefix = '(' + key +':' + val + ') AND '
        continue
      if flag:
        searchString = '(' + searchString + ' AND \\"' + key +'\\":' + val + ')' 
      else:
        searchString = '(' + '\\"' + key +'\\":' + val + ')'
        flag = True
  if prefix != "":
    for i in range(0, len(searchString)):
      if searchString[i]!='(':
        temp = searchString[:i] + prefix + searchString[i:]
        searchString = temp
        break
  return '\"' + searchString + '\"'

def getRecordIds(searchString):
  print("search string", searchString)
  headers = {
      'Content-Type': 'application/json',
      'Origin': 'https://ieeexplore.ieee.org',
  }
  pageNo = 1
  recordIds = []
  totalPages = pageNo
  while(pageNo<=totalPages):
    try:
      data = '''{"action":"search",
      "newsearch":true,
      "matchBoolean":true,
      "queryText":''' + searchString + ''',
      "ranges":[''' + ranges + '''],
      "highlight":true,
      "returnFacets":["ALL"],
      "returnType":"SEARCH",
      "matchPubs":true,
      "rowsPerPage":"100",
      "pageNumber":''' + str(pageNo) +'}'

      response = requests.post('https://ieeexplore.ieee.org/rest/search', headers=headers, data=str(data))
      # print("received response")
      response = response.json()
      # print(response)
      # print(len(response['records']))
      # print("processing response")
      splitInd = len('/document/')
      totalRecords = response['totalRecords']
      totalPages = math.ceil(totalRecords/100)
      recordsCount = min(totalRecords - (pageNo-1)*100, 100)
      records = response['records']
      print("totalPages:",totalPages, "totalRecords:", totalRecords, "pageNo:", pageNo, "records count: ", recordsCount)
      # print(response)
    except Exception as e:
      print(repr(e), 'No such page exists :', (pageNo))
      pageNo+=1
      continue
    for recordInd in range(0, recordsCount):
      # print(records[0]['documentLink'][splitInd:-1])
      # print(recordInd)
      try:
        recordIds.append(records[recordInd]['documentLink'][splitInd:-1])
        # print(recordInd, records[recordInd]['documentLink'][splitInd:-1])
      except Exception as e:
        print(repr(e), 'Document link not available :', recordInd+(pageNo-1)*100+1)
    pageNo+=1
  print(len(recordIds))
  return recordIds


def getBibTex(recordIds):
  bibs = []
  headers={
      'Accept': 'application/json',
      # 'Content-Type':'application/json'
  }
  data={
      'recordIds' : None,
      'download-format' : 'download-bibtex',
      'citations-format' :'citation-abstract'
  }
  url = 'https://ieeexplore.ieee.org/xpl/downloadCitations'
  for recordId in recordIds:
    try:
      print(recordId)
      data['recordIds'] = str(recordId)
      response = requests.post(url, headers=headers, data=data) 
      bib = response.text
    except Exception as e:
      print(repr(e), 'BibTeX accessing error :', (recordId))
      continue
    # print(bib)
    bib = bib.replace("<br>", "")
    # print(bib)
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
      # print("attr",attribute)
      try:
        ind_attr = attribute.index("=")
      except Exception as e:
        bibtex = bibtex[1:]
        continue
      # print(ind_attr)
      bib_dict[attribute[:ind_attr].strip()] = attribute[ind_attr+1:].strip('{} \r,')
      bibtex = bibtex[ind + 1:]
    # print(bib_dict)
    bibs.append(bib_dict)
  print("from ieee", len(bibs))
  return bibs


def getIEEERecords(searchInput):
  searchString = getSearchString(searchInput)
  print(searchString)
  recordIds = getRecordIds(searchString)
  bibTex = getBibTex(recordIds)
  return bibTex

# getIEEERecords("hgf")
