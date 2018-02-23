def parcours_graph(G, cmd, curr_node, var):
    if cmd == "skip":
        for key in G[curr_node]:
            curr_node = key
            cmd = G.nodes[curr_node]['cmd']

    elif cmd == "if":
        for edge in G.edges(curr_node, data=True):
            if edge[2]['bool'](var):
                curr_node = edge[1]
                cmd = G.nodes[curr_node]['cmd']
                break

    elif cmd == "assign":
        for edge in G.edges(curr_node, data=True):
            edge[2]['func'](var)
            for key, value in var.items():
                print("new value of {} : {}".format(key, value))
            curr_node = edge[1]
            cmd = G.nodes[curr_node]['cmd']

    elif cmd == "while":
        for edge in G.edges(curr_node, data=True):
            if edge[2]['bool'](var):
                if edge[2]['cmd'] == 'assign':
                    edge[2]['func'](var)
                    for key, value in var.items():
                        print("new value of {} : {}".format(key, value))
                curr_node = edge[1]
                cmd = G.nodes[curr_node]['cmd']
                break
    return cmd, curr_node

def initialization(G,var) :
    curr_node = 0
    cmd = G.nodes[curr_node]['cmd']
    for key, value in var.items():
        print("initial value of {} : {}".format(key, value))
    return cmd, curr_node