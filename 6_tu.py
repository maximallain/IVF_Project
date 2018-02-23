from cfg.pgcd import pgcd
from cfg.prog import prog
from parcours_graph import parcours_graph, initialization


def extract_labels(G):
    """ Returns a dictionary whose key is a node and whose value is a dictionary of a node and a list of nodes which represents the path """
    label_assign = {}
    labels = G.nodes
    for node in labels:
        label_assign[node] = {}
        if G.node[node]['cmd'] == 'assign':
            print("Found on 'assign'")
            to_explore = []
            print("Node is %i" % node)

            # Initialisation de la pile
            for e in G.edges(node, data=True):
                to_explore.append(e[1])

            # On stocke dans to_explore tous les noeuds qui héritent de cette définition et dont on doit checker les assignations
            for curr_node in to_explore:
                print("Curr node is %i" % curr_node)

                # Ici on doit parcourir les enfants de ce node assign
                for edge_from_curr_node in G.edges(node, data=True):
                    child = edge_from_curr_node[1]
                    print("child : ".format(child))
                    if G.node[child]['cmd'] != 'assign':
                        # On se prépare à explorer ces enfants
                        to_explore.append(child)

                # On garde une trace des enfants if et while de cette boucle
                label_assign[node][child] = []
                if G.node[curr_node]['cmd'] == 'if' or G.node[curr_node]['cmd'] == 'while':
                    print("son is if or while")
                    for edge in G.edges(curr_node, data=True):
                        label_assign[node][curr_node].append(edge[1])
                to_explore.remove(curr_node)

    print(label_assign)
    return label_assign


def verify_criteria(label_assign):
    """ Returns False if all the elements 'labels_assign' were not crossed, True if there were """
    res = True
    for r in label_assign:
        for b in label_assign[r]:
            if label_assign[r] != []:
                print(
                    "Le noeud %i est un assign qui dont l' evaluations au noeud %i n'est pas faite par ce jeu de tests\n" % (
                    r, b))
                res = False
    return res


def tu(G, var, label_assign):
    """ Returns label_assign updated by the crossing of the graph G with the variables var """
    # Initialization
    cmd, curr_node = initialization(G, var)
    last_assign = 0

    # Crossing the graph
    while cmd != "end":

        if cmd == "if":
            for edge in G.edges(curr_node, data=True):
                if edge[1] > curr_node:
                    if edge[2]['bool'](var):
                        try:
                            # La condition a été executée POUR le last_assign traversé
                            label_assign[last_assign][curr_node].remove(edge[1])
                        except ValueError:
                            pass
                        except KeyError:
                            pass

        elif cmd == "assign":
            # On garde une trace du dernier assign traversé
            last_assign = curr_node

        elif cmd == "while":
            for edge in G.edges(curr_node, data=True):
                if edge[1] > curr_node:
                    if edge[2]['bool'](var):
                        try:
                            # La condition a été executée POUR le last_assign traversé
                            label_assign[last_assign][curr_node].remove(edge[1])
                        except ValueError:
                            pass
                        except KeyError:
                            pass

        cmd, curr_node = parcours_graph(G, cmd, curr_node, var)

    # End
    G.nodes[curr_node]['msg'](var)
    return label_assign


def tu_tests(G, tests):
    """ Takes a set of tests, a graph G and returns True if the criteria TU is passed """
    label_assign = extract_labels(G)
    for var in tests:
        label_assign = tu(G, var, label_assign)
    res = verify_criteria(label_assign)
    print("////////////////////////////////////////\n" \
           "/// TESTS PASS THE CRITERIA  : {} ///\n" \
           "///////////////////////////////////////\n".format(res))
    return res


print("----\nPROG\n----")
tests = [{'x': 5}, {'x': -3}, {'x': 50}, {'x': -1}]
tu_tests(prog.graph, tests)

print("----\nPGCD\n----")
tests_pgcd = [{'x': 400, 'y': 280}, {'x': -15, 'y': 6}, {'x': 50, 'y': 3}, {'x': -10, 'y': 4}]
tu_tests(pgcd.graph, tests_pgcd)
