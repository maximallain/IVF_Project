from cfg.cfg_model import cfg


def pgcd_graph(G):
    G.add_node(0, cmd='skip')
    G.add_node(1, cmd='while')
    G.add_node(2, cmd='end', msg=lambda var: msg(var))

    G.add_edge(0, 1, bool=True, cmd='skip')
    G.add_edge(1, 1, bool=lambda var: cond_1(var), cmd='assign', func=lambda var: assign_1(var), var=('x', 'y'))
    G.add_edge(1, 2, bool=lambda var: not (cond_1(var)), cmd='skip')


def assign_1(var):
    x = var['x']
    var['x'] = var['y']
    var['y'] = x % var['y']


def cond_1(var):
    return var['x'] % var['y'] != 0


def msg(var):
    print('Le PGCD est : {}\n'.format(var['y']))


pgcd = cfg({'x', 'y'})
pgcd_graph(pgcd.graph)