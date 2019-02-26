
from scipy.integrate import odeint
import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt

# C hunt for A and B

t = np.arange(0,1000,0.1)

def deriv(w,t,a,b,c,d,e,f,g,h,i,j,k): 
    x,y,z = w
    return np.array([ x*(a-b*y-c*z), y*(-d+e*x-f*y-g*z), z*(-h+i*x-j*y-k*z)])

# live together
p = [0.1,0.002,0.0001, 0.3,0.003,0.0002,0.001, 0.1,0.01,0.001,0.1,  100,150,100]
# A dies out
p2 = [0.1,0.002,0.0001, 0.3,0.003,0.0002,0.001, 0.1,0.01,0.001,0.1,  0,150,100]
# B dies out(失败了)
# p3 = [0.1,0.002,0.0001, 0.3,0.003,0.0002,0.001, 0.1,0.01,0.001,0.1,  100,0,100]
# C dies out
p4 = [0.1,0.002,0.0001, 0.3,0.003,0.0002,0.001, 0.1,0.01,0.001,0.1,  100,150,0]

def run(p):
	a,b,c,d,e,f,g,h,i,j,k,x0,y0,z0=p
	yinit = np.array([x0,y0,z0]) 
	yyy = odeint(deriv,yinit,t,args=(a,b,c,d,e,f,g,h,i,j,k))

	plt.figure(figsize=(7,5))
	plt.plot(t,yyy[:,0],"b-",label="Species1")
	plt.plot(t,yyy[:,1],"r-",label="2")
	plt.plot(t,yyy[:,2],"g-",label="3")
	plt.xlabel(u'Time t')
	plt.ylabel(u'Population')
	plt.legend(loc=4)
	plt.show()

run(p)
run(p2)
# run(p3)
run(p4)