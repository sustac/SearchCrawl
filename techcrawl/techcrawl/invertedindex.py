import re
import sys
import json

x = 0
word_count = 0.0
class Appearance:
    #appearance of term and frequency

    def __init__(self, docId, frequency):
        self.docId = docId
        self.frequency = frequency

        
    def __repr__(self):
        return str(self.__dict__)

class Database:
    # in memory DB just a dictionary
    # functions for standard update,delete and get on dicts

    def __init__(self):
        self.db = dict()

    def __repr__(self):
        return str(self.__dict__)

    
    def get(self, id):
        return self.db.get(id, None)

    
    def add(self, document):
        return self.db.update({document['id']: document})

    def remove(self, document):
        return self.db.pop(document['id'], None)



class InvertedIndex:
    # Indexing happens here
    
    def __init__(self, db):
        self.index = dict()
        self.db = db

    def __repr__(self):
        return str(self.index)

        
    def index_document(self, document):
        global word_count
        # Remove punctuation and stopwords, also make everything lowercase to avoid problems.
        stopword = []
        text = re.sub(r'[^\w\s]','', document['text'])
        for line in open('stopwords.txt'):
            stopword.append(line)
        text = text.lower()
        terms = text.split(' ')
        terms = [ word for word in terms if word not in stopword]
        appearances_dict = dict()

        # Dictionary with term and frequency
    
        for term in terms:
            term_frequency = appearances_dict[term].frequency if term in appearances_dict else 0
            appearances_dict[term] = Appearance(document['id'], term_frequency + 1)
            
        # Update the index
        update_dict = { key: [appearance]
                       if key not in self.index
                       else self.index[key] + [appearance]
                       for (key, appearance) in appearances_dict.items() }

        self.index.update(update_dict)

        # Add the document 
        self.db.add(document)
        word_count = float(len(self.index))
#       print(word_count)

        return document


    def lookup_query(self, query):
        ### make query lower case to match text!!!
        query = query.lower()
        return { term: self.index[term] for term in query.split(' ') if term in self.index }


def highlight(id, term, text):
    ### make text lower case so the term is always highlighted
    text = text.lower()
    replaced_text = text.replace(term, "\033[1;32;40m {term} \033[0;0m".format(term=term))
    return "--- line {id}: {replaced}".format(id=id, replaced=replaced_text)


def main():
    db = Database()
    index = InvertedIndex(db)
    x = 0
    global word_count
    page = input("please enter json file to index, including the .json: ")

    with open( page, "r") as f:
        data = json.load(f)

    for line in data:
        document = {
            'id': x,
            'text' : str(line)
        }
        index.index_document(document)
        x += 1    
    
    answer = 'y'
    while(answer != 'quit'):
        print("\n")
        search_term = input("Enter term(s) to search for text and line # or" "\n"
                                 "enter freq to get frequency of certain word or" "\n"
                                 "enter clear to clear the terminal: ")
        
        print("\n")
        
        if search_term == 'freq':
            query = input("enter term for frequency: ")
            print("\n")
            result = index.lookup_query(query)
            frequency = 0
            if(query in result):
                frequency = float(len(result[query]))
                frequency = float(frequency/word_count)
            print("The frequency of {} is {}" .format(query, frequency))
            print("\n")
            answer = input("enter quit to stop searching, y to continue:")
            print("\n")

        elif search_term == 'clear':
            sys.stderr.write("\x1b[2J\x1b[H")
            
        else:
            result = index.lookup_query(search_term)
            for term in result.keys():
                for appearance in result[term]:
                    line = db.get(appearance.docId)
                    print(highlight(appearance.docId, term, line['text']))
            print("\n")
            answer = input("enter quit to stop searching, y to continue:")
            print("\n")
    
main()
