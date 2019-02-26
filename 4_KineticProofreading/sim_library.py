
########################################
# This section of the file has a library of gates.
# They are:
# constDriver:
#	input: none
#	output: the node to drive
#	params: the value to drive to
# pwl:
#	no inputs
#	output: the node to drive
#	params: one list of time/concentration pairs. So [0 4 2 5] would imply
#	a concentration of 4 at t=0, 5 at t=2, interpolation for t in (0,2),
#	and a concentration of 5 for t>2.
# sin()
#	Implement out=A*sin(w*t)+B. Assume w is in radians/sec.
#	Parameters are A, w, B.
#	We currently do not use B; instead, we require that you use
#	add_reactant() to initialize appropriately.
# inv1(); a Hill-function inverter.
# buf1(): a Hill-function buffer
# "Implies" gate: out = !a | b.
# def imp1(t, inputs, outputs, params):
# constitutive(): no inputs; always drives the output with a slew rate of .05
########################################

# Drive a node to a constant value.
# Keep monitoring the node's current value and adjust accordingly.
# No inputs
# One output, which is the node to drive.
# One parameter, which is the desired constant output concentration.
def constDriver (t, inputs, outputs, params):
    checkInputs ('constDriver', 0,1,1, inputs, outputs, params)
    assert ((len(inputs)==0) and (len(params)==1) and (len(outputs)==1))
    desired = params[0]; current=outputs[0]
    return ([[], [desired-current]])

# Drive a node to a PWL sequence.
# One output, which is the node to drive.
# No inputs at all.
# The parameters are (t,concentration) pairs. So [0 4 2 5] would imply a
# concentration of 4 at t=0, 5 at t=2, interpolation for t in (0,2), and
# a concentration of 5 for t>2.
def pwl (t, inputs, outputs, params):
    import numpy as np
    checkInputs ('pwl', 0,1,44, inputs, outputs, params)
    # Split the parameter list into arrays of time and concentration.
    tt = np.array (params[0::2])
    yy = np.array (params[1::2])
    assert ((tt[0]==0) and (len(tt)==len(yy)))
    desired = np.interp (t, tt, yy)
    current=outputs[0]
    return ([ [], [10*(desired-current)] ])

# An inverter whose Vout-vs-Vin transfer curve is pwl.
def inv_pwl (t, inputs, outputs, params):
    import numpy as np
    checkInputs ('inv_pwl', 1,1,44, inputs, outputs, params)
    # Split the parameter list into arrays of Cin and Cout.
    Cin  = np.array (params[0::2])
    Cout = np.array (params[1::2])
    assert (len(Cin)==len(Cout))
    val = np.interp (inputs[0], Cin, Cout)
    delta = val - outputs[0]
    #print ('t=',t,': inv_pwl [in]=',inputs[0],', pwl=',val,"[out]'=",delta)
    return ([ [], [delta] ])

# Implement out=A*sin(w*t)+B
# Assume w is in radians/sec.
# Parameters are A, w, B.
# We currently do not use B; instead, we require that you use add_reactant()
# to initialize appropriately.
# I.e., we just return conc' = A*w*cos(w*t)
def sin (t, inputs, outputs, params):
    checkInputs ('sin', 0,1,3, inputs, outputs, params)
    A, w, B = params;
    return ([[], [A*w*cos(w*t)]])

# Hill-function inverter.
# TF = (in**n)/kDN
# out' = kP*kD/(kD+TF) - kDP*[out]
# Steady state when kP*kD/(kD+TF) = kDP*[out], or
#	[out] = (kP/kDP) * kD/(kD+TF)
#	So [in]=0   => TF=0   => [out]=kP/kDP
#	   [in]=inf => TF=inf => [out]=0
# [out] is half of its max when kD=TF, or kD=(in^n)/kDN, or in=(kD*kDN)^(1/n)
# Parameters are kP, kDP, kD, kDN, n.
# inputs are the input and output.
def inv1(t, inputs, outputs, params):
    checkInputs ('invHill', 1,1,5, inputs, outputs, params)
    kP, kDP, kD, kDN, n = params
    TF = (inputs[0]**n) / kDN
    return ([kP*kD/(kD+TF) - kDP*inputs[1]])
    #Ksw = (kDN*kD)**(1/n)
    #print('Inv1 kDN=',kDN,'kD=',kD,'Ksw=',Ksw)
    #print ('t=',t,': inv',Q in=',inputs[1], ',', '=',inputs[0],'*='

# TF = (in^n)/kDN
# out' = kP*TF/(kD+TF) - kDP*[out]
# SS when kP*TF/(kD+TF) = kDP*[out], or
#	[out] = (kP/kDP) * TF/(kD+TF)
#	So [in]=0   => TF=0   => [out]=0
#	   [in]=inf => TF=inf => [out]=kP/kDP
# [out] is half of its max when kD=TF, or kD=(in^n)/kDN, or in=(kD*kDN)^(1/n)
def buf1(t, inputs, outputs, params):
    checkInputs ('bufHill', 1,1,5, inputs, outputs, params)
    kP, kDP, kD, kDN, n = params
    TF = (inputs[0]**n) / kDN
    return ([kP*TF/(kD+TF) - kDP*inputs[1]])
    #Ksw = (kDN*kD)**(1/n); print('Buf1 kDN=#d,kD=#d,Ksw=#d\n', kDN,kD,Ksw)
    #print ('t=#d: buf #s in=#d, #s=#d, #s*=#d.\n', t, inputs(1),inputs(2),Q,out(1))

# "Implies" gate: out = !a | b.
def imp1(t, inputs, outputs, params):
    checkInputs ('impliesHill', 2,1,5, inputs, outputs, params)
    kP, kDP, kD, kDN, n = params
    TFa = (inputs[0]**n) / kDN
    TFb = (inputs[1]**n) / kDN
    return ([[], [kP*max(kD/(kD+TFa), TFb/(kD+TFb)) - kDP*outputs[0]]])
    # print ('t=#d: imp #s A=#d,B=#d,#s=#d, TFa=#d,P1=#d,TFb=#d,P2=#d,D=#d, #s*=#d.\n', t, inputs(1),inputs(2),Q,inputs(3),TFa,(kD/(kD+TFa)),TFb,(TFb/(kD+TFb)),(kDP*inputs(3)),Q,out(1))

# Always-on promoter.
def constitutive (t, inputs, outputs, params):
    checkInputs ('constitutive', 0,1,1, inputs, outputs, params)
    return ([.05])

def checkInputs (fName, nIn, nOut, nParam, In, out, param):
    if (nIn != len(In)):
        raise Exception ('Instance '+fName+' expects '+str(nIn)
                         +' inputs, but has '+str(len(In)))
    if (nOut != len(out)):
        raise Exception ('Instance '+fName+' expects '+str(nOut)
                         +' outputs, but has '+str(len(out)))
    if (nParam == 44):	# special case, means >=4 and even
        if ((len(param)<4) or (len(param)&1==1)):
         raise Exception ('Instance '+fName+' has '
                          +str(len(param))+' parameters, but wants an even'
                          +' number >=4')
    else:
        if (nParam != len(param)):
         raise Exception ('Instance '+fName+' expects '+str(nParam)
                         +' parameters, but has '+str(len(param)))