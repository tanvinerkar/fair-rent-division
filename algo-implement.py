
import scipy.optimize
import networkx as nx
from pulp import *
import matplotlib.pyplot as plt
# import scipy.optimize

k=int(input("Enter number of rooms: "))
n=int(input("Enter number of students: "))

inp=[[-100 for x in range(k)] for l in range(k)]

for i in range(n):
    for j in range(k):
        inp[i][j]=int(input("Enter value for room "+str(j+1)+" as desired by student "+str(i+1)+": "))

file_o=open('op','w')
file_o.close()
file_o=open('op','a')
# k=4
# n=3
from_nodes = [i for i in range(1,k+1)]
to_nodes = [i for i in range(1,k+1)]

ucap={}
vcap={}
for i in range(1,k+1):
    ucap[i]=1
    vcap[i]=1

# ucap = {1: 1, 2: 1, 3: 1} #u node capacities
# vcap = {1: 1, 2: 1, 3: 1} #v node capacities

""" inp=[[216, 439, 345,0],
     [401, 211, 388,0],
     [173, 315, 512,0],
     [-100,-100,-100,-100]] """
wts={}
for i in range(1,k+1):
    for j in range(1,k+1):
        wts[(i,j)]=inp[i-1][j-1]
""" wts = {(1, 1): 216, (1, 2): 439, (1, 3): 345,
       (2, 1): 401, (2, 2): 211, (2, 3): 388,
       (3, 1): 173, (3, 2): 315, (3, 3): 512}  """

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
    file_o.write( "Status:"+ LpStatus[prob.status]+'\n')
    return(prob)


def print_solution(prob):
    # Each of the variables is printed with it's resolved optimum value
    for v in prob.variables():
        if v.varValue > 1e-3:
            n=v.name
            va=v.varValue
            file_o.write(n+' = '+str(va)+'\n')
    tot=round(value(prob.objective), 4)
    file_o.write("Sum of wts of selected edges = "+str(tot))


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

file_o.close()

file_o=open('op','r')
L=file_o.readlines()
room_allot=[]
for i in range(1,n+1):
    room_allot.append((L[i][4],L[i][2]))
file_o.close()

inp_transpose=[[0 for x in range(k)] for y in range(k)]
for i in range(k):
    for j in range(k):
        inp_transpose[j][i]=inp[i][j]

room_allot.sort()
# print(len(room_allot))
bound=[]
for i in range(n):
    if int(room_allot[i][1])<=n:
        mx=inp_transpose[i].pop(int(room_allot[i][1])-1)
        mx_new=max(inp_transpose[i])
        bound.append((mx_new,mx))

c=[1 for x in range(n)]
A_eq =[[1 for x in range(n)]]
b_eq =[1000]
# bound=((216,401),(315,439),(388,512))

res=scipy.optimize.linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bound, method='simplex')
# print(res.x)

utility=0.0

# print(len(room_allot))

for i in range(n):
    # if int(room_allot[i][1])<=n:
    utility+= (inp[int(room_allot[i][1])-1][i]) - (res.x)[i]

avg_utility=utility/n

final_answer=[]
for i in range(n):
    # if int(room_allot[i][1])<=n:
    temp_price=inp[int(room_allot[i][1])-1][i] - avg_utility
    final_answer.append((i+1,temp_price))

# print("Room\tPrice")
for i in range(n):
    print(str(i+1),'\t', round(final_answer[i][1],2))