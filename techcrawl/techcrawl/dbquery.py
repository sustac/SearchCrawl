import csv
import re
import pymongo
import networkx as nx
from copy import deepcopy
from pymongo import MongoClient, ReturnDocument


##function to search the indexed fields, generate a score(word frequency) and then display in descending score order. I split the result to just show the title and url.
def text_search(collection,text):
    query = collection.find({"$text": {"$search": text}},{'score': {'$meta': 'textScore'}})
    query.sort([('score', {'$meta' : 'textScore'})])
    for item in query:
        item = str(item)
        item = item.split(', \'body\':')
        a = item[0]
        a = a.split('), ')[1]
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
                {'$group': {'_id': '$url', 'unique_ids': {'$addToSet': '$_id'}, 'count': {'$sum': 1}}},
                {'$match': {'count': { '$gte': 2 }}}
            ]
    )
    
    delete_me = []
    for doc in cursor:
        del doc['unique_ids'][0]
        for id in doc['unique_ids']:
            delete_me.append(id)

    collection.delete_many({'_id': {'$in': delete_me}})


# function to delete entire collection
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
            values.update({k:v})
    
    
    for k,v in values.items():
        k = re.sub('\"', '', k)
        k = re.sub(' ', '', k)
        collection.find_one_and_update({"domain": k},
                                        {'$set': {'pagerank' : v}},
                                        return_document=ReturnDocument.AFTER)

def main():

    ###### LOCALHOST CONNECTION
    client = MongoClient()
    
    ##### defaulting to index.pages collection as of now, where the crawler is storing the data.
    db = client.index
    collection = db.pages

    answer = ''

    print("\n")
    print("If you are creating a new collection then you need to run index first!!!!!!")
    print("Index creates a test document to insert(so db/collection is saved) and then creates an index so we can search.")
    print("If index is created already and you want to crawl more pages just enter quit.")
    print("Remove duplicates deletes all duplicates in database collection, should be run before pagerank and search commands.")
    print("You need to run pagerank every time you add new pages to the collection if you want the pagerank score to search on. not necessary.")  
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
            text = input("Enter term you would like to search for: ")
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





