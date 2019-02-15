import csv
import re
import string
import sys
import os
import networkx as nx
from networkx.algorithms import approximation as apxa
import matplotlib.pyplot as plt

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
        item = item.split(',')
        v = item[0]
        e = item[1]
        G.add_edge(v, e)
    

    return G


def main(): 

    rows = get_data()
    print('-----------------------------------------------------------------------------')
    G = make_graph(rows)

 
    answer = ''
    print("\n")
    
    while(answer != 'quit'):
        answer = input("please enter a metric you would like to see (enter quit to terminate, enter help for options): ")
        print("\n")               
        
        if answer == "help":
            print("the options are: info, clear screen, density, node degree, in centrality, out centrality, closeness centrality, avg cluster, draw, pagerank") 
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
            density = nx.density(G)
            print(density)
            print("\n")
            print('-----------------------------------------------------------------------------')
        
        elif answer == "node degree":
            number = input("number of nodes to display: ")
            degree = nx.degree(G)
            top_degree = sorted( ((v,k) for k,v in degree), reverse=True)
            print("highest node degrees")
            for i in range(int(number)):
                print("{}: {}" .format(i+1,top_degree[i]))
            print("\n")
            print('-----------------------------------------------------------------------------')
        
        elif answer == "in centrality": 
            number = input("number of top in centrality to display: ")
            inDegree = nx.in_degree_centrality(G)
            top_in = sorted( ((v,k) for k,v in inDegree.items()), reverse=True)
            print("top nodes by in_degree centrality")
            for i in range(int(number)):
                print("{}: {}" .format(i+1,top_in[i]))
            print("\n")
            print('-----------------------------------------------------------------------------')
        
        elif answer == "out centrality":
            number = input("number of top out centrality to display: ")
            outDegree = nx.out_degree_centrality(G)
            top_out = sorted( ((v,k) for k,v in outDegree.items()), reverse=True)
            print("top nodes by out_degree centrality")
            for i in range(int(number)):
                print("{}: {}" .format(i+1, top_out[i]))
            print("\n")
            print('-----------------------------------------------------------------------------')
        
        elif answer == "draw":
            nx.draw(G, with_labels=False)
            plt.show()
            print('\n')
            print('-----------------------------------------------------------------------------')
        
        elif answer == "pagerank":
            page_rank = nx.pagerank_numpy(G, alpha=0.9)
            number = input("number of top pagerank scores to display: ")
            top_rank = sorted( ((v,k) for k,v in page_rank.items()), reverse = True)
            print("top nodes by pagerank")
            for i in range(int(number)):
                print("{}: {}" .format(i+1, top_rank[i]))
            print("\n")
            print('-----------------------------------------------------------------------------')
        
        elif answer == "avg cluster":
            print("the average clustering coefficient")
            print(nx.average_clustering(G))
            print("\n")
            print('-----------------------------------------------------------------------------')
        
        elif answer == "closeness centrality":
            number = input("number of closeness centralities to display: ")
            closeDegree = nx.closeness_centrality(G)
            top_close = sorted( ((v,k) for k,v in closeDegree.items()), reverse=True)
            print("top nodes by closeness centrality")
            for i in range(int(number)):
                print("{}: {}" .format(i+1, top_close[i]))
            print("\n")
            print('-----------------------------------------------------------------------------')

        elif answer == "quit":
            break;
        
        else:
            print("come again, say what?")
            print("\n")
            print('-----------------------------------------------------------------------------')


main()


