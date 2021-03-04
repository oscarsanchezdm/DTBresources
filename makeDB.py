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

#write DB to a file
newDB = hashlist
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