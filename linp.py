import scipy.optimize

c=[1,1,1]
A_eq =[[1,1,1]]
b_eq =[1000]
bound=((216,401),(315,439),(388,512))

res=scipy.optimize.linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bound, method='simplex')
print(res.x)