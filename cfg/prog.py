from cfg.cfg_model import cfg
import sympy as sym

def prog_graph(G):
    x = sym.Symbol('x')
    G.add_node(0, cmd='skip')
    G.add_node(1, cmd='if')
    G.add_node(2, cmd='assign')
    G.add_node(3, cmd='assign')
    G.add_node(4, cmd='if')
    G.add_node(5, cmd='assign')
    G.add_node(6, cmd='assign')
    G.add_node(7, cmd='while')
    G.add_node(8, cmd='end', msg=lambda var : msg(var))

    G.add_edge(0, 1, bool=True, cmd='skip',symb=x)
    G.add_edge(1, 2, bool=lambda var: cond_1(var), cmd='skip', symb=sym.Function('x<=0'), val_bool = True)
    G.add_edge(1, 3, bool=lambda var: not (cond_1(var)), cmd='skip',symb=sym.Function('x>0'), val_bool = False)
    G.add_edge(2, 4, bool=True, cmd='assign', func=lambda var: assign_1(var), var=('x'), symb=-x)
    G.add_edge(3, 4, bool=True, cmd='assign', func=lambda var: assign_2(var), var=('x'), symb=1-x)
    G.add_edge(4, 5, bool=lambda var: cond_2(var), cmd='skip', symb=sym.Function('x==1'), val_bool = True)
    G.add_edge(4, 6, bool=lambda var: not (cond_2(var)), cmd='skip',symb=sym.Function('x!=1'), val_bool = False)
    G.add_edge(5, 7, bool=True, cmd='assign', func=lambda var: assign_3(var), var=('x'), symb=1)
    G.add_edge(6, 7, bool=True, cmd='assign', func=lambda var: assign_4(var), var=('x'), symb=x+1)
    G.add_edge(7, 7, bool=lambda var: cond_3(var), cmd='assign', func=lambda var: assign_5(var), var=('x'), symb=x+1)
    G.add_edge(7, 8, bool=lambda var: not (cond_3(var)), cmd='skip', symb=sym.Function('x>=10'))
    return G

def assign_1(var):
    var['x'] = -var['x']

def assign_2(var):
    var['x'] = 1-var['x']

def assign_3(var):
    var['x'] = 1

def assign_4(var):
    var['x'] += 1

def assign_5(var):
    var['x'] += 1

def cond_1(var):
    return var['x']<=0

def cond_2(var):
    return var['x']==1

def cond_3(var):
    return abs(var['x'])<10

def msg(var):
    print("Final value of x : {}\n".format(var['x']))

prog = cfg({'x'})
prog_graph(prog.graph)