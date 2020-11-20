from acm import *
from ieee import *
from sciencedirect import *
from springer import *
import copy
import json
import multidict
import threading 

def bibToJson(fileName, bibs):
  print("total results", len(bibs))
  output_json = {}
  for bib in range(0, len(bibs)):
    output_json[bib] = bibs[bib]
  # print(output_json)
  # filename = 'output.json'   
  with open(fileName, 'w') as outfile:
      json.dump(output_json, outfile)

def removeNone(searchInput):
  newInput = {}
  for key in searchInput.keys():
    if len(searchInput[key])!=0:
      newInput[key] = searchInput[key]
  return newInput

def inputToACM(searchInput):
  try:
    searchInput['AllField'] = searchInput.pop('basic')
  except:
    pass
  try:
    searchInput['PubIdSortField'] = searchInput.pop('isbn')
  except:
    pass
  try:
    searchInput['PubIdSortField'] = searchInput.pop('issn')
  except:
    pass
  try:
    searchInput['ContribAuthor'] = searchInput.pop('author')
  except:
    pass
  try:
    searchInput['Keyword'] = searchInput.pop('authSpecKey')
  except:
    pass
  try:
    searchInput['date'] = 'AfterMonth=1&AfterYear=' + searchInput.pop('yearStart') + '&BeforeMonth=12&BeforeYear=' + searchInput.pop('yearEnd')
  except:
    pass
  try:
    searchInput['Title'] = searchInput.pop('title')
  except:
    pass
  print("input to ACM", searchInput)
  return searchInput

def inputToIEEE(searchInput):
  try:
    searchInput['Full Text .AND. Metadata'] = searchInput.pop('basic')
  except:
    pass
  try:
    searchInput['ISBN'] = searchInput.pop('isbn')
  except:
    pass
  try:
    searchInput['ISSN'] = searchInput.pop('issn')
  except:
    pass
  try:
    searchInput['Authors'] = searchInput.pop('author')
  except:
    pass
  try:
    searchInput['Author Keywords'] = searchInput.pop('authSpecKey')
  except:
    pass
  try:
    searchInput['ranges'] =  '\"' + searchInput.pop('yearStart') + '_' + searchInput.pop('yearEnd') + '_Year\"'
  except:
    pass
  try:
    title = searchInput.pop('title')
    key = '(\\"Document Title\\":' + title + ') OR \\"Publication Title\\"'
    searchInput[key] = title
  except:
    pass
  print("input to IEEE", searchInput)
  return searchInput

def inputToScienceDirect(searchInput):
  try:
    searchInput['qs'] = searchInput.pop('basic')
  except:
    pass
  try:
    searchInput['docId'] = searchInput.pop('isbn')
  except:
    pass
  try:
    searchInput['docId'] = searchInput.pop('issn')
  except:
    pass
  try:
    searchInput['authors'] = searchInput.pop('author')
  except:
    pass
  try:
    searchInput['tak'] = searchInput.pop('authSpecKey')
  except:
    pass
  try:
    searchInput['date'] =  searchInput.pop('yearStart') + '-' + searchInput.pop('yearEnd')
  except:
    pass
  print("input to Science Direct", searchInput)
  return searchInput

def inputToSpringer(searchInput):
  try:
    searchInput['queryText'] = searchInput.pop('basic')
  except:
    pass
  try:
    searchInput['isbnIssn'] = searchInput.pop('isbn')
  except:
    pass
  try:
    searchInput['isbnIssn'] = searchInput.pop('issn')
  except:
    pass
  try:
    searchInput['authorEditor'] = searchInput.pop('author')
  except:
    pass
  try:
    searchInput['Author Keywords'] = searchInput.pop('authSpecKey')
  except:
    pass
  try:
    searchInput['ranges'] =  '\"' + searchInput.pop('yearStart') + '_' + searchInput.pop('yearEnd') + '_Year\"'
  except:
    pass
  print("input to Springer", searchInput)
  return searchInput

def getJSONAll(searchInput, fileName):
  print("\nfrom getJSONALL", searchInput)
  bibTex = [[], [], [], []]
  t = [None]*4
  searchInput = removeNone(searchInput)
  t[0] = threading.Thread(target=getACMRecords, args=(inputToACM(searchInput.copy()),bibTex[0])) 
  t[1] = threading.Thread(target=getIEEERecords, args=(inputToIEEE(searchInput.copy()),bibTex[1]))
  t[2] = threading.Thread(target=getScienceDirectRecords, args=(inputToScienceDirect(searchInput.copy()),bibTex[2])) 
  t[3] = threading.Thread(target=getSpringerRecords, args=(inputToSpringer(searchInput.copy()),bibTex[3]))
  for i in range(4):
    t[i].start()
  for i in range(4):
    t[i].join()
  print(len(bibTex[0]))
  print(len(bibTex[1]))
  print(len(bibTex[2]))
  print(len(bibTex[3]))

  # bibTex += getACMRecords(inputToACM(searchInput.copy()))
  # bibTex += getIEEERecords(inputToIEEE(searchInput.copy()))
  # bibTex += getScienceDirectRecords(inputToScienceDirect(searchInput.copy()))
  # bibTex += getSpringerRecords(inputToSpringer(searchInput.copy()))
  bibTex = bibTex[0]+bibTex[1]+bibTex[2]+bibTex[3]
  bibToJson(fileName, bibTex)

def processInput(searchInput):
  size = ceil(len(searchInput)/2)+1
  key = "selectSearchWithin"
  val = "textSearchWithin"
  newSearchInput = multidict.MultiDict()
  for i in range(1, size):
    try:
      k = key + str(i)
      v = val + str(i)
      newSearchInput.add(searchInput[k], searchInput[v])
    except:
      break
  print(newSearchInput)
  return newSearchInput

def getJSONACM(searchInput, fileName):
  # print("\nfrom getJSONACM", searchInput)
  searchInput = removeNone(searchInput)
  searchInput = processInput(searchInput)
  print("\n\n\n", searchInput)
  bibTex = []
  bibTex = getACMRecords(searchInput.copy(), bibTex)
  bibToJson(fileName, bibTex)

def getJSONIEEE(searchInput, fileName):
  # print("\nfrom getJSONIEEE", searchInput)
  searchInput = removeNone(searchInput)
  searchInput = processInput(searchInput)
  print("\n\n\n", searchInput)
  bibTex = []
  bibTex = getIEEERecords(searchInput.copy(), bibTex)
  bibToJson(fileName, bibTex)

def getJSONScienceDirect(searchInput, fileName):
  # print("\nfrom getJSONScienceDirect", searchInput)
  searchInput = removeNone(searchInput)
  print("\n\n\n", searchInput)
  bibTex = []
  bibTex = getScienceDirectRecords(searchInput.copy(), bibTex)
  bibToJson(fileName, bibTex)
