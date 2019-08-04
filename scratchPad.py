# x = 2
# y =y = 3

# print(x + y)

# for n in range(1, 1000000): 
#     print(n)



"""
import threading

def f(f_stop):
    # do something here ...
    print('wutt')

    if not f_stop.is_set():
        # call f() again in 60 seconds
        threading.Timer(1, f, [f_stop]).start()

f_stop = threading.Event()
# start calling f now and every 60 sec thereafter
f(f_stop)

# stop the thread when needed
#f_stop.set()
"""



import requests
import json
from myConfig import *
import uuid

url1 = "https://api.todoist.com/sync/v8/sync"
data1 = {
        'token': userToken,
        'sync_token': "* \\",
        'resource_types':'["projects"]'
}

allProjects = requests.get(url1, data1)

f = open("data1.json", 'w')
f.write( str( allProjects.text ) )
f.close()

# print(allProjects.json())



url2 = "https://api.todoist.com/sync/v8/sync"
data2 = {
        'token': userToken,
        'sync_token': "* \\",
        'resource_types':'["items"]'
}

items = requests.get(url2, data2)

f = open("items.json", 'w')
f.write( str( items.text ) )
f.close()

# print(items.text)

print("get all project's returned sync_token", allProjects.json()["sync_token"])

url3 = "https://api.todoist.com/sync/v8/sync"
data3 = {
        'token': userToken,
        'sync_token': allProjects.json()["sync_token"],
        'resource_types':'["items"]',
        'commands': '[{"type": "item_close","uuid": "' + str(uuid.uuid4()) + '","args": { "id": 3326429409 } }]'
}

completeItem = requests.get(url3, data3)

f = open("completeItem.json", 'w')
f.write( str( completeItem.text ) )
f.close()

print(completeItem.text)