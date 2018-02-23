from cfg.prog import prog
from cfg.pgcd import pgcd
from parcours_graph import parcours_graph, initialization

def extract_labels(G):
    """ Returns a list of graph's nodes which contains the command 'if' or 'while' """
    labels_if_while = {}
    labels = G.nodes
    for node in labels :
        if G.node[node]['cmd'] in ['if','while']:
            labels_if_while[node] = [child for child in G[node]]
    return labels_if_while

def td(G, var, res):
    """ Returns a list of the visited nodes which contains the command 'while' or 'if' from the graph G crossed by variables initialized in 'var' """
    # Initialization
    cmd, curr_node = initialization(G, var)
    # Crossing the graph
    while cmd != "end":
        if cmd in ['if', 'while'] :
            for edge in G.edges(curr_node, data=True):
                if (edge[2]['bool'](var)) & (curr_node not in res):
                    res[curr_node] = [edge[1]]
                elif (edge[2]['bool'](var)) & (curr_node in res):
                    if edge[1] not in res[curr_node] :
                        res[curr_node].append(edge[1])
        cmd, curr_node = parcours_graph(G, cmd, curr_node, var)
    # End
    G.nodes[curr_node]['msg'](var)
    return res

def td_test(G, tests):
    """ Takes a set of tests and a graph G and returns True if the test TD is passed """
    res = {}
    l = extract_labels(G)
    for var in tests :
        res = td(G, var, res)
    for value in res.values():
        value.sort()
    print("////////////////////////////////////////\n" \
           "/// TESTS PASS THE CRITERIA  : {} ///\n" \
           "///////////////////////////////////////\n".format(res == l))
    return res == l

print("----\nPROG\n----")
tests = [{'x':5},{'x':-3},{'x':50}, {'x' : -1}]
td_test(prog.graph, tests)

print("----\nPGCD\n----")
tests_pgcd = [{'x':400, 'y' : 280},{'x':-15, 'y': 6},{'x':50, 'y' : 3}, {'x' : -10, 'y' : 4}]
td_test(pgcd.graph, tests_pgcd)
