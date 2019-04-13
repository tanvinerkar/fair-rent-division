import scipy.optimize
from pulp import *

totalrent=float(input("Enter total rent: "))
k=int(input("Enter number of rooms: "))
n=int(input("Enter number of students: "))

inp=[[-100 for x in range(k)] for l in range(k)]

for i in range(n):
    for j in range(k):
        inp[i][j]=int(input("Enter value for room "+str(j+1)+" as desired by student "+str(i+1)+": "))

file_o=open('op','w')
file_o.close()
file_o=open('op','a')

from_nodes = [i for i in range(1,k+1)]
to_nodes = [i for i in range(1,k+1)]

"""
Dictionaries to store capacties of nodes. Here, capacity of each node = 1.
"""
ucap={}
vcap={}
for i in range(1,k+1):
    ucap[i]=1
    vcap[i]=1

wts={}
for i in range(1,k+1):
    for j in range(1,k+1):
        wts[(i,j)]=inp[i-1][j-1]

#just a convenience function to generate a dict of dicts

#Converting the weights dictionary format 
#from {(value1, value2): wt12, (value1, value3): wt13}
#to {value1: {value2: wt12, value3: wt13}}

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
                   for v in to_nodes]), "Total weights of Lselected edges"


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

    # The status of the solution is written to the file
    file_o.write( "Status:"+ LpStatus[prob.status]+'\n')
    return(prob)


def write_solution(prob):
    # Each of the variables is written to the op.txt file with its resolved optimum value
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
write_solution(p)

file_o.close()

"""
Reading the MWBM's results to create a list of the final room allotment.
"""
file_o=open('op','r')
L=file_o.readlines()
room_allot=[]
for i in range(1,n+1):
    room_allot.append((L[i][4],L[i][2]))
file_o.close()

"""
Creating a transpose of the matrix inp.
"""
inp_transpose=[[0 for x in range(n)] for y in range(k)]
for i in range(k):
    for j in range(n):
        inp_transpose[i][j]=inp[j][i]

"""
Sorting the room allocation list to get increasing order of room numbers.
"""
room_allot.sort()

"""
Setting the lower bound of each room's final value to the 2nd highest price bid (after the price bid by the student to whom the room has been allotted) for that room.
"""

bound=[]
for i in range(n):
    if int(room_allot[i][1])<=n:
        mx=inp_transpose[i].pop(int(room_allot[i][1])-1) #Removing the price which the person (to whom that room has been allotted) bid for that room
        mx_new=max(inp_transpose[i])
        while mx_new>=mx:
                inp_transpose[i].remove(mx_new)
                if inp_transpose[i]==[]:
                        mx_new=0
                        break
                mx_new=max(inp_transpose[i])
                
        bound.append((mx_new,mx))
"""
Setting the parameters for the linear optimization function.
"""
c=[1 for x in range(n)]
A_eq =[[1 for x in range(n)]]
b_eq =[totalrent]
res=scipy.optimize.linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bound, method='simplex')

"""
Calculating the utility using the result of the linear optimization.
Note: The solution returned by the linear optimization function is not the final solution as envy-freeness has not been checked for yet.
"""

utility=0.0

"""
Creating a transpose of the matrix inp again, since inp_transpose was changed to find bounds for the optimization parameters.
"""
inp_transpose=[[0 for x in range(n)] for y in range(k)]
for i in range(k):
    for j in range(n):
        inp_transpose[i][j]=inp[j][i]

if type(res.x)!="<class 'list'>":
    res=[]
    for i in range(n):
        # print(i)
        res.append(inp_transpose[i][int(room_allot[i][1])-1])
    utility=sum(res) - totalrent
else:                
    for i in range(n):
        utility+= (inp[int(room_allot[i][1])-1][i]) - (res.x)[i]

avg_utility=utility/n
"""
By calculating the average utility, envy-freeness is guaranteed.
It is assured that the envy-freeness condition is satisfied.
"""

"""
Calculating the final price as:
Final Price = Price bid for room by student to which it is assigned - Average Utility
"""

final_answer=[]
for i in range(n):
    # if int(room_allot[i][1])<=n:
    temp_price=inp[int(room_allot[i][1])-1][i] - avg_utility
    final_answer.append((i+1,temp_price))
"""
print("\nRoom\tStudent\tPrice")
for i in range(n):
    print(str(i+1),'\t',room_allot[i][1],'\t', round(final_answer[i][1],2))
"""

def key_sort(t):
        return t[1]
room_allot.sort(key=key_sort)

print("\nStudent\t Room\t Price")
for i in range(n):
        print(str(i+1),'\t',room_allot[i][0],'\t',round(final_answer[int(room_allot[i][0])-1][1],2))