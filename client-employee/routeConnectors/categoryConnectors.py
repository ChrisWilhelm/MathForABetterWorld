import urllib3
from .rootName import root
import json
import ast

#root = rootName.root
curPath = "/api/category"

http = urllib3.PoolManager()

def getCategories():
  r = http.request("GET", root + curPath + "/", headers={'Content-Type': 'application/json'})
  return ast.literal_eval(r.data.decode('utf-8'))

def postCategory(name, desc, isActive):
  f = json.dumps( {
    "name": name,
    "description": desc,
    "isActive": isActive
  })
  r = http.request("POST", root + curPath + "/", body=f, headers={'Content-Type': 'application/json'})
  return r.data.decode('utf-8')

def deleteCategory(idField):
  r = http.request("DELETE", root + curPath + "/" + str(idField), headers={'Content-Type': 'application/json'})
  return r.data

def updateCategory(idField, name, desc, isActive):
  f = json.dumps({
    "name": name,
    # "id": idField,
    "description": desc,
    "isActive": isActive
  })
  r = http.request("POST", root + curPath + "/" + str(idField) + "/" + "update", body=f, headers={'Content-Type': 'application/json'})
  return r.data
