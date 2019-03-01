import csv
import re
import string
import sys
import os
import networkx as nx
from networkx.algorithms import approximation as apxa
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore") # only here to drop ComplexWarning from hits algorithm

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


# function to return immediate dominators/dominance frontier
def dominance(G):
    
    data = ''
    while data != 'done':
        start = input("please enter start node: ")
        start = '\''+start+'\''
        if start not in G.nodes:
            print("webpage not in graph, please re-try.")
            print('\n')
        else:
            data = 'done'
            
    imm_dominance = nx.immediate_dominators(G, start)
    front_dominance = nx.dominance_frontiers(G, start)
    
    print('\n')
    print("The number of immediate dominators is {} and the number of paths in dominance frontier is {}. " 
          .format(len(imm_dominance), len(front_dominance)))
    print('\n')
    
    data = ''
    while data != 'quit':
        data = input("enter list to list immediate doms or enter search to find specific node(quit to return to menu): ")
    
        if data == 'list':
            number = input("number of immediate dominators to display: ")
            print('\n')
            print("The immediate dominators from start node {}: " .format(start))
            print('\n')
            top_dom = sorted( ((v,k) for k,v in imm_dominance.items()), reverse=True)
            for i in range(int(number)):
                print("{}: {}" .format(i+1,top_dom[i]))
            print('\n')

        elif data == 'search':
            while data != 'done':
                page = input('Enter web page to find: ')
                page = '\''+page+'\''
                if page not in G.nodes:
                    print("webpage not in graph, please re-try.")
                    print('\n')
                else:
                    data = 'done'
            print('\n')
            print('the right column dominates the left')
            print('\n')
            for item in imm_dominance.items():
                if page in item:
                    print(item)
            print('\n')

        elif data == 'quit':
            data = 'quit'

        else:
            print('come again, say what?')
            print('\n')

    
    data = ''
    while data != 'quit':
        print('\n')
        data = input("Search for web page in the dominance frontier(y or n)?")
        print('\n')
        if data == 'y':
            while page != 'done':
                page = input("enter web page to see the paths it's included in(quit to return to menu): ")
                page = '\''+page+'\''
                if page not in G.nodes:
                    print("webpage not in graph, please re-try.")
                    print('\n')
                else:
                    print('\n')
                    print("The paths {} is included in." .format(page))
                    print('\n')
                    for item in front_dominance.items():
                        if page in item:
                            print(item)
                    page = 'done'
                    print('\n')
        
        elif data == 'n':
            data = 'quit'

        else:
            print('come again, say what?')
            print('\n')

# function to return list of highest in_centralities
def in_centrality(G):

    inDegree = nx.in_degree_centrality(G)
    
    data = ''
    while data !='quit':
        data = input("Enter top for highest in centralities or search to find single page(quit to return to menu): ")
        print('\n')

        if data == 'top':
            number = input("enter number of centralities to show: ")
            print('\n')
            top_in = sorted( ((v,k) for k,v in inDegree.items()), reverse=True)
            print("top nodes by in centrality")
            print('\n')
            for i in range(int(number)):
                print("{}: {}" .format(i+1, top_in[i]))
            print('\n')

        elif data == 'search':
            page = input('Enter web page to find: ')
            page = '\''+page+'\''
            print('\n')
            print('{} out centrality is {}' .format(page, inDegree.get(page)))
            print('\n')

        elif data == 'quit':
            data = 'quit'

        else:
            print("come again, say what?")
            print('\n')


# function to return list of highest out_centralities
def out_centrality(G):

    outDegree = nx.out_degree_centrality(G)
    
    data = ''
    while data !='quit':
        data = input("Enter top for highest out centralities or search to find single page(quit to return to menu): ")
        print('\n')

        if data == 'top':
            number = input("enter number of centralities to show: ")
            print('\n')
            top_out = sorted( ((v,k) for k,v in outDegree.items()), reverse=True)
            print("top nodes by out centrality")
            print('\n')
            for i in range(int(number)):
                print("{}: {}" .format(i+1, top_out[i]))
            print('\n')

        elif data == 'search':
            page = input('Enter web page to find: ')
            page = '\''+page+'\''
            print('\n')
            print('{} out centrality is {}' .format(page, outDegree.get(page)))
            print('\n')

        elif data == 'quit':
            data = 'quit'

        else:
            print("come again, say what?")
            print('\n')


# function to return list of highest closeness centralities
def closeness_centrality(G):

    closeDegree = nx.closeness_centrality(G)

    data = ''
    while data !='quit':
        data = input("Enter top for highest closeness centralities or search to find single page(quit to return to menu): ")
        print('\n')
        
        if data == 'top':
            number = input("enter number of centralities to show: ")
            print('\n')
            top_close = sorted( ((v,k) for k,v in closeDegree.items()), reverse=True)
            print("top nodes by closeness centrality")
            print('\n')
            for i in range(int(number)):
                print("{}: {}" .format(i+1, top_close[i]))
            print('\n')

        elif data == 'search':
            page = input('Enter web page to find: ')
            page = '\''+page+'\''
            print('\n')
            print('{} closeness centrality is {}' .format(page, closeDegree.get(page)))
            print('\n')

        elif data == 'quit':
            data = 'quit'

        else:
            print("come again, say what?")
            print('\n')


# function to look at specific node(web page) and see connections(links) and visualize
def neighbors(G):
    
    print('Neighbors are the outgoing links, will differ from node degree which is all links.')
    print('\n')
    
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
    
    print('If node has over 50 neighbors graph will overlap and become non sense.')
    choice = input('Would you like to see graph of neighbors(y or n): ')
    if choice is 'y':
        list_node = []
        list_node.append(node)
        pos = nx.spring_layout(N) #,scale = 6)
        nx.draw_networkx_nodes(N,pos, node_size=600)
        nx.draw_networkx_nodes(N,pos, nodelist = list_node, node_color='b', node_size=600)
        nx.draw_networkx_edges(N, pos, width=1)
        nx.draw_networkx_labels(N, pos)
        plt.axis('off')
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
                
                choice = input('Enter h for hub or a for authority(quit to return to menu): ')
                print('\n')

                if choice == 'h':
                    page = ''
                    while page != 'n':
                        page = input('Enter web page to find: ')
                        page = '\''+page+'\''
                        
                        if page not in G.nodes:
                            print('\n')
                            print('webpage not in graph, please re-try.')
                        
                        else:
                            print('\n')
                            print('{} hub score is {}' .format(page, h.get(page)))
                            print('\n')
                            page = 'n'

                elif choice == 'a':
                    page = ''
                    while page != 'n':
                        page = input('Enter web page to find: ')
                        page = '\''+page+'\''
                    
                        if page not in G.nodes:
                            print('\n')
                            print('webpage not in graph, please re-try.')
                    
                        else:
                            print('\n')    
                            print('{} authority score is {}' .format(page, a.get(page)))
                            print('\n')
                            page = 'n'

                elif choice == 'quit':
                    choice = 'n'

                else:
                    print('come again, say what?')
            
        elif data == 'quit':
            data = 'n'
        
        else:
            print('come again, say what?')
            print('\n')

# function to see if 2 nodes share a common neighbor
def share(G):
    
    data = ''
    while data != 'n':
        node1 = input('enter first node: ')
        node1 = '\''+node1+'\''
        
        if node1 in G.nodes:
            data = 'n'
        else:
            print('webpage not in graph, please re-try.')
            print('\n')
            
    while data != 'b':
        node2 = input('enter second node: ')
        node2 = '\''+node2+'\''
        
        if node2 in G.nodes:
            data = 'b'
        else:
            print('webpage not in graph, please re-try.')
            print('\n')

    list3 = []

    for item in nx.neighbors(G,node1):
        if item in nx.neighbors(G,node2):
            list3.append(item)

    if len(list3) == 0:
        print('\n')
        print("There are no common links.")

    if len(list3) != 0:
        print('\n')
        print('The common links are:')
        print('\n')
        for item in list3:
            print(item)
        print('\n')

        data = ''
        while data != 'd':
            data = input('would you like to see graph of shared links(y or n)? ')
            if data == 'y':
                N = nx.DiGraph()
                for item in list3:
                    N.add_edge(node1,item)
                    N.add_edge(node2,item)
                list_node = []
                list_node.append(node1)
                list_node.append(node2)
                pos = nx.shell_layout(N)
                nx.draw_networkx_nodes(N,pos, node_size=500)
                nx.draw_networkx_nodes(N,pos, nodelist = list_node, node_color='b', node_size=500)
                nx.draw_networkx_edges(N, pos, width=1)
                nx.draw_networkx_labels(N, pos)
                plt.axis('off')
                plt.show()
                data = 'd'
        
            elif data == 'n':
                data = 'd'
        
            else:
                print('choice is not y or n.')
                print('\n')


# function to display program choices
def options():

    options = ['info(disregard in/out average meant for undirected graphs)', 'clear screen', 'density', 'dominance(immediate,frontier)', 'node degree', 'neighbors', 
               'share(shared outgoing links)','in centrality', 'out centrality', 'closeness centrality', 'avg cluster',
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
        
        elif answer == "dominance":
            dominance(G)
            print('\n')
            print('-----------------------------------------------------------------------------')
            
        elif answer == "node degree":
            node_degree(G)
            print("\n")
            print('-----------------------------------------------------------------------------')
        
        elif answer == 'neighbors':
            neighbors(G)
            print('\n')
            print('-----------------------------------------------------------------------------')
        
        elif answer == 'share':
            share(G)
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


