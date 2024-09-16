import urllib3
from .rootName import root
import json
import ast

#root = rootName.root
curPath = "/api/rack"

http = urllib3.PoolManager()

def getRacks():
  r = http.request("GET", root + curPath + "/", headers={'Content-Type': 'application/json'})
  return ast.literal_eval(r.data.decode('utf-8'))


def postRack(location, desc, weightLimit, isActive):
  f = json.dumps({
    "location": location,
    "description": desc,
    "weightLimit": weightLimit,
    "isActive": isActive
  })
  r = http.request("POST", root + curPath + "/", body=f, headers={'Content-Type': 'application/json'})
  return r.data.decode('utf-8')

def deleteRack(idField):
  r = http.request("DELETE", root + curPath + "/" + str(idField), headers={'Content-Type': 'application/json'})
  return r.data

def updateRack(idField, location, desc, weightLimit, isActive):
  f = json.dumps({
    "location": location,
    "description": desc,
    "weightLimit": weightLimit,
    "isActive": isActive
  })
  r = http.request("POST", root + curPath + "/update/" + str(idField), body=f, headers={'Content-Type': 'application/json'})
  return r.data.decode('utf-8')