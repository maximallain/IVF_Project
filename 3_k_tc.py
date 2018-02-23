from cfg.pgcd import *
from cfg.prog import *
from parcours_graph import parcours_graph, initialization


def k_path_list(G, node, k):
    """ Returns the list of all possible k_path from the origin node """
    if k == 0:
        return [node]
    else:
        list = []
        for child in G[node]:
            for path in k_path_list(G, child, k - 1):
                if type(path) == int:
                    list_temp = [node] + [path]
                else:
                    list_temp = [node] + path
                list.append(list_temp)
    return list

def k_tc(G, var, node, k):
    """ Crosses the graph with an initial variables' set and returns a k_path from the origin node"""
    # Initialization
    cmd, curr_node = initialization(G, var)

    # Crossing the graph until we reach the node
    while (cmd != "end") & (curr_node != node) :
        cmd, curr_node = parcours_graph(G, cmd, curr_node, var)

    # Creation of the path list
    path = [curr_node]

    # Crossing the graph and adding the current node to the path
    while (cmd != "end") & (len(path) != k+1):
        cmd, curr_node = parcours_graph(G, cmd, curr_node, var)
        path.append(curr_node)

    # End
    while (cmd != "end"):
        cmd, curr_node = parcours_graph(G, cmd, curr_node, var)
    G.nodes[curr_node]['msg'](var)
    return path

def k_tc_test(G, tests, node, k):
    """ Takes a set of tests, a graph G and returns True if the test k-TC is passed """
    k_path = k_path_list(G, node, k)
    if k_path == [] :
        print("There is no path with a size of %i " % k)
        return True
    for test in tests :
        current_path = k_tc(G, test, node, k)
        print("path : {}\n".format(current_path))
        if current_path in k_path :
            k_path.remove(current_path)
            print("New k_path : {}".format(k_path))
    print("////////////////////////////////////////\n" \
           "/// TESTS PASS THE CRITERIA  : {} ///\n" \
           "///////////////////////////////////////\n".format(k_path == []))
    return k_path == []

print("----\nPROG\n----")
tests = [{'x':5},{'x':-3},{'x':50}, {'x' : -1}]
print(k_path_list(prog.graph, 0, 3))
k_tc_test(prog.graph, tests, 0, 3)

print("----\nPGCD\n----")
tests_pgcd = [{'x':6880, 'y' : 4000},{'x':-21, 'y': 15},{'x':50, 'y' : 3}, {'x' : -10, 'y' : 4}]
print(k_path_list(pgcd.graph, 1, 3))
k_tc_test(pgcd.graph, tests_pgcd, 1, 3)
