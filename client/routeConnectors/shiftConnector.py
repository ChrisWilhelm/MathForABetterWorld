import urllib3
import json
#import rootName
from .rootName import root

#root = rootName.root
curPath = "/api/shift"

http = urllib3.PoolManager()

def getShifts():
  r = http.request("GET", root + curPath + "/", headers={'Content-Type': 'application/json'})
  return r.data

# times must be ISO 8601 times
def postShift(userId, startTime):
  f = json.dumps({
    "userId": userId,
    "start": startTime,
  })
  r = http.request("POST", root + curPath + "/", body=f, headers={'Content-Type': 'application/json'})
  return r.data.decode('utf-8')

def deleteShift(idField):
  r = http.request("DELETE", root + curPath + "/" + idField, headers={'Content-Type': 'application/json'})
  return r.data

def updateShift(idField, userId, startTime, endTime, foodWeightTaken):
  f = json.dumps({
    "id": idField,
    "userId": userId,
    "start": startTime,
    "end": endTime,
    "foodTaken": foodWeightTaken
  })
  r = http.request("POST", root + curPath + "/update", body=f, headers={'Content-Type': 'application/json'})
  return r.data.decode('utf-8')

def signout(foodTaken, id):
  f = json.dumps({
    "id": id,
    "foodTaken": foodTaken
  })
  r = http.request("POST", root + curPath + "/signout", body=f, headers={'Content-Type': 'application/json'})
  return r.data.decode('utf-8')

def activeShifts():
  r = http.request("GET", root + curPath + "/activeshifts", headers={'Content-Type': 'application/json'})
  return r.data