import sys
import os
import time
import argparse
from progress import Progress
import random


def load_graph(args):
    """Load graph from text file

    Parameters:
    args -- arguments named tuple

    Returns:
    A dict mapling a URL (str) to a list of target URLs (str).
    """
    MyDictionary = {}
    with open('school_web.txt', 'r') as args.datafile: #Opening the file
    # Iterate through the file line by line
        for line in args.datafile:
            # And split each line into two URLs
            node, target = line.split()

            #Chech if the node(=key) is already in MyDictionary
            if node in MyDictionary.keys():
                MyDictionary[node].append(target)

            #If it's not just add the key and the value normally
            else:
                MyDictionary[node] = []
                MyDictionary[node].append(target)

        # Testing if the dictionary is correct
        # print(MyDictionary)
    return MyDictionary

def print_stats(graph):
    """Print number of nodes and edges in the given graph"""

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
    """Stochastic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its hit frequency

    This function estimates the Page Rank by counting how frequently
    a random walk that starts on a random node will after n_steps end
    on each node of the given graph.
    """
    hit_count = []
    num_keys = len(graph.keys())

    for i in range(num_keys):
        hit_count.append(0)

    #Make a list with all the nodes so we can get the position of each node easier
    node_list = []
    for i in graph.keys():
        node_list.append(i)

    for i in range(args.repeats):
        random_node = random.randint(0, num_keys)
        current_node = node_list[random_node-1]

        #for i in range(args.steps):

            #currrent_node =


def distribution_page_rank(graph, args):
    """Probabilistic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its probability to be reached

    This function estimates the Page Rank by iteratively calculating
    the probability that a random walker is currently on any node.
    """
    raise RuntimeError("4. This function is not implemented yet.")


parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="selected page rank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="number of repetitions")
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
