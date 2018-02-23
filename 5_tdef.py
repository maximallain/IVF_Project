from cfg.prog import prog
from cfg.pgcd import pgcd
from parcours_graph import parcours_graph, initialization

def extract_labels_var(G, x):
    """ Returns a list of graph's nodes which contains the command 'assign' associated to the variable """
    labels = G.nodes
    l = []
    for node in labels :
        for child, value in G[node].items():
            if value['cmd'] == 'assign' :
                if x in value['var'] :
                    l.append(node)
    return l

def extract_labels(cfg):
    """ Returns a dictionary of list of graph's nodes which contains (variable, list of node which contain the command 'assign' associated to the variable) """
    d = {}
    for x in cfg.var :
        d[x]=extract_labels_var(cfg.graph,x)
    return d

def t_def(cfg, var, assign_dict):
    """ Returns a list of the visited nodes which contains the command 'while' or 'if' from the graph G crossed by variables initialized in 'var' """

    # Initialization
    G = cfg.graph
    cmd, curr_node = initialization(G, var)

    # Crossing the graph
    while cmd != "end":
        for edge in G.edges(curr_node, data=True):
            if edge[2]['cmd'] == 'assign' :
                for x in edge[2]['var'] :
                    try :
                        if curr_node not in assign_dict[x]:
                            assign_dict[x].append(curr_node)
                    except KeyError :
                        assign_dict[x] = [curr_node]
                    except TypeError:
                        assign_dict[x] = [curr_node]
        cmd, curr_node = parcours_graph(G, cmd, curr_node, var)

    # End
    G.nodes[curr_node]['msg'](var)
    return assign_dict

def t_def_tests(cfg, tests) :
    """ Takes a set of tests, a graph G and returns True if the test T-DEF is passed """
    assign_dict = {}
    for test in tests :
        assign_dict = t_def(cfg, test, assign_dict)
    for value in assign_dict.values():
        value.sort()
    return "////////////////////////////////////////\n" \
           "/// TESTS PASS THE CRITERIA  : {} ///\n" \
           "///////////////////////////////////////\n".format(assign_dict == extract_labels(cfg))

print("----\nPROG\n----")
tests = [{'x':5},{'x':-3},{'x':50}, {'x' : -1}]
t_def_tests(prog, tests)

print("----\nPGCD\n----")
tests_pgcd = [{'x':400, 'y' : 280},{'x':-15, 'y': 6},{'x':50, 'y' : 3}, {'x' : -10, 'y' : 4}]
print(t_def_tests(pgcd, tests_pgcd))
