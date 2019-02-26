#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 21:37:51 2018

@author: yuanning
"""

from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

'''
this is for  2 species, B x2 eats x1
assume:
1 when the food is plenty, the birth rate is in direct proportion to its population,
and the death rate is related to both the number of predator and prey itself.
2 the birth rate of predator is depend on the number of prey and predator, 
and the death rate is depend on the number of predator.
'''

'''
this model show that in the final, #predator and #prey will get balance. 
They'll finally live together: k2 & K=k3 shows predation; k1 & k4 shows breed
We could see the priod of two species: 
    when the #predator reaches max, 
    the #prey will decrease. At this moment: #predator = k1/k2
    when the #prey reaches max,
    the #predator will decrease. #prey = k4/k3
    ...

'''
t = np.arange(0,100,0.1)

def deriv(w,t,k1, k2, k3, k4): 
    x1,x2 = w
    return np.array([ k1*x1 - k2*x1 *x2,
                      k3*x1*x2 - k4*x2
                     ])
# x2 eats x1
p1 = [0.2, 0.0005, 0.0002, 0.2, 1000, 600]


def run(p):
    k1, k2, k3, k4,x1,x2 = p
    yinit = np.array([x1,x2]) 
    yyy = odeint(deriv,yinit,t,args=(k1, k2, k3, k4))
    
    plt.figure(figsize=(7,5))
    plt.plot(t,yyy[:,0],"b-",label="x1-prey")
    plt.plot(t,yyy[:,1],"r-",label="x2-predator")
    plt.plot([0,100],[1000,1000],"y--")
    plt.plot([0,100],[400,400],"y--")
    
    plt.xlabel(u'time')
    plt.ylabel(u'population')
    plt.title(u'curve')
    plt.legend(loc=4)
    plt.show()
run(p1)
#%%
'''
in this model, we also consider the competition in their own species.
Difference with 1st model:
Because of the environment, we can not get a priod-like graph like 1.

'''

t = np.arange(0,1000,0.1)

def deriv2(w,t,k1, k2, k3, k4, k5, k6): 
    x1,x2 = w
    return np.array([ x1*(k1 - k2*x1 - k3*x2),
                      x2*(k4*x1 -k5*x2 - k6)
                     ])
# live together
p1 = [0.2, 0.00001,0.0005, 0.0002,0.00001, 0.2,1500, 500]

def run(p):
    k1, k2, k3, k4, k5, k6,x1,x2 = p
    yinit = np.array([x1,x2]) 
    yyy = odeint(deriv2,yinit,t,args=(k1, k2, k3, k4, k5, k6))
    
    plt.figure(figsize=(7,5))
    plt.plot(t,yyy[:,0],"b-",label="x1-prey")
    plt.plot(t,yyy[:,1],"r-",label="x2-predator")
    plt.plot([0,1000],[379,379],"y--")
    plt.plot([0,1000],[1018,1018],"y--")
    
    plt.xlabel(u'time')
    plt.ylabel(u'population')
    plt.title(u'curve')
    plt.legend(loc=4)
    plt.show()
run(p1)

#%%

t = np.arange(0,1000,0.1)

def deriv2(w,t,k1, k2, k3, k4, k5, k6, k7, ,k8, k9, k10): 
    x1,x2 = w
    return np.array([ x1*(k1 - k2*x1 - k3*x2),
                      x2*(k4*x1 -k5*x2 - k6)
                     ])
# live together
p1 = [0.2, 0.00001,0.0005, 0.0002,0.00001, 0.2,1500, 500]

def run(p):
    k1, k2, k3, k4, k5, k6,x1,x2 = p
    yinit = np.array([x1,x2]) 
    yyy = odeint(deriv2,yinit,t,args=(k1, k2, k3, k4, k5, k6))
    
    plt.figure(figsize=(7,5))
    plt.plot(t,yyy[:,0],"b-",label="x1-prey")
    plt.plot(t,yyy[:,1],"r-",label="x2-predator")
    plt.plot([0,1000],[379,379],"y--")
    plt.plot([0,1000],[1018,1018],"y--")
    
    plt.xlabel(u'time')
    plt.ylabel(u'population')
    plt.title(u'curve')
    plt.legend(loc=4)
    plt.show()
run(p1)
