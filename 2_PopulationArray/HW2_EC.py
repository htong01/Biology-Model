

import numpy as np

# Extra credits

m=np.zeros(75) # Birth rate
m[7:15]=0.42; m[15:28]=3.5; m[28:53]=4.3; m[53:75]=4.8
n=np.zeros(75) # population
n[7:15]=100/8; n[15:28]=200/13; n[28:53]=400/25; n[53:75]=500/22
p2=np.zeros(75) # Survival rate
p2[0:7]=0.76; p2[7:15]=0.84; p2[15:28]=0.92; p2[28:53]=0.95; p2[53:75]=0.96

#def vitalrate(p):
#    m=np.zeros(75) # Birth rate
#    m[7:15]=0.42; m[15:28]=3.5; m[28:53]=4.3; m[53:75]=4.8
#    n=np.zeros(75) # population
#    n[7:15]=100/8; n[15:28]=200/13; n[28:53]=400/25; n[53:75]=500/22
#    p2=np.zeros(75) # Survival rate
#    p2[0:7]=0.76; p2[7:15]=0.84; p2[15:28]=0.92; p2[28:53]=0.95; p2[53:75]=0.96
#    p2=p*1.05
#    n_next=np.zeros(75)
#    for i in range(5):
#        n_next[1:75]=n[0:74]*p2[0:74]
#        n_next[0]=n_next[1:75].dot(m[1:75])
#        print('young juveniles',n_next[0:7].sum())
#        print('older juveniles',n_next[7:15].sum())
#        print('young adults',n_next[15:28].sum())
#        print('mid-age adults',n_next[28:53].sum())
#        print('older adults',n_next[53:75].sum())
#        print('total population',n_next.sum())
#        print('\n')
#        n=n_next
#
#vitalrate(p[0:7])


p2[0:7]=0.76*1.05
n_next=np.zeros(75)
for i in range(2):
    n_next[1:75]=n[0:74]*p2[0:74]
    n_next[0]=n_next[1:75].dot(m[1:75])
    print('total population',n_next.sum())
    n=n_next


print('\n')
n=np.zeros(75) # population
n[7:15]=100/8; n[15:28]=200/13; n[28:53]=400/25; n[53:75]=500/22
p2[0:7]=0.76; p2[7:15]=0.84*1.05
n_next=np.zeros(75)
for i in range(2):
    n_next[1:75]=n[0:74]*p2[0:74]
    n_next[0]=n_next[1:75].dot(m[1:75])
    print('total population',n_next.sum())
    n=n_next

p2[7:15]=0.84; p2[15:28]=0.92*1.05
print('\n')
n=np.zeros(75) # population
n[7:15]=100/8; n[15:28]=200/13; n[28:53]=400/25; n[53:75]=500/22
n_next=np.zeros(75)
for i in range(2):
    n_next[1:75]=n[0:74]*p2[0:74]
    n_next[0]=n_next[1:75].dot(m[1:75])
    print('total population',n_next.sum())
    n=n_next

p2[28:53]=0.95*1.05; p2[15:28]=0.92
print('\n')
n=np.zeros(75) # population
n[7:15]=100/8; n[15:28]=200/13; n[28:53]=400/25; n[53:75]=500/22
n_next=np.zeros(75)
for i in range(2):
    n_next[1:75]=n[0:74]*p2[0:74]
    n_next[0]=n_next[1:75].dot(m[1:75])
    print('total population',n_next.sum())
    n=n_next

p2[28:53]=0.95; p2[53:75]=0.96*1.05
print('\n')
n=np.zeros(75) # population
n[7:15]=100/8; n[15:28]=200/13; n[28:53]=400/25; n[53:75]=500/22
n_next=np.zeros(75)
for i in range(2):
    n_next[1:75]=n[0:74]*p2[0:74]
    n_next[0]=n_next[1:75].dot(m[1:75])
    print('total population',n_next.sum())
    n=n_next
