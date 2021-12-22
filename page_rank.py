import sys
import os
import time
import argparse
from progress import Progress
import random


def load_graph(args):
    MyDictionary = {}

    # Opening the file
    with open('school_web.txt', 'r') as args.datafile:
        # Iterate through the file line by line
        for line in args.datafile:

            # And split each line into two URLs
            node, target = line.split()

            # Chech if the node(=key) is already in MyDictionary
            if node in MyDictionary.keys():
                MyDictionary[node].append(target)

            # If it's not just add the key and the value normally
            else:
                MyDictionary[node] = []
                MyDictionary[node].append(target)

        # Testing if the dictionary is correct
        # print(MyDictionary)
    return MyDictionary

def print_stats(graph):

    # To find the number of nodes is easy as we can look for the number of keys in the dictionary
    print("The number of nodes in the graph is:", len(graph.keys()))

    """
    To find the number of edges is harder as we can't just look directly
    for the number of values in the dictionary as most of the values for each
    key are in a list.
    """
    count = 0
    for key, value in graph.items():

        # Check if the value of the key is a list. If yes just add the length of it to the count
        if isinstance(value, list):
            count += len(value)
    print("The number of edges in the graph is:", count)


def stochastic_page_rank(graph, args):
    hit_count = []
    num_keys = len(graph.keys())

    # Populate the hit_count list with 0 for each node
    for i in range(num_keys):
        hit_count.append(0)

    # Make a list with all the nodes so we can get the position of each node easier
    node_list = []
    for i in graph.keys():
        node_list.append(i)

    # Test if the node list contains the correct values or all values
    # print(len(node_list))
    # print(node_list)

    for _ in range(args.repeats):
        random_node = random.randint(0, num_keys)
        current_node = node_list[random_node -1]

        for _ in range(args.steps):

            # Get the edges of the node from the graph dictionary
            list_of_values = graph[current_node]
            random_edge = random.randint(0, len(list_of_values))

            # Update the current_node
            current_node = list_of_values[random_edge -1]

        # Update the hit_count list
        index_node = node_list.index(current_node)
        hit_count[index_node] += 1/args.repeats

    # Creating the dictionary that contains the link and hit count
    hit_frequency = {}

    # Using 2 for loops in order to add the keys and values correctly to the dictionary
    for key in node_list:

        # This for loop only loops once for each iteration of the first loop as it has a break
        for value in hit_count:
            hit_frequency[key] = value

            # Due to the break we will just remove the first hit_count
            # from the list to use the good one for the next iteration
            hit_count.remove(value)
            break

    # The better way of writing the dictionary: hit_frequency = {node_list[i]: hit_count[i] for i in range(len(node_list))}
    return hit_frequency


def distribution_page_rank(graph, args):
    node_prob = []
    num_nodes = len(graph.keys())
    uniform_prob = 1/ num_nodes
    for _ in range(num_nodes):
        node_prob.append(uniform_prob)

    # Make a list with all the nodes so we can get the position of each node easier
    node_list = []
    for i in graph.keys():
        node_list.append(i)

    for _ in range(args.steps):

        # Initialize next_prob[node] = 0 for all nodes
        next_prob = []
        for _ in range(num_nodes):
            next_prob.append(0)

        for node in range(num_nodes):

            # Use a current_node to better find the edges of each node
            current_node = node_list[node]
            edges = graph[current_node]
            out_degree = len(edges)
            p = node_prob[node]/ out_degree

            for target in range(out_degree):
                # Look for the index of each edge in the node_list to accurately assign each prob
                index_node = node_list.index(edges[target])
                next_prob[index_node] += p

        # Update the node_prob with the new prob from next_prob
        for indx in range(num_nodes):

            # Checks only for the prob that have changed in the next_prob
            if next_prob[indx] != 0:
                node_prob[indx] = next_prob[indx]

    # Creating the dictionary that contains the link and probability
    page_prob = {}
    for key in node_list:
        for value in node_prob:
            page_prob[key] = value
            node_prob.remove(value)
            break
    return page_prob


parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="selected page rank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=100_000, help="number of repetitions")
parser.add_argument('-s', '--steps', type=int, default=100, help="number of steps a walker takes")
parser.add_argument('-n', '--number', type=int, default=20, help="number of results shown")


if __name__ == '__main__':
    args = parser.parse_args()
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank

    graph = load_graph(args)

    print_stats(graph)

    start = time.time()
    ranking = algorithm(graph, args)
    stop = time.time()
    time = stop - start

    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:args.number]))
    sys.stderr.write(f"Calculation took {time:.2f} seconds.\n")
