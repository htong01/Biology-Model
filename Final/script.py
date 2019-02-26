#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 12:54:12 2018

@author: Huilin
"""

from scipy.integrate import odeint
import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt

#t = np.arange(0,100,0.1)
#
#def deriv(w,t,a,b,c,d, e,f,g,h, i,j,k): 
#    x,y,z = w
#    return np.array([ x*(a-b*y-c*z-d*x), y*(-e+f*x-g*y-h*z), z*(-i+j*x-k*y)])
#
#p=[0.1,0.02,0.001,0.3, 0.001,0.03,0.02,0.01, 0.05,0.1,0.001,  100,150,100]
## Live together
#p = [0.0005,0.00008,0.2,0.00045,  0.00006, 0.2, 0.1,0.00004,  0.00004, 0.0002, 0.004, 800, 200, 200]
#
#
#
#def run(p):
#    a,b,c,d,e,f,g,h,i,j,k,x0,y0,z0=p
#    yinit = np.array([x0,y0,z0]) 
#    yyy = odeint(deriv,yinit,t,args=(a,b,c,d,e,f,g,h,i,j,k))
#    
#    plt.figure(figsize=(7,5))
#    plt.plot(t,yyy[:,0],"b-",label="Species1")
#    plt.plot(t,yyy[:,1],"r-",label="2")
#    plt.plot(t,yyy[:,2],"g-",label="3")
#    plt.xlabel(u'Time t')
#    plt.ylabel(u'Population')
#    plt.legend(loc=4)
#    plt.show()
#
##    x1 = (a*h*k - c*h*i - d*e*k + d*g*i)/(b*h*k - c*h*j - d*f*k + d*g*j)
##    x2 = -(a*h*j - b*h*i - d*e*j + d*f*i)/(b*h*k - c*h*j - d*f*k + d*g*j)
##    x3 = -(a*f*k - a*g*j - b*e*k + b*g*i + c*e*j - c*f*i)/(b*h*k - c*h*j - d*f*k + d*g*j)
##    return x1,x2,x3
#
#run(p)



#%% C hunt for B and B hunt for A

t = np.arange(0,100,0.1)

def deriv(w,t, a,b,c, d,e,f,g, h,j,k): 
    x,y,z = w
    return np.array([ x*(a-b*x-c*y), y*(-d+e*x-f*y-g*z), z*(-h+j*y-k*z)])

# live together
p = [0.1,0.1,0.01, 0.3,0.003,0.002,0.01, 0.1,0.001,0.0001,  100,150,100]
# A dies out
p2 = [0.1,0.1,0.01, 0.3,0.003,0.002,0.01, 0.1,0.001,0.0001,  0,150,100]
# B dies out
p3 = [0.1,0.1,0.01, 0.3,0.003,0.002,0.01, 0.1,0.001,0.0001,  100,0,100]
# C dies out
p4 = [0.1,0.1,0.01, 0.3,0.003,0.002,0.01, 0.1,0.001,0.0001,  100,150,0]

def run(p):
    a,b,c,d,e,f,g,h,j,k,x0,y0,z0=p
    yinit = np.array([x0,y0,z0]) 
    yyy = odeint(deriv,yinit,t,args=(a,b,c, d,e,f,g, h,j,k))
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
run(p3)
run(p4)