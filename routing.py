import csv
import sys
import argparse

my_list = []
vertices = []

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional arguments
parser.add_argument("csv_file", help="CSV File to Read")
 
# Read arguments from command line
args = parser.parse_args()

csv_file = args.csv_file

with open(csv_file, newline='') as file:
    reader = csv.reader(file, delimiter=' ', quotechar='|')
    #next(reader, None)  # skip the 1st row (header)
    for row in reader:
        my_list.append(row[0].split(','))

temp = my_list[0]
vertices = temp

"""
[
 ['', 'u', 'v', 'w', 'x', 'y', 'z'], 
 ['u', '0', '7', '3', '5', '9999', '9999'], 
 ['v', '7', '0', '3', '9999', '4', '9999'], 
 ['w', '3', '3', '0', '4', '8', '9999'], 
 ['x', '5', '9999', '4', '0', '7', '9'], 
 ['y', '9999', '4', '8', '7', '0', '2'], 
 ['z', '9999', '9999', '9999', '9', '2', '0']
]
"""

def dijkstra_algorithm():

    dictionary = {}

    for i in range(1, len(my_list)):  # for each row -- skip the first row ['', 'u', 'v', 'w', 'x', 'y', 'z']
        array = []
        for j in range(1, len(my_list[i])):  # for each column in a row -- skip the first column of each row (contain letter)
            my_list[i][j] = int(my_list[i][j])    # turn all the string number to int
            
            if my_list[i][j] != 0 and my_list[i][j] != 9999:
                array.append([my_list[0][j], my_list[i][j]])      # array.append([adjacent_node, cost]) -- an array of lists
                
        dictionary[my_list[i][0]] = array    # dictionary.append(startNode : array of [adjacent_node, cost])
        
    """
    {
     'u': [['v', 7], ['w', 3], ['x', 5]], 
     'v': [['u', 7], ['w', 3], ['y', 4]],
     'w': [['u', 3], ['v', 3], ['x', 4], ['y', 8]],
     'x': [['u', 5], ['w', 4], ['y', 7], ['z', 9]],
     'y': [['v', 4], ['w', 8], ['x', 7], ['z', 2]],
     'z': [['x', 9], ['y', 2]]
    }
    """

    # find the closet adjacent node with a smallest cost from a given node
    def smallest_link(node):
        links = dictionary[node]    # access the array of [adjacent_node, cost] of that given node  
        closet_node = None       # default setting
        smallest_cost = 9999     # default setting
        for link in links:
            if link[1] < smallest_cost:     # if the cost from the node to this adjacent_node < smallest_cost
                closet_node = link[0]
                smallest_cost = link[1]         
        return closet_node, smallest_cost
        
    # delete the visited node from the dictionary by delete its links at other nodes
    # for example: u is visited (updated costs from u-v, u-w, u-x), 
    # then we want to delete links from v-u, w-u, x-u because they are repeated.
    def update_visited_node(node):
        for startNode in dictionary:     # for each startNode in dictionary (u,v,w,y,z)
            links_array = dictionary[startNode]
            for link in links_array:
                if link[0] == node:     # if that startNode connects with the visited node, delete that link
                    links_array.remove(link)
                    dictionary[startNode] = links_array
                    break   # go to next startNode
                
    #---------------------MAIN------------------------

    source_node = input("Please, provide the source node: ")

    shortest_paths = []
    visited_nodes = []

    visited_nodes.append([source_node,0])    # visited_nodes = [[u,0]]
    update_visited_node(source_node)         # delete links from other nodes to u in dictionary

    node,cost = smallest_link(source_node)      # find the next closest node from u (w,3)

    shortest_paths.append( str(source_node)+str(node) )     # shortest_paths = ['uw']
    visited_nodes.append([node,cost])       # visited_nodes = [[u,0], [w,3]]
    update_visited_node(node)               # delete links from other nodes to w in dictionary

    """
    {
     'u': [['v', 7], ['x', 5]],
     'v': [['y', 4]],
     'w': [['v', 3], ['x', 4], ['y', 8]],
     'x': [['y', 7], ['z', 9]],
     'y': [['v', 4], ['x', 7], ['z', 2]],
     'z': [['x', 9], ['y', 2]]
    }
    """

    #-------------------END MAIN----------------------

    def find_next_node(visited_nodes):
        new_costs = []
        
        for item in visited_nodes:  # visited_nodes = [[u,0], [w,3]]
            cur_node = item[0]
            cur_cost = item[1]
            node, cost = smallest_link(cur_node)
            new_costs.append([cur_node, node, cur_cost+cost])    # new_costs = [[u,x,5], [w,v,6]]
        
        min_link = new_costs[0]         # min_link = [u,x,5] -- default setting
        min_cost = new_costs[0][2]      # min_cost = 5 -- default setting

        for item in new_costs:
            temp_cost = item[2]
            if temp_cost < min_cost:
                min_link = item             # min_link = [u,x,5]
                min_cost = temp_cost        # min_cost = 5
        
        
        existing_path = False
        for path in shortest_paths:         # shortest_paths = ['uw']
            if path[-1] == min_link[0]:     
                shortest_paths.append( path+str(min_link[1]) )
                existing_path = True
                
        if not existing_path:
            shortest_paths.append( str(min_link[0])+str(min_link[1]) )
        
        next_node = [min_link[1],min_link[2]]   # next_node = [x,5]
        return next_node
        
    #---------------------MAIN------------------------

    while len(visited_nodes) < len(dictionary):
        next_node = find_next_node(visited_nodes)
        visited_nodes.append(next_node)
        update_visited_node(next_node[0])
        
    # prints the output
    print(f"\nShortest path tree for node {source_node}:")
    for i in range(len(shortest_paths)):
        print(shortest_paths[i], end=', ')
        
    print(f"\nCosts of the least-cost paths for node {source_node}:")
    for i in range(len(visited_nodes)):
        print(f"{visited_nodes[i][0]}:{visited_nodes[i][1]}", end=', ')   
         
    print()
            
def distance_vector(source, adj_matrix):
    N = len(adj_matrix)
    dist = [sys.maxsize] * N

    # Set variables to use the index of the adjacency matrix
    # Rather than the value to avoid math errors
    ix = 0
    count=0

    for row in adj_matrix:     
        if row[0] == source:
            ix = count
        else:
            count+=1
    dist[ix] = 0

    # Check the distance vectors
    # If positive, list out
    # If negtive print a statement
    for k in range(N-1):
        for i in range(1,N):
            for j in range(1,N): 
                if dist[i] != sys.maxsize and adj_matrix[i][j] and dist[j]> (dist[i] + int(adj_matrix[i][j])):
                    dist[j] = dist[i]+int(adj_matrix[i][j])     

    for k in range(N-1):
        for i in range(1,N):
            for j in range (1,N):
                if(adj_matrix[i][j] and dist[j] > (dist[i] + int(adj_matrix[i][j]))): 
                    print("\n negative distance path")
                    
   # For the length of the adjacency matrix
   # Print the distances for each node
    for i in range(1,N):
            print(" {}".format(dist[i]), end='')
       
def main():
    dijkstra_algorithm()
    
    # Run Bellman Ford algorithm 
    # Skipping over the first row to only use the number values
    for row in my_list[1:]:
        print(f"\nDistance vector for node {row[0]}:", end='')
        distance_vector(row[0], my_list)

main()