import numpy as np
import random

# Problem 1
m=np.array([0,1,5/6,0]) # Birth rate
p=np.array([0.6,0.8,2/3,0]) # Survival rate
n=np.array([750,450,360,240]) # Initial population

segma=0
r=random.gauss(0,segma)
np.clip(r,-1,1)
p=p*(1+r)
for i in range(1,5):
    print("The "+str(i)+"th "+"year:")
    n[1:4]=np.round(n[0:3]*p[0:3])
    n[0]=np.round(n[1:4].dot(m[1:4]))
    total=n.sum()
    print('n0=',n[0],end='\t'); print('n1=',n[1],end='\t'); print('n2=',n[2],end='\t'); print('n3=',n[3],end='\t')
    print('n_total',total)
#%%
# Problem 2
m=np.array([0,1,5/6,0]) # Birth rate
p=np.array([0.6,0.8,2/3,0]) # Survival rate
n=np.array([750,450,360,240]) # Initial population
i=0
total=n.sum()
random.seed(0)

while total > 0:
    m=np.array([0,1,5/6,0]) # Birth rate
    p=np.array([0.6,0.8,2/3,0]) # Survival rate
    sigma=0.15
    r=random.gauss(0,sigma)
    np.clip(r,-1,None)
    p=p*(1+r); m=m*(1+r)
    np.clip(p,0,1)
    n[1:4]=np.round(n[0:3]*p[0:3])
    n[0]=np.round(n[1:4].dot(m[1:4]))
    total=float(n.sum())
    i+=1
print('\n')
print ('Need %d generations for the population to die out' %i)
#%%
# Problem 3
m=np.array([0,1,5/6,0]) # Birth rate
p=np.array([0.6,0.8,2/3,0]) # Survival rate
n=np.array([750,450,360,240]) # Initial population
i=0
total=n.sum()
random.seed(0)
while (total > 0):
    m=np.array([0,1,5/6,0]) # Birth rate
    p=np.array([0.6,0.8,2/3,0]) # Survival rate
    sigma=0.25
    r=random.gauss(0,sigma)
    np.clip(r,-1,None)
    p=p*(1+r); m=m*(1+r)
    np.clip(p,0,1)
    n[1:4]=np.round(n[0:3]*p[0:3])
    n[0]=np.round(n[1:4].dot(m[1:4]))
#    n[1:4]=n[0:3]*p[0:3]
#    n[0]=n[1:4].dot(m[1:4])
    total=float(n.sum())
    i+=1
print('\n')
print ('Need %d generations for the population to die out' %i)