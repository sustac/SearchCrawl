import csv
import re
import os
import pymongo
import networkx as nx
from copy import deepcopy
from pymongo import MongoClient, ReturnDocument


#function to search the indexed fields, generate a score(word frequency) and then display in descending score order. 
#I split the result to just show the title and url.
def text_search(collection,text):

    query1 = collection.find({"$text": {"$search": text}},{'score': {'$meta': 'textScore'}}).limit(15)    
    for item in query1:
        if item['score_added'] is not 1:
            score = item['score'] + item['pagerank']
            collection.update_one({
                '_id': item['_id']
            },{
                '$set':{ 'score' : score, 'score_added' : 1}
            })
        else:
            pass
  
    
    query = collection.find({"$text": {"$search": text}},{'score': {'$meta': 'textScore'}}).limit(15)
    query.sort([('score', {'$meta' : 'textScore'})])

    for item in query:         
        item = str(item)
        item = item.split(', \'domain\':')
        a = item[1]
        print("{}" .format(a))




#function to create indexed fields to enable text search of them, also insert a dummy document to be able to have an index(cant index nothing).
def create_index(collection):
    mydict = { "title" : "x", "url" : "w", "body" : "testtesttest", "domain" : "test.com" }
    collection.insert_one(mydict)
    collection.create_index([("title" , pymongo.TEXT), ("url" , pymongo.TEXT), ("body", pymongo.TEXT), ("domain", pymongo.TEXT)], default_language='english')


# function to loop through the collection and remove duplicates, insanely hard to avoid duplicates and not throw errors while crawling.
def remove_duplicates(collection):
    cursor = collection.aggregate(
            [
                {'$group': {'_id': '$domain', 'unique_ids': {'$addToSet': '$_id'}, 'count': {'$sum': 1}}},
                {'$match': {'count': { '$gte': 2 }}}
            ]
    )
    
    delete_me = []
    for doc in cursor:
        del doc['unique_ids'][0]
        for id in doc['unique_ids']:
            delete_me.append(id)

    collection.delete_many({'_id': {'$in': delete_me}})


# function to delete entire collection, will delete the current collection being accessed
def remove_collection(collection):
    choice = input("better be bloody sure mate! y to delete, n to back out while you still can: ")
    if choice == 'n':
        print('good call')
        print("\n")
    
    else:
        collection.drop()
        print("collection dropped")
        print("\n")

# function to create pagerank scores and then add them to the pagerank field in the collection. utilizing networkx!
def add_pagerank(collection):
    rows = []
    
    files = [f for f in os.listdir(os.curdir) if os.path.isfile(f)]
    print('\n')
    print('These are the csv files in current directory: ')
    [print(f) for f in files if f.endswith('.csv')]
    print('\n')
    page = input("please enter csv file name including .csv: ")

    with open(page, "r") as f:
        readCSV = csv.reader(f, delimiter=',')

        for row in readCSV:
            rows.append(row)

    rows = rows[:-1]

    G = nx.DiGraph()

    rows = [str(row) for row in rows]

    for item in rows:

        item = re.sub('https://', '', item)
        item = re.sub('http://', '', item)
        item = re.sub('www.', '', item)
        item = re.sub('\[', '', item)
        item = re.sub('\]', '', item)
        item = re.sub('\"', '', item)
        item = item.split(',')
        v = item[0]
        e = item[1]
        G.add_edge(v, e)

    page_rank = nx.pagerank_numpy(G, alpha=0.9)
    
    mypages = collection.distinct('domain')
    
    values = {}

    for k,v in page_rank.items():
        k = re.sub('\"', '', k)
        k = re.sub(' ', '', k)
        k = re.sub('\'', '', k)
        if k in mypages:
            if k not in values:
                values.update({k:v})
    
    for k,v in values.items():
        k = re.sub('\"', '', k)
        k = re.sub(' ', '', k)
        v = float(v)
# left shift pagerank value by 2 to make more of an impact        
        v *= 100
        collection.find_one_and_update({"domain": k},
                                        {'$set': {'pagerank' : v}},
                                        return_document=ReturnDocument.AFTER, modifiers={'$snapshot': True} )
        


#Change collection configuration in settings.py for mongodb
def change_collection(new_collection):
    with open('settings.py') as my_settings:
        lines = my_settings.readlines()
    
    f = open('settings.py', 'w')
    for line in lines:
        if line.startswith('MONGODB_COLLECTION'):
            line = 'MONGODB_COLLECTION = ' + '\''+ new_collection +'\'' + '\n'
            f.write(line)
        else:
            f.write(line)

    f.close()

#list collection in the index database
def list_collections(db):
    print('\n')
    print("The collections in the index database are: ")
    show = db.list_collection_names()
    for item in show:
        print(item)

def main():
    ###### LOCALHOST CONNECTION
    client = MongoClient()
        
    ##### Set database to index and then set collection to use / set collection name in settings file
    db = client.index
    
    print(list_collections(db))       
    print('\n')    
    my_collection = input("Enter collection to use(or create new one): ")
    change_collection(my_collection)
    collection = db[my_collection]

    answer = ''

    print("\n")
    print("If you are creating a new collection then you need to run index first!!!!!!")
    print("Index creates a test document to insert(so db/collection is saved) and then creates an index so we can search.")
    print("Only need to create index one time for a collection")
    print("Remove duplicates deletes all duplicates in database collection, should be run before pagerank and search commands.")
    print("Only need to remove duplicates when new content added to collection(scraped data).")
    print("You need to run pagerank every time you add new pages to the collection(uses .csv file to generate pagerank).")  
    print("Search allows you to search for specific terms in the collection you specify.")
    print("Remove allows you to entirely remove your specified collection.")
    print("\n")

    while(answer is not 'quit'):
        answer = input("enter index, remove duplicates, pagerank, search, remove(quit to terminate): ")
        if answer == 'quit':
            answer = 'quit'
        
        elif answer == 'index':
            create_index(collection)
            print("\n")
        
        elif answer == 'remove duplicates':
            remove_duplicates(collection)
            print("\n")
            
        elif answer == 'pagerank':
            add_pagerank(collection)
            print("\n")
        
        elif answer == 'search':
            while(text is not 'quit'):
                text = input("Enter term you would like to search for(quit to return to menu): ")
                if text == 'quit':
                    break;
                else:
                    print("\n")
                    text_search(collection,text)
                    print("\n")
        
        elif answer == 'remove':
            remove_collection(collection)
            print("\n")

        else:
            print("that is not a choice you can choose!")
            print("\n")



main()




