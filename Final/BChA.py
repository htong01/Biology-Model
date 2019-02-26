from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0,1000,0.1)

def deriv(w,t,k1, k2, k3, k4, k5, k6, k7, k8, k9, k10): 
    x1,y1,y2 = w
    return np.array([ x1*(k7 - k8 * x1 - k9 * y1 -k10 * y2), 
                      y1*(k1 * x1 - k2 * y1 -k3),
                      y2*(k4 * x1 - k5 * y2- k6)
                     ])
# live together
p1 = [0.0005, 0.00008, 0.2, 0.00045, 0.00006, 0.2, 0.1, 0.00004, 0.0002, 0.0004, 800, 200, 200]
# y1 died：
p2 = [0.00025, 0.00006, 0.1, 0.0002, 0.00006, 0.1, 0.2, 0.00002, 0.0008, 0.0008, 800, 200, 200]
# y2 died:
p3 = [0.0001, 0.00006, 0.1, 0.0002, 0.00006, 0.1, 0.2, 0.00002, 0.0008, 0.0005, 800, 200, 200]
# y1 and y2 died:
p4 = [0.0002, 0.0002, 0.5, 0.0008, 0.0003, 0.4, 0.1, 0.0002, 0.0004, 0.0005, 800, 200 , 200]

def run(p):
    k1, k2, k3, k4, k5, k6, k7, k8, k9, k10,x1,y1,y2 = p
    yinit = np.array([x1,y1,y2]) # init
    yyy = odeint(deriv,yinit,t,args=(k1, k2, k3, k4, k5, k6, k7, k8, k9, k10))
    
    plt.figure(figsize=(7,5))
    plt.plot(t,yyy[:,0],"b-",label="x1")
    plt.plot(t,yyy[:,1],"r-",label="y1")
    plt.plot(t,yyy[:,2],"g-",label="y2")
#    plt.plot([0,1000],[250,250],"y--")
#    plt.plot([0,1000],[375,375],"y--")
#    plt.plot([0,1000],[375,375],"y--")
    plt.plot([0,1000],[0,0],"y--")
    
    plt.xlabel(u'time')
    plt.ylabel(u'population')
    plt.title(u'live together')
    plt.legend(loc=4)
    plt.show()
run(p1)
#run(p2)
#run(p3)
#run(p4)