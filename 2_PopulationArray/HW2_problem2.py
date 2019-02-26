import numpy as np

m=np.zeros(75) # Birth rate
m[7:15]=0.42; m[15:28]=3.5; m[28:53]=4.3; m[53:75]=4.8
p=np.zeros(75) # Survival rate
p[0:7]=0.76; p[7:15]=0.84; p[15:28]=0.92; p[28:53]=0.95; p[53:75]=0.96
n=np.zeros(75) # population
n[7:15]=100/8; n[15:28]=200/13; n[28:53]=400/25; n[53:75]=500/22

n_next=np.zeros(75)
for i in range(5):
    n_next[1:75]=n[0:74]*p[0:74]
    n_next[0]=n_next[1:75].dot(m[1:75])
    print('young juveniles',n_next[0:7].sum())
    print('older juveniles',n_next[7:15].sum())
    print('young adults',n_next[15:28].sum())
    print('mid-age adults',n_next[28:53].sum())
    print('older adults',n_next[53:75].sum())
    print('total population',n_next.sum())
    print('total population exclude young juveniles:',n_next[7:75].sum())
    print('\n')
    n=n_next