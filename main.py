from acm import *
from ieee import *
from sciencedirect import *
from springer import *

import json

def bibToJson(searchInput, bibs):
  print("total results", len(bibs))
  output_json = {}
  for bib in range(0, len(bibs)):
    # print(bib)
    output_json[bib] = bibs[bib]

  # print(output_json)

  filename = str(searchInput)    
  with open(filename, 'w') as outfile:
      json.dump(output_json, outfile)

def removeNone(searchInput):
  newInput = {}
  for key in searchInput.keys():
    print(key, searchInput[key], type(searchInput[key]), len(searchInput[key]))
    if len(searchInput[key])!=0:
      newInput[key] = searchInput[key]
      # print(key)
      # searchInput.pop(key)
  return newInput

# https://dl.acm.org/action/doSearch?fillQuickSearch=false&expand=dl&field1=AllField&text1=data&field2=Title&text2=ttl&field3=ContribAuthor&text3=auth&field4=Keyword&text4=key&field5=PubIdSortField&text5=1234
#https://dl.acm.org/action/doSearch?fillQuickSearch=false&expand=dl&field1=AllField&text1=data&AfterMonth=1&AfterYear=2018&BeforeMonth=2&BeforeYear=2020

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

# https://www.sciencedirect.com/search?qs=data&date=1995-2017&authors=divya&tak=divya&title=advanced&docId=14568632

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
  pass


def getJSON(searchInput):
  print("from getJSON", searchInput)
  bibTex = []
  searchInput = removeNone(searchInput)
  inputToACM(searchInput)
  # if searchInput['website'] == 'all':
  # searchInput.pop('website)
  bibTex.append(getACMRecords(inputToACM(searchInput)))
  # bibTex.append(getIEEERecords(inputToIEEE(searchInput)))
  # bibTex.append(getScienceDirectRecords(inputToScienceDirect(searchInput)))
  #   bibTex.append(getSpringerRecords(inputToSpringer(searchInput)))
  bibToJson(searchInput, bibTex)
  
 
    # bibTex.append(getACMRecords(inputToACM(searchInput)))
    # bibTex.append(getIEEERecords(searchInput)))
    # bibTex.append(getScienceDirectRecords(searchInput)))
    # bibTex.append(getSpringerRecords(searchInput)))
  # elif searchInput['website'] == 'acm':

  # elif searchInput['website'] == 'ieee':
  # elif searchInput['website'] == 'sciencedirect':
  # elif searchInput['website'] == 'springer':
  
