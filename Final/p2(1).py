#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 19:37:01 2018

@author: yuanning
"""

from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0,200,0.1)

def deriv(w,t,k1, k2, k3, k4, k5, k6): 
    x,y,z,n = w
    return np.array([ k1 - k2*x - k3*x*y + k4*z, 
                      k3*x*y -(k2+k5+k6)*y,
                      k6*y -(k2+k4)*z,
                      k1-k2*n -k5*y
                     ])
#stable population
p1 = [3,0.005, 0.0013, 0, 0.042, 0.001,80,20,20,120]

def run(p):
    k1, k2, k3, k4, k5, k6, x,y,z,n = p
    yinit = np.array([x,y,z,n]) 
    yyy = odeint(deriv,yinit,t,args=(k1, k2, k3, k4, k5, k6))
    
    plt.figure(figsize=(7,5))
    plt.plot(t,yyy[:,0],"b-",label="no disease")
    plt.plot(t,yyy[:,1],"r-",label="have disease")
    plt.plot(t,yyy[:,2],"g-",label="recovery")
    plt.plot(t,yyy[:,3],"y-",label="total population")

    #plt.plot([0,1000],[250,250],"y--")
    #plt.plot([0,1000],[375,375],"y--")
    #plt.plot([0,1000],[375,375],"y--")
    #plt.plot([0,1000],[0,0],"y--")
    
    plt.xlabel(u'time')
    plt.ylabel(u'population')
    plt.title(u'curve')
    plt.legend(loc=4)
    plt.show()
run(p1)
#%%
t = np.arange(0,20000,0.1)

def deriv2(w,t,k1, k2, k3, k4, k5, k6): 
    x,y,z,n = w
    return np.array([ k1*n - k2*x - k3*x*y + k4*z, 
                      k3*x*y -(k2+k5+k6)*y,
                      k6*y -(k2+k4)*z,
                      (k1-k2)*n -k5*y
                     ])
#stable population
p1 = [0.006, 0.005, 0.0003, 0, 0.02, 0.001, 80, 20,0, 1000]

def run(p):
    k1, k2, k3, k4, k5, k6, x,y,z,n = p
    yinit = np.array([x,y,z,n]) 
    yyy = odeint(deriv2,yinit,t,args=(k1, k2, k3, k4, k5, k6))
    
    plt.figure(figsize=(7,5))
    plt.plot(t,yyy[:,0],"b-",label="no disease")
    plt.plot(t,yyy[:,1],"r-",label="have disease")
    plt.plot(t,yyy[:,2],"g-",label="recovery")

    #plt.plot([0,1000],[250,250],"y--")
    #plt.plot([0,1000],[375,375],"y--")
    #plt.plot([0,1000],[375,375],"y--")
    #plt.plot([0,1000],[0,0],"y--")
    
    plt.xlabel(u'time')
    plt.ylabel(u'population')
    plt.title(u'curve')
    plt.legend(loc=4)
    plt.show()
run(p1)

#%%
t = np.arange(0,25,0.1)

def deriv0(w,t,k1, k2): 
    x,y,z,n = w
    return np.array([ - k1*x*y, 
                      k1*(n-y)*y,
                      k2*(y),
                      - k1*x*y + k1*(n-y)*y + k2*y
                      
                     ])
#stable population
#p1 = [0.006, 0.005, 0.0003, 0, 0.02, 0.001, 80, 20,0, 1000]


p1 = [ 0.000004, 0.000002, 8000, 1000, 1000, 10000]

def run(p):
    k1, k2, x, y, z, n = p
    
    yinit = np.array([x,y,z,n]) 
    yyy = odeint(deriv0,yinit,t,args=(k1, k2))
    plt.figure(figsize=(7,5))
    plt.plot(t,yyy[:,0],"b-",label="no disease")
    plt.plot(t,yyy[:,1],"r-",label="have disease")
    plt.plot(t,yyy[:,2],"r-",label="have disease")


    plt.xlabel(u'time')
    plt.ylabel(u'population')
    plt.title(u'curve')
    plt.legend(loc=4)
    plt.show()
run(p1)
#%%
n0=2000
n=10000
k=0.000002
Y0=2000
t = np.arange(0,400,0.1)
y = (np.exp(k*n*t)*n*Y0)/(n-Y0+np.exp(k*n*t)*Y0)
y0 = (np.exp(k*n0*t)*n0*Y0)/(n0-Y0+np.exp(k*n0*t)*Y0)
plt.figure(figsize=(7,5))
plt.plot(t,y,"b-",label="with disease")
plt.plot(t,10000-y,"r-",label="no disease")

plt.xlabel(u'time')
plt.ylabel(u'population')
plt.title(u'model 1')
plt.legend(loc=4)
plt.show()
