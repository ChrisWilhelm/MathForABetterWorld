import urllib3
from .rootName import root
import json
import ast

#root = rootName.root
curPath = "/api/location"

http = urllib3.PoolManager()

def getLocations():
  r = http.request("GET", root + curPath + "/", headers={'Content-Type': 'application/json'})
  return ast.literal_eval(r.data.decode('utf-8'))

def postLocation(name, longitude, latitude, isActive):
  f = json.dumps( {
    "name": name,
    "longitude": longitude,
    "latitude": latitude,
    "isActive": isActive
  })
  r = http.request("POST", root + curPath + "/", body=f, headers={'Content-Type': 'application/json'})
  return r.data.decode('utf-8')

def deleteLocation(idField):
  r = http.request("DELETE", root + curPath + "/" + str(idField), headers={'Content-Type': 'application/json'})
  return r.data

def updateLocation(idField, name, longitude, latitude, isActive):
  f = json.dumps({
    "name": name,
    "longitude": longitude,
    "latitude": latitude,
    "isActive": isActive,
  })
  r = http.request("POST", root + curPath + "/" + str(idField) + "/" + "update", body=f, headers={'Content-Type': 'application/json'})
  return r.data

def getVisitsPerLocation():
  r = http.request("GET", root + curPath + "/visitsPerLocation/", headers={'Content-Type': 'application/json'})
  return r.data.decode('utf-8')
  
def getWeightsPerLocation():
  r = http.request("GET", root + curPath + "/weightPerLocation/", headers={'Content-Type': 'application/json'})
  return r.data.decode('utf-8')