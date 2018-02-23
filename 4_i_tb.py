from cfg.prog import prog
from cfg.pgcd import pgcd
from parcours_graph import parcours_graph, initialization


def extract_labels(G):
    """ Returns a list of graph's nodes which contains the command 'while' """
    labels_while = {}
    labels = G.nodes
    for node in labels :
        if G.node[node]['cmd'] == 'while':
            labels_while[node]=0
    return labels_while

def verify_criteria(labels_while,i):
    """ Returns False if the length of the list 'labels_while' is higher than i, True if not"""
    for r in labels_while:
        if labels_while[r]>i:
            return False
    return True

def itb(G, var, i):
    """ Returns True if the criteria i_tb is verified for the graph G crossed by var """

    # Initialization
    cmd, curr_node = initialization(G, var)
    labels_while = extract_labels(G)

    # Crossing the graph
    while cmd != "end":
        if cmd == "while":
            for edge in G.edges(curr_node, data=True):
                if edge[2]['bool'](var):
                    labels_while[curr_node]=labels_while[curr_node]+1
        cmd, curr_node = parcours_graph(G, cmd, curr_node, var)


    # End
    G.nodes[curr_node]['msg'](var)
    respect = verify_criteria(labels_while, i)
    return respect

def itb_test(G, tests, i):
    """ Takes a set of tests, a graph G and returns True if the test i-TB is passed """
    for test in tests :
        if not(itb(G, test, i)) :
            print("////////////////////////////////////////\n"
                  "/// TESTS PASS THE CRITERIA  : False ///\n"
                  "///////////////////////////////////////\n")
            return False
    print("////////////////////////////////////////\n" \
           "/// TESTS PASS THE CRITERIA  : True ///\n" \
           "///////////////////////////////////////\n")
    return True


print("----\nPROG\n----")
tests = [{'x':5},{'x':-3},{'x':50}, {'x' : -1}]
itb_test(prog.graph, tests, 4)

print("----\nPGCD\n----")
tests_pgcd = [{'x':400, 'y' : 280},{'x':-15, 'y': 6},{'x':50, 'y' : 3}, {'x' : -10, 'y' : 4}]
itb_test(pgcd.graph, tests_pgcd, 3)
