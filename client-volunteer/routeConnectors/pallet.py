import urllib3
from .rootName import root
import json
import ast

#root = rootName.root
curPath = "/api/pallet"

http = urllib3.PoolManager()

def getFood():
  r = http.request("GET", root + curPath + "/", headers={'Content-Type': 'application/json'})
  return r.data.decode('utf-8')

def postFood(entryUserId, inputDate, expirationDate, weight, companyId, rackId, description, categoryId):
  jsonDict = {
    "entryUserId": entryUserId,
    "inputDate": inputDate.isoformat(),
#    "expirationDate": expirationDate.isoformat(),
    "weight": int(weight),
    "companyId": companyId,
    "description": description,
    "categoryIds": [categoryId]
  }
  
  if expirationDate.year != 1970:
    jsonDict["expirationDate"] = expirationDate.isoformat()
  if rackId > 0:
    jsonDict["rackId"] = rackId
  f = json.dumps(jsonDict)
  r = http.request("POST", root + curPath + "/", body=f, headers={'Content-Type': 'application/json'})
  return r.data.decode('utf-8')

def deleteFood(idField):
  r = http.request("DELETE", root + curPath + "/" + idField, headers={'Content-Type': 'application/json'})
  return r.data

def updateFood(idField, entryUserId, inputDate, expirationDate, weight, companyId, rackId, description, categoryId):
  f = json.dumps({
    "entryUserId": entryUserId,
    "inputDate": inputDate,
    "expirationDate": expirationDate,
    "weight": weight,
    "companyId": companyId,
    "rackId": rackId,
    "description": description,
    "categoryId": categoryId
  })
  r = http.request("POST", root + curPath + "/edit/" + idField, body=f, headers={'Content-Type': 'application/json'})
  return r.data.decode('utf-8')