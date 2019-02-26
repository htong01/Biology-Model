
########################################
# Useful functions from the simulation-infrastructure package
# clear_sim()
#	Clears away the entire simulation network and results
# add_metab (metabName, initVal)
#	Declare a metabolite and its value at time=0.
#	All metabolites must be declared before giving them to add_reaction().
# add_reaction (reacFunc, reacName, inputs, outputs, params):
#    Declare a new reaction. The inputs are:
#	reacFunc: name of the function that implements this reaction
#	reacName: a string, just for debugging.
#	inputs: vector of names for the reactants.
#	outputs: vector of names for the products (there can be more than one).
#	parameters: vector of double for the instance parameters.
# run_sim (tEnd, n_timepoints=10):
#	Run a simulation from t=0 to t=tEnd.
#	Return:
#	- a 1D array of timepoints, containing n_timepoints evenly-spaced
#	  values of time between 0 and tEnd (so if tEnd=2 and n_timepoints=5,
#	  then it returns [0, .5, 1, 1.5, 2].
#	- a 2D array of simulation results. Each row corresponds to one of the
#	  above timepoints; each column corresponds to one reactant.
# run_xfer_curve (inName, Cmax,outName, sideInputNames,sideInputVals,nPoints)
#	Computes a transfer curve. It sweeps the reactant 'inName' from 0 to
#	'Cmax', and measures the resulting concentration of the product
#	'outName'. You can also specify a vector of other reactants
#	'sideInputVals' to hold constant to the associated values
#	'sideInputVals.
#	It returns two values:
#	- a 1D array of the values 'inName' we evaluated at (i.e., 'nPoints'
#	  evenly-spaced concentrations between 0 and 'Cmax'
#	- a 1D array of the corresponding values of 'outName'.
# steady_state_sim (tEndGuess)
#	Simulates the current network until all metabolite levels are reasonably
#	steady. You must have already used add_metab() to set any initial
#       conditions and/or driving input reactants as needed.
#	Steady_state_sim() returns three values:
#	- the time it needed to simulate to before reaching steady state. It
#	  first tries simulating to tEndGuess; but will also simulate up to
#	  1000 times longer if needed.
#	- a vector of the final concentrations for every metabolite.
#	- a Boolean, telling whether we ever did reach steady state. If we
#	  simulate until 100*tEndGuess and the metabolite levels are still
#	  changing, we give up and return false.
# final_val (y, metabolite):
#	Given the integration results from run_sim(), return the final value of
#	a given metabolite (given by its name).
########################################

# The global variables:
#	g_metabs:		list of metabolite-name strings.
g_metabs = []

#	g_metab_initVal:	list of metabolite initial values.
g_metab_initVal = []

#	g_reactions:		list of reactions. Each is an object
#		.reac=function, .name=string, .inputs=list[int],
#		.outputs=list[int], .params=list[double].
g_reactions = []

# Whichever reaction function (if any) is currently executing.
g_current_reaction=None

# One object per reaction instance.
class Reaction:
    func=0	# The function that handles this reaction
    name=""	# Name of this reaction
    inputs=[]	# All reactants
    outputs=[]	# All products
    params=[]	# self.reac may be a simple, generic reaction function, that
        	# needs parameters (e.g., reaction velocities)
    memory=None	# a slot that the user can use if desired
    def __init__ (self, F, N, I, O, P):
        self.func=F; self.name=N; self.inputs=I; self.outputs=O; self.params=P

def clear_sim():
    global g_metabs, g_metab_initVal, g_reactions;
    g_metabs=[]; g_reactions=[]; g_metab_initVal=[];

# All metabolites must be declared here before using them in add_reaction().
def add_metab (r, init):
    if (not (type(r) is str)):
      raise Exception('Metabolite '+r+' given to add_metab() must be a string')

    global g_metabs, g_metab_initVal;
    g_metabs.append (r)
    g_metab_initVal.append (init)

# def add_reaction()
#    Declare a new reaction. The inputs are:
#	reac: pointer to the reaction def.
#	reaction name: a string, just for debugging.
#	inputs: vector of names for the reactants.
#	outputs: vector of names for the products (there can be more than one).
#	parameters: vector of double for the instance parameters.
def add_reaction (reacFunc, name, inputs, outputs, params):
    global g_reactions, g_metabs;

    if (not (type(inputs) is list)):
        raise Exception ('Inputs to reaction '+name+' must be a list')
    if (not (type(outputs) is list)):
        raise Exception ('Outputs to reaction '+name+' must be a list')
    if (not (type(params) is list)):
        raise Exception ('Params to reaction '+name+' must be a list')

    # convert reactant names to indices into g_metabs[].
    reac_idxs=[]
    for reac in inputs:
        reac_idxs.append (metab_number (reac));

    prod_idxs=[]
    for prod in outputs:
        prod_idxs.append (metab_number (prod));

    r = Reaction (reacFunc, name, reac_idxs, prod_idxs, params)
    g_reactions.append (r)

# Given the name of a metabolite, find its index in g_metabs.
def metab_number (name):
    global g_metabs
    try:
        return (g_metabs.index (name))
    except:
        raise LookupError ('** There is no metabolite named ' + name +'**')

# Run a simulation from t=0 to t=tend.
# Return a 1D array of timepoints and a 2D array of results
def run_sim (tend, n_timepoints=10):
    import numpy
    import scipy.integrate
    global g_metabs, g_metab_initVal

    # array with n_points points evenly space between 0 and tend.
    timePts = numpy.linspace (0, tend, n_timepoints)

    # odeint inputs:
    #   - function that we supply, which must return state-variable derivatives
    #   - initial values of state variables (and the size of this 1D array tells
    #     odeint how many state variables there are).
    #   - an array of the times when we want the DFQ solved.
    # odeint outputs: just one, a 2D array with
    #   - one row per requested timepoint 
    #   - one column per metabolite
    y = scipy.integrate.odeint (reactions_func, g_metab_initVal, timePts)

    #print ('t=', timePts)
    #print ('y=', y)
    return (timePts, y)

# The function that gets passed to scipy.integrate.odeint(), and gives it all
# of the derivatives at time t.
# Inputs:  'y' is a column vector of the variables at time 't'.
# Outputs: 'yprime', a column vector of the first derivatives.
def reactions_func (y, t):
    # Zero the vector of rates, so that each reaction can accumulate its output
    # rates into the vector.
    global g_reactions, g_metabs, g_current_reaction
    import numpy
    assert (y.size == len(g_metabs))
    yprime = numpy.zeros (y.size)

    for r in g_reactions:
        g_current_reaction = r	# for write_my_space() below.

        # Prepare inputs[]; the current values of this reaction's reactants.
        inputs = numpy.zeros (len(r.inputs))
        for i in range(len(r.inputs)):
            inputs[i] = y [r.inputs[i]]

        # Ditto for outputs[]
        outputs = numpy.zeros (len(r.outputs))
        for i in range(len(r.outputs)):
            outputs[i] = y [r.outputs[i]]

        # Call the actual reaction function. It returns a list of d(product)/dt;
 	# i.e., how fast it slews each of its products. In fact, it returns one
        # list for inputs and one for outputs, since chemical reactions consume
        # their inputs as well as produce outputs.
        in_slews,out_slews = r.func (t, inputs, outputs, r.params)

        # Sum its d(product)/dt into the total metabolite d/dt.
        assert (len(out_slews) == len(r.outputs))
        for idx,met_idx in enumerate(r.outputs):
            yprime[met_idx] += out_slews[idx]

        # Ditto for the input slew rates.
        if (in_slews != []):
            assert (len(in_slews) == len(r.inputs))
            for idx,met_idx in enumerate(r.inputs):
                yprime[met_idx] += in_slews[idx]

        if (False):
            print ('t=',t, 'reaction', r.name, ': input concs ', end='')
            for idx, met_idx in enumerate(r.inputs):
                print (g_metabs[met_idx], '=', y[idx], end='')

            print ('; output slews ')
            for idx, met_idx in enumerate(range(r.outputs)):
                print (g_metabs[met_idx], '=', y[idx], end='')
            print ('')

    return (yprime)

# Compute a transfer curve.
# Inputs:
#	inName, Cmax, outName: sweep the main input inName from 0 to Cmax
#		and measure the response at outName.
#	sideInputNames, sideInputVals: lists of the names of side inputs and
#		the concentrations to hold them steady at.
#	nPoints: the number of evenly-spaced points to evaluate inName at.
# Outputs: vectors on x & y values for the transfer curve; each is n_points x 1.
# Operation:
#	At each sample point, the function creates constant sources to drive
#	the inputs and then runs a simulation 
def run_xfer_curve (inName, Cmax,outName, sideInputNames,sideInputVals,nPoints):
    import sim_infrastructure as si
    import sim_library as sl
    import numpy as np
    global g_reactions;

    # Run the sims until this max time.For now, just use a constant.
    tMax = 100

    # Drive the side inputs with the desired constant values.
    assert (len(sideInputNames) == len(sideInputVals))
    for idx,name in enumerate(sideInputNames):
        si.add_reaction (sl.constDriver,name, [],[name], [sideInputVals[idx]])

    # Drive the main input with another constant (we will keep changing its
    # actual value on the fly).
    si.add_reaction (sl.constDriver,inName, [], [inName], [0]);

    # Now do the xfer curve points, one sim at a time
    out_numb = metab_number (outName)
    xVal = np.linspace (0, Cmax, nPoints).tolist()	# input values
    yVal = []		# will get filled with output values
    for x in xVal:
        # The final reaction added was our main input. Drive its value now.
        g_reactions[-1].params[0] = x
        tMax,y,OK = steady_state_sim (tMax)
        assert (OK)
        yVal.append (y[-1,out_numb])	# i.e., the desired output's final value

    return (xVal,yVal)

# Run until all variables are pretty steady.
# However, some systems never reach any steady state, so detect that if needed
# Return a tuple (t, y, OK)
def steady_state_sim (tEndGuess):
    tEnd = tEndGuess/2
    done = False
    OK = True
    while (not done):
        if (tEnd > tEndGuess*1000):
            print ('Simulation did not converge at t=', tEnd)
            return (t,y,False)

        tEnd = tEnd*2	# Try a longer sim.
        t,y = run_sim (tEnd, 100)

        done = True
        n_react = (y.shape) [1]
        for i in range (n_react):	# For each column... i.e., each metab
            x1=y[90,i]; x2=y[99,i]
            done = done and ((max(x1,x2)<.001) or (abs(x2-x1)/max(x2,x1) < .01))
    return  (tEnd, y, True)

# Given the integration results from a simulation, return the final value of
# a given metabolite (given by its name).
def final_val (y, metab):
    return (y [-1, metab_number (metab)])

########################################
## Functions for a reaction instance to save private data & get it back later
## They rely on the fact that reactions_func() always uses g_current_reaction
## to let us know which reaction is currently being evaluated.

def write_my_space (memObj):
    global g_current_reaction
    r.memory = memObj

def read_my_space (memObj):
    global g_current_reaction
    return (r.memory)

########################################
## Functions to implement memory of past state (e.g., a delay line).
## I.e., save away time-stamped data and then retrieve it
## They maintain and use a list of TimeStampedData objects; each one has a time
## stamp 't' and some data.
## We assume that the objects are always in time-stamp order.
class TimeStampedData:
    t=0
    data=None
    def __init__ (self, T, D):
        self.t=T; self.data=D

def save_state_time (t, newData, memObj, how_long=10000000):
    assert (t > memObj[-1].t)		# Check that time stamps are in order
    memObj.append (TimeStampedData (t, newData))	# add the new data
    while (memObj[0].t < t-how_long):			# delete any old data
        del memObj[0]

# Find the item whose time stamp is closest to 't' and return it.
def get_state_time (t, obj):
    for obj in memObj:
        if (obj.t > t):
            break
        bestObj = obj
    return (obj if (obj.t-t < t-bestObj.t) else bestObj)