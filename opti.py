import networkx as nx
from pulp import *
import matplotlib.pyplot as plt
# import scipy.optimize



from_nodes = [1, 2, 3]
to_nodes = [1, 2, 3]
ucap = {1: 1, 2: 1, 3: 1} #u node capacities
vcap = {1: 1, 2: 1, 3: 1} #v node capacities

wts = {(1, 1): 216, (1, 2): 439, (1, 3): 345,
       (2, 1): 401, (2, 2): 211, (2, 3): 388,
       (3, 1): 173, (3, 2): 315, (3, 3): 512} 

#just a convenience function to generate a dict of dicts
def create_wt_doubledict(from_nodes, to_nodes):

    wt = {}
    for u in from_nodes:
        wt[u] = {}
        for v in to_nodes:
            wt[u][v] = 0

    for k,val in wts.items():
        u,v = k[0], k[1]
        wt[u][v] = val
    return(wt)

def solve_wbm(from_nodes, to_nodes, wt):
    ''' A wrapper function that uses pulp to formulate and solve a WBM'''

    prob = LpProblem("WBM Problem", LpMaximize)

    # Create The Decision variables
    choices = LpVariable.dicts("e",(from_nodes, to_nodes), 0, 1, LpInteger)

    # Add the objective function 
    prob += lpSum([wt[u][v] * choices[u][v] 
                   for u in from_nodes
                   for v in to_nodes]), "Total weights of selected edges"


    # Constraint set ensuring that the total from/to each node 
    # is less than its capacity
    for u in from_nodes:
        for v in to_nodes:
            prob += lpSum([choices[u][v] for v in to_nodes]) <= ucap[u], ""
            prob += lpSum([choices[u][v] for u in from_nodes]) <= vcap[v], ""


    # The problem data is written to an .lp file
    prob.writeLP("WBM.lp")

    # The problem is solved using PuLP's choice of Solver
    prob.solve()

    # The status of the solution is printed to the screen
    print( "Status:", LpStatus[prob.status])
    return(prob)


def print_solution(prob):
    # Each of the variables is printed with it's resolved optimum value
    for v in prob.variables():
        if v.varValue > 1e-3:
            print(f'{v.name} = {v.varValue}')
    print(f"Sum of wts of selected edges = {round(value(prob.objective), 4)}")


def get_selected_edges(prob):

    selected_from = [v.name.split("_")[1] for v in prob.variables() if v.value() > 1e-3]
    selected_to   = [v.name.split("_")[2] for v in prob.variables() if v.value() > 1e-3]

    selected_edges = []
    for su, sv in list(zip(selected_from, selected_to)):
        selected_edges.append((su, sv))
    return(selected_edges)        

wt = create_wt_doubledict(from_nodes, to_nodes)
p = solve_wbm(from_nodes, to_nodes, wt)
print_solution(p)


