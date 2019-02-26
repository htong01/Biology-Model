import numpy as np

m=np.array([0,1,5/6,0]) # Birth rate
p=np.array([0.6,0.8,2/3,0]) # Survival rate
n=np.array([0,1200,900,900]) # Initial population

# Problem 1
n1_1=n[0]*p[0]
n1_2=n[1]*p[1]
n1_3=n[2]*p[2]
n1_0=n1_1*m[1]+n1_2*m[2]+n1_3*m[3]
print('First Year')
print('n0=',n1_0)
print('n1=',n1_1)
print('n2=',n1_2)
print('n3=',n1_3)

# Problem 2
print('\n'*3)
for i in range(1,71):
    print("The "+str(i)+"th "+"year:")
#    n3=n2*p2
#    n2=n1*p1
#    n1=n0*p0
    n[1:4]=n[0:3]*p[0:3]
    n[0]=n[1]*m[1]+n[2]*m[2]+n[3]*m[3]
    total=n.sum()
    print('n0=',n[0],end='\t'); print('n1=',n[1],end='\t'); print('n2=',n[2],end='\t'); print('n3=',n[3],end='\t')
    print('n_total',total)


# Problem 3
print('\n'*3)
m=np.array([0,1,0.9,0]) # Birth rate
p=np.array([0.6,0.8,2/3,0]) # Survival rate
n=np.array([0,1200,900,900]) # Initial population


for i in range(1,71):
    print("The "+str(i)+"th "+"year:")
    n[1:4]=n[0:3]*p[0:3]
    n[0]=n[1]*m[1]+n[2]*m[2]+n[3]*m[3]
    total=n.sum()
    print('n0=',n[0],end='\t'); print('n1=',n[1],end='\t'); print('n2=',n[2],end='\t'); print('n3=',n[3],end='\t')
    print('n_total',total)

