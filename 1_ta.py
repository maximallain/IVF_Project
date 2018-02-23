from cfg.prog import prog
from cfg.pgcd import *
from parcours_graph import parcours_graph, initialization

def extract_labels(G):
    """ Returns a list of graph's nodes which contains the command 'assign' """
    labels = G.nodes
    l = []
    for node in labels:
        if G.node[node]['cmd'] == 'assign':
            l.append(node)
    return l

def ta(G, var):
    """ Returns a list of the visited nodes which contains the command 'assign' from the graph G crossed by variables initialized in 'var' """

    # Initialization
    assign_list = []
    cmd, curr_node = initialization(G, var)

    # Crossing the graph
    while cmd != "end":
        if cmd == 'assign':
            assign_list.append(curr_node)
        cmd, curr_node = parcours_graph(G, cmd, curr_node, var)

    # End
    G.nodes[curr_node]['msg'](var)
    return assign_list


def ta_test(G, tests):
    """ Takes a set of tests and a graph G and returns True if the test TA is passed """

    mergedlist = []
    labels = extract_labels(G)

    for test in tests:
        assign_list = ta(G, test)
        mergedlist = list(set(mergedlist + assign_list))

    print("////////////////////////////////////////\n" \
           "/// TESTS PASS THE CRITERIA  : {} ///\n" \
           "///////////////////////////////////////\n".format(mergedlist == labels))
    return mergedlist == labels


print("----\nPROG\n----")
tests = [{'x': 5}, {'x': -3}, {'x': 50}, {'x': -1}]
ta_test(prog.graph, tests)

print("----\nPGCD\n----")
tests_pgcd = [{'x': 400, 'y': 280}, {'x': -15, 'y': 6}, {'x': 50, 'y': 3}, {'x': -10, 'y': 4}]
ta_test(pgcd.graph, tests_pgcd)
