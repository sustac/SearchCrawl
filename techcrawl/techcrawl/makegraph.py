import json
import re
import string
import sys
import networkx as nx
from networkx.algorithms import approximation as apxa
import matplotlib.pyplot as plt


def main():
     
    key = []
    value = []
    mylist = []
    format_list = []

############################################### get data from connections.json, append keys and values to seperate lists

    page = input("please enter json file name including .json: ")
    
    with open(page, "r") as f:
        data = json.load(f)
    
    for item in range(len(data)):
        value.append(data[item])

################################################# convert to string for python operators to work, make list of pages/links, filter    
    value = [str(i) for i in value]
    
    for item in value:
        item = item.split('\'url\':', 1)[1]
 #       a = item.split(',', 3)[1]
 #       b = item.split(',', 3)[2]
 #       item = a + '  ' + b
        mylist.append(item)

    
    for item in mylist:
        item = re.sub('https://', '', item)
        item = re.sub('http://', '', item)
        item = re.sub('\'link\':', '', item)
        item = re.sub('}', '', item)
     #   item = re.sub('\r', '', item)
     #   item = re.sub('\\', '', item)
        item = re.sub('\[', '', item)
        item = re.sub('\]', ', ', item)
        item = re.sub('u\'', '', item)
        item = re.sub('www.', '', item)
     #   item = re.sub('.edu', '', item)
    #    item = re.sub('.org', '', item)
   #     item = re.sub('.net', '', item)
   #     print(item)
        format_list.append(item)

    
#########################################loop thru format_list and create nodes edges
    
    G = nx.DiGraph(name='link_graph')
    for item in format_list:
#        print(item)
        item = item.split(', ', 1)
#        print(item)
        v = item[0]
#           print(v)
        e = item[1]
#           print(e)
            
        G.add_edge(v, e)

############################################  user input for graph metric choices
 
    answer = ''
    print("\n")
    while(answer != 'quit'):
        answer = input("please enter a metric you would like to see (enter quit to terminate, enter help for options): ")
        print("\n")               
        
        if answer == "help":
            print("the options are: info, clear screen, density, node degree, in cardinality, out cardinality, avg cluster, draw, pagerank") 
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
        elif answer == "in cardinality": 
            number = input("number of top in cardinalities to display: ")
            inDegree = nx.in_degree_centrality(G)
            top_in = sorted( ((v,k) for k,v in inDegree.items()), reverse=True)
            print("top nodes by in_degree centrality")
            for i in range(int(number)):
                print("{}: {}" .format(i+1,top_in[i]))
            print("\n")
        elif answer == "out cardinality":
            number = input("number of top out cardinalities to display: ")
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
            number = input("number of top pageranks to display: ")
            page_rank = nx.pagerank_numpy(G, alpha=0.85)
            top_rank = sorted( ((v,k) for k,v in page_rank.items()), reverse=True)
            print("top nodes by page_rank")
            for i in range(int(number)):
                print("{}: {}" .format(i+1, top_rank[i]))
            print("\n")

        elif answer == "avg cluster":
            print("the average clustering coefficient")
            print(nx.average_clustering(G))
            print("\n")
        
        elif answer == "quit":
            break;
        else:
            print("come again, say what?")
            print("\n")

#    clique = apxa.max_clique(G)
#    print("\n")
#    print(clique)

main()


