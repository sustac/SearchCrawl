import csv
import re
import string
import sys
import networkx as nx
from networkx.algorithms import approximation as apxa
import matplotlib.pyplot as plt


def main():
     
    rows = []
    format_list = []

############################################### get data from csv file, append to list

    page = input("please enter csv file name including .csv: ")
    
    with open(page, "r") as f:
        readCSV = csv.reader(f, delimiter=',')
        
        for row in readCSV:
            rows.append(row)
    
    rows = rows[:-1]


################################################# convert to string for python operators to work, filter, then create graph(nodes,edges)    
    
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
        

############################################  user input for graph metric choices
 
    answer = ''
    print("\n")
    
    while(answer != 'quit'):
        answer = input("please enter a metric you would like to see (enter quit to terminate, enter help for options): ")
        print("\n")               
        
        if answer == "help":
            print("the options are: info, clear screen, density, node degree, in centrality, out centrality, closeness centrality, avg cluster, draw, pagerank") 
            print("\n")
        
        elif answer == "info":
            print(nx.info(G))
            print("\n")
        
        elif answer == "clear screen":
            sys.stderr.write("\x1b[2J\x1b[H")
            print("\n")
        
        elif answer == "density":
            print("graph density")
            density = nx.density(G)
            print(density)
            print("\n")
        
        elif answer == "node degree":
            number = input("number of nodes to display: ")
            degree = nx.degree(G)
            top_degree = sorted( ((v,k) for k,v in degree), reverse=True)
            print("highest node degrees")
            for i in range(int(number)):
                print("{}: {}" .format(i+1,top_degree[i]))
            print("\n")
        
        elif answer == "in centrality": 
            number = input("number of top in centrality to display: ")
            inDegree = nx.in_degree_centrality(G)
            top_in = sorted( ((v,k) for k,v in inDegree.items()), reverse=True)
            print("top nodes by in_degree centrality")
            for i in range(int(number)):
                print("{}: {}" .format(i+1,top_in[i]))
            print("\n")
        
        elif answer == "out centrality":
            number = input("number of top out centrality to display: ")
            outDegree = nx.out_degree_centrality(G)
            top_out = sorted( ((v,k) for k,v in outDegree.items()), reverse=True)
            print("top nodes by out_degree centrality")
            for i in range(int(number)):
                print("{}: {}" .format(i+1, top_out[i]))
            print("\n")
        
        elif answer == "draw":
            nx.draw(G, with_labels=False)
            plt.show()
        
        elif answer == "pagerank":
            page_rank = nx.pagerank_numpy(G, alpha=0.9)
            maximum = max(page_rank, key=page_rank.get)
            print("max in page_rank ")
            print(maximum, page_rank[maximum])
            print("\n")
        
        elif answer == "avg cluster":
            print("the average clustering coefficient")
            print(nx.average_clustering(G))
            print("\n")
        
        elif answer == "closeness centrality":
            number = input("number of closeness centralities to display: ")
            closeDegree = nx.closeness_centrality(G)
            top_close = sorted( ((v,k) for k,v in closeDegree.items()), reverse=True)
            print("top nodes by closeness centrality")
            for i in range(int(number)):
                print("{}: {}" .format(i+1, top_close[i]))
            print("\n")

        elif answer == "quit":
            break;
        
        else:
            print("come again, say what?")
            print("\n")


main()


