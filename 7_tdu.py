from cfg.pgcd import pgcd


"""def extract_labels(G, curr_node=0):
    # on récupère l'ensemble des chemins possibles sous forme [{noeud: cmd}]
    # on garde que les chemins qui ont pour début cmd = assign et fin cmd = if ou while
    curr_node = 0
    cmd = G.nodes[curr_node]['cmd']
    res = []
    while cmd != "end":
        if cmd in ["if", "while"] :
            return [curr_node]
        elif cmd == "assign" :
            for a in pgcd.graph.successors(0) :
                curr_node
            return [curr_node].append(extract_labels(G, curr_node=c))"""

print("We didn't succeed to represent this criteria. We explained our approach in the read me.")
