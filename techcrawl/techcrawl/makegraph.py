import csv
import re
import string
import sys
import os
import networkx as nx
from networkx.algorithms import approximation as apxa
import matplotlib.pyplot as plt

# function to grab data from csv file and append to list
def get_data():
    
    rows = []
    
    files = [f for f in os.listdir(os.curdir) if os.path.isfile(f)]
    files = [f for f in files if f.endswith('.csv')]
    print('\n')
    print('These are the csv files in current directory: ')
    [print(f) for f in files]
    print('\n')

    data = ''
    while(data != 'n'):
        data = input("please enter csv file name including .csv: ")
        if data in files:
            with open(data, "r") as f:
                readCSV = csv.reader(f, delimiter=',')
                for row in readCSV:
                    rows.append(row)

            data = 'n'
        else:
            print('\n')
            print("no such file exists.")


    rows = rows[:-1]

    return rows

# function to take list generated from csv file and create graph
def make_graph(rows):
    
    G = nx.DiGraph(name='link_graph')

    rows = [str(row) for row in rows]

    for item in rows:
        item = re.sub('https://', '', item)
        item = re.sub('http://', '', item)
        item = re.sub('www.', '', item)
        item = re.sub('\[', '', item)
        item = re.sub('\]', '', item)
        item = re.sub('\"', '', item)
        item = re.sub(' ', '', item)
        item = item.split(',')
        v = item[0]
        e = item[1]
        G.add_edge(v, e)
    

    return G

# function to return list of highest node degrees
def node_degree(G):
    
    number = input("number of nodes to display: ")
    degree = nx.degree(G)
    top_degree = sorted( ((v,k) for k,v in degree), reverse=True)
    print("highest node degrees")
    for i in range(int(number)):
        print("{}: {}" .format(i+1,top_degree[i]))

# function to return list of highest in_centralities
def in_centrality(G):

    number = input("number of top in centrality to display: ")
    inDegree = nx.in_degree_centrality(G)
    top_in = sorted( ((v,k) for k,v in inDegree.items()), reverse=True)
    print("top nodes by in_degree centrality")
    for i in range(int(number)):
        print("{}: {}" .format(i+1,top_in[i]))

# function to return list of highest out_centralities
def out_centrality(G):

    number = input("number of top out centrality to display: ")
    outDegree = nx.out_degree_centrality(G)
    top_out = sorted( ((v,k) for k,v in outDegree.items()), reverse=True)
    print("top nodes by out_degree centrality")
    for i in range(int(number)):
        print("{}: {}" .format(i+1, top_out[i]))

# function to return list of highest closeness centralities
def closeness_centrality(G):

    number = input("number of closeness centralities to display: ")
    closeDegree = nx.closeness_centrality(G)
    top_close = sorted( ((v,k) for k,v in closeDegree.items()), reverse=True)
    print("top nodes by closeness centrality")
    for i in range(int(number)):
        print("{}: {}" .format(i+1, top_close[i]))

# function to look at specific node(web page) and see connections(links) and visualize
def neighbors(G):
    
    data = ''
    while data != 'n':
        
        node = input("enter page name to see neighbors(links): ")
        node = '\''+node+'\''
        
        if node not in G.nodes:
            print('webpage not in graph, please re-enter.')
            print('\n')
        
        else:
            data = 'n'
    
    N = nx.Graph()
    print('\n')
    print("{} neighbors are: " .format(node))
    print('\n')
    x = 0
    
    for item in nx.neighbors(G,node):
        print('{}. {}' .format(x+1,item))
        N.add_edge(node,item)
        x += 1
    print('\n')
    
    choice = input('Would you like to see graph of neighbors(y or n): ')
    if choice is 'y':
        nx.draw(N, with_labels=True)
        plt.show()

# function to generate page rank score of each node(web page) and display/search results
def page_rank(G):
    
    page_rank = nx.pagerank_numpy(G, alpha=0.9)
    data = ''
    while data != 'n':
        
        data = input("Enter top for highest pageranks or search to find single page(quit to return to menu): ")
        print('\n')

        if data == 'top':
            number = input("number of top pagerank scores to display: ")
            top_rank = sorted( ((v,k) for k,v in page_rank.items()), reverse = True)
            print('\n')
            print("top nodes by pagerank")
            print('\n')
            for i in range(int(number)):
                print("{}: {}" .format(i+1, top_rank[i]))
            print('\n')

        elif data == 'search':
            page = input('Enter web page to find: ')
            page = '\''+page+'\''
            print('\n')
            print('{} page rank is {}' .format(page, page_rank.get(page)))
            print('\n')

        elif data == 'quit':
            data = 'n'

        else:
            print('come again, say what?.')
            print('\n')

# function to generate the hubs and authorities score for node(web page) and display/search results
def hits(G):
    
    h,a = nx.hits_numpy(G, normalized = True)
    top_hubs = sorted( ((v,k) for k,v in h.items()), reverse = True)
    top_auth = sorted( ((v,k) for k,v in a.items()), reverse = True)
    data = ''
    while data != 'n':
        
        data = input("Enter hubs for top hubs or authorities for top authorities or search for single page(quit to return to menu): ")
        print('\n')

        if data == 'hubs':
            number = input("number of top hubs to display: ")
            print('\n')
            print("top nodes by hub")
            print('\n')
            for i in range(int(number)):
                print("{}: {}" .format(i+1, top_hubs[i]))
            print("\n")
        
        elif data == 'authorities':
            number = input("number of top authorities to display: ")
            print('\n')
            print("top nodes by hub")
            print('\n')
            for i in range(int(number)):
                print("{}: {}" .format(i+1, top_auth[i]))
            print("\n")
        
        elif data == 'search':
            choice = ''
            while choice != 'n':
                
                choice = input('Enter h for hub or a for authority: ')
                print('\n')

                if choice == 'h':
                    page = input('Enter web page to find: ')
                    print('\n')
                    page = '\''+page+'\''
                    print('{} hub score is {}' .format(page, h.get(page)))
                    print('\n')

                elif choice == 'a':
                    page = input('Enter web page to find: ')
                    print('\n')
                    page = '\''+page+'\''
                    print('{} authority score is {}' .format(page, a.get(page)))
                    print('\n')

                elif choice == 'quit':
                    choice = 'n'

                else:
                    print('come again, say what?')
            
        elif data == 'quit':
            data = 'n'
        
        else:
            print('come again, say what?')
            print('\n')

# function to display program choices
def options():

    options = ['info', 'clear screen', 'density', 'node degree', 'neighbors', 'in centrality', 'out centrality', 'closeness centrality', 'avg cluster',
               'pagerank(google original ranking algorithm)', 'hits(hubs and authorities ranking algorithm)', 'draw']
    
    print("the options are: ")
    print('\n')
    for item in options:
        print(item)


def main(): 

    rows = get_data()
    G = make_graph(rows)
    print('-----------------------------------------------------------------------------')
 
    answer = ''
    print("\n")
    
    while(answer != 'quit'):
        answer = input("please enter a metric you would like to see (enter quit to terminate, enter help for options): ")
        print("\n")               
        
        if answer == "help":
            options()
            print("\n")
            print('-----------------------------------------------------------------------------')
        
        elif answer == "info":
            print(nx.info(G))
            print("\n")
            print('-----------------------------------------------------------------------------')
        
        elif answer == "clear screen":
            sys.stderr.write("\x1b[2J\x1b[H")
            print("\n")
            print('-----------------------------------------------------------------------------')
        
        elif answer == "density":
            print("graph density")
            print(nx.density(G))
            print("\n")
            print('-----------------------------------------------------------------------------')
        
        elif answer == "node degree":
            node_degree(G)
            print("\n")
            print('-----------------------------------------------------------------------------')
        
        elif answer == 'neighbors':
            neighbors(G)
            print('\n')
            print('-----------------------------------------------------------------------------')
        
        elif answer == "in centrality": 
            in_centrality(G)
            print("\n")
            print('-----------------------------------------------------------------------------')
        
        elif answer == "out centrality":
            out_centrality(G)
            print("\n")
            print('-----------------------------------------------------------------------------')
        
        elif answer == "draw":
            nx.draw(G, with_labels=False)
            plt.show()
            print('\n')
            print('-----------------------------------------------------------------------------')
        
        elif answer == "pagerank":
            page_rank(G)
            print("\n")
            print('-----------------------------------------------------------------------------')
        
        elif answer == "hits":
            hits(G)
            print('\n')
            print('-----------------------------------------------------------------------------')
       
        elif answer == "avg cluster":
            print("the average clustering coefficient")
            print(nx.average_clustering(G))
            print("\n")
            print('-----------------------------------------------------------------------------')
        
        elif answer == "closeness centrality":
            closeness_centrality(G)
            print("\n")
            print('-----------------------------------------------------------------------------')
        
        elif answer == "quit":
            break;
        
        else:
            print("come again, say what?")
            print("\n")
            print('-----------------------------------------------------------------------------')


main()


