def iter(values, cover,u,v,weights):
    R=[]
    T=[]
    n=len(values)
    k=len(values[0])
    for i in cover:
        if i[0] not in R:
            R.append(i[0])
        if i[1] not in T:
            T.append(i[1])
    R.sort()
    T.sort()

    epsilon=values[0][0]
    for i in range(n):
        for j in range(k):
            if i not in R and j not in T:
                exc=u[i]+v[j]-weights[i][j]
                epsilon=min(exc,epsilon)

    for i in range(n):
        if i not in R:
            u[i]=u[i]-epsilon

    for j in range(k):
        if j in T:
            v[j]=v[j]+epsilon

def formg(values, weights,u ,v):
    for i in range(len(values)):
        for j in range(len(values[0])):
            values[i][j]=u[i]+v[j]-weights[i][j]
    print(values)
    # print(weights)
    # print("lol")

    # cover=[]
    for i in range(len(values)):
        for j in range(len(values[0])):
            if values[i][j]==0:
                if (i,j) not in cover:
                    cover.append((i,j))
    print(cover)

class GFG: 
	def __init__(self,graph): 
		self.graph = graph 
		self.ppl = len(graph) 
		self.jobs = len(graph[0])
        # self.matchR = [-1] * self.jobs 

	def bpm(self, u, seen): 
		for v in range(self.jobs): 
			if self.graph[u][v]==0 and seen[v] == False: 
				seen[v] = True
				if self.matchR[v] == -1 or self.bpm(self.matchR[v], seen): 
					self.matchR[v] = u 
					return True
		return False

	
	def maxBPM(self): 
		self.matchR = [-1] * self.jobs
		result = 0
		for i in range(self.ppl): 
			seen = [False] * self.jobs 
			if self.bpm(i, seen):
				result += 1
		return result


def main():
    n=int(input())
    k=int(input())
    values=[[0 for x in range(k)] for y in range(n)]
    for i in range(n):
        for j in range(k):
            values[i][j]=int(input())
    global u
    global v
    u=[]
    for i in range(n):
        u.append(max(values[i]))
    v=[0]*k
    global weights
    # weights=list(values)
    weights=[[0 for x in range(k)] for y in range(n)]
    for i in range(n):
        for j in range(k):
            weights[i][j]=values[i][j]

    g = GFG(values)
    global cover
    cover=[]
    formg(values,weights,u,v)
    iter(values, cover,u,v,weights)
    # formg(values,weights,u,v)
    m=g.maxBPM()
    print("m outside",m)
    while(m!=n):
        print(m)
        iter(values, cover,u,v,weights)
        formg(values,weights,u,v)
        m=g.maxBPM()
    
    print(cover)
main()