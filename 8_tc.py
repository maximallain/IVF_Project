from cfg.prog import prog
from cfg.pgcd import pgcd

def extract_conditions(G):
    """ Returns a list of conditions which contains the command 'if' or 'while' """
    labels_if_while = []
    labels = G.nodes
    for node in labels :
        if G.node[node]['cmd'] in ['if', 'while']:
            for edge in G.edges(node, data=True):
                labels_if_while.append(edge[2]['bool'])
                break
    return labels_if_while

def td(var, label):
    """ Returns 'T' if all the conditions returned 'true', 'F' if all the conditions returned 'false' and else, returns '' """
    res = {True : [], False : []}
    for key, value in var.items():
        print("initial value of {} : {}".format(key, value))
    i = 0
    for cond in label:
        if cond(var) :
            res[True].append(i)
        else :
            res[False].append(i)
        i+=1
    for key, value in res.items():
        if len(value) == len(label) :
            if key :
                return "T"
            else :
                return "F"
    return ""

def td_test(G, tests):
    """ Takes a set of tests, a graph G and returns True if the criteria TD is passed """
    labels_if_while = extract_conditions(G)
    l = ["T","F"]
    for test in tests:
        res = td(test, labels_if_while)
        print(res)
        if res in l :
            l.remove(res)
    print("////////////////////////////////////////\n" \
           "/// TESTS PASS THE CRITERIA  : {} ///\n" \
           "///////////////////////////////////////\n".format(l == []))
    return l == []

print("----\nPROG\n----")
tests = [{'x': 5}, {'x': -3}, {'x': 50}, {'x': -1}, {'x': 1}]
td_test(prog.graph, tests)

print("----\nPGCD\n----")
tests_pgcd = [{'x': 400, 'y': 280}, {'x': -15, 'y': 6}, {'x': 50, 'y': 3}, {'x': -10, 'y': 4}, {'x':10, 'y':5}]
td_test(pgcd.graph, tests_pgcd)
