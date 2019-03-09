"""
Program to accept values from the users for the computation

k: number of rooms
n: number of students
L: 2D matrix of order n*k
"""

k=int(input("Enter number of rooms: "))
n=int(input("Enter number of students: "))

L=[[0 for x in range(k)] for l in range(n)]

for i in range(n):
    for j in range(k):
        L[i][j]=int(input("Enter value for room "+str(j+1)+" as desired by student "+str(i+1)+": "))

for i in range(n):
    for j in range(k):
        print(L[i][j],end=' ')
    print()
    