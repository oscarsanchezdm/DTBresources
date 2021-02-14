from os import listdir
from os.path import isfile, join
import pandas as pd
from hashlib import sha256

#resources and db paths
#hashlist.csv must be included. it must be a CSV file separated by \n that contains SHA256 hashes
resources_path = "./resources/"
hashlist_path = "hashlist.csv"
newdb_path = "resourcelist.csv"

#import db
hashlist = pd.read_csv(hashlist_path,header=None)

#get resources list
resource_list = [f for f in listdir(resources_path) if not f.startswith('.') and isfile(join(resources_path, f))]
resource_list.sort()

#add a column to the hashlist
newDB = hashlist
newDB[1] = 0

#search for matches
r = 0
for i in range(0,len(hashlist)):
    if len(resource_list) <= r:
        break

    act_hash = hashlist.at[i,0]
    act_resource = resource_list[r]

    while (act_resource < act_hash):
        r = r+1
        if len(resource_list) <= r:
            stop = True
            break
        act_resource = resource_list[r]

    if (act_resource == act_hash):
        newDB.at[i,1] = 1

#write DB to a file
newDB.to_csv(newdb_path, index=False, header=False)

#generate DB file hash and write it to a file
def hash_file(filename, hash_func=sha256):
    h = hash_func()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)

    return h.hexdigest()

filehash = hash_file(newdb_path)

newdb_hash_file = open("resourcelist_hash.txt","w")
newdb_hash_file.write(filehash)
newdb_hash_file.close()