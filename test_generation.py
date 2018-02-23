from cfg.prog import *
import networkx as nx
#from pyscipopt import Model, quicksum, multidict
import sympy as sym
from sympy.utilities.lambdify import lambdastr

def all_paths(G):
    """
    Cette fonction renvoie tous les chemins du noeud 'start' au noeud 'end'.
    Elle utilise la fonction all_paths_utils

    Output: Object with all paths
    Avec un chemin = [Node,Node,Node...]
    """
    print("Generation des chemins...")
    return nx.all_simple_paths(G,1,8)

def generate_contraints(G):
    """
    Cette fonction renvoie un tableau: [CONST,CONST...]
    Avec CONST = [A,A...]
    et A avec une suite de transformations ou de contraintes portant sur les variables du problème. Exemple: "x+y+5" ou 4x+5<2
    """
    simple_paths = all_paths(G)
    all_constraints=[]
    for path in simple_paths:
        ass_constraints=[]
        for step,next_step in zip(path,path[1:]):
            if G.node[step]['cmd']=="assign":
                for edge in G.edges(step,data=True):
                    if edge[0]==step and edge[1]==next_step:
                        ass_constraints.append(('func',edge[2]['symb']))
            elif G.node[step]['cmd']=="if" or "while":
                for edge in G.edges(step,data=True):
                    if edge[0]==step and edge[1]==next_step:
                        ass_constraints.append(('bool',edge[2]['symb']))
        all_constraints.append(ass_constraints)
    return all_constraints

def set_problem(paths_of_constraints):
    tests=[]
    print("Liste des contraintes associées à chaque chemin :")
    for path in paths_of_constraints:
        print("Pour le chemin : ")
        print(path)
        # Pour chaque path on associe un problème d'optimisation
        #model = Model("path")
        #self.model.setObjective(quicksum(x), "minimize")
        x = sym.Symbol('x')
        exp=x
        all_func=sym.Function('x')
        for const in path:
            if const[0]=='bool':
                c = const[1]
                #Dans ce cas là on peut directement associer cette contrainte à notre problème d'optimisation
                # On applique à c toutes les transformations considérées jusqu'à maintenant
                c=all_func(c)
                print("Nouveau prédicat de chemin : ")
                print(c)
                # on ajoute la contrainte à notre problème
                #self.model.addCons(c, "const")
            if const[0]=='func':
                func = const[1]
                # On doit appliquer une transformation à nos variables
                all_func = sym.Function(str(all_func(func)))

        #potential_test = model.optimize()
        print("Ces contraintes sont envoyées à un solveur de contraintes (pyscipopt)")
        #tests=tests.append(potential_test)
        return tests


if __name__ == "__main__":
    prog = cfg({'x'})
    G=prog_graph(prog.graph)
    paths_of_constraints_and_transf = generate_contraints(G)
    tests = set_problem(paths_of_constraints_and_transf)
