# This function returns the distance covered by Manduca's head.
# Inputs:
#	Two 10-row matrices; each row is one of the 10 time segments.
#	- 'muscles' is a 10x4 matrix of muscle forces; all entries are 100 or 0
#	- 'legs' is a 10x5 matrix of legs locked. 1 means locked, 0 means not.
#	- 'record': if 0 or not supplied, then no recording.
#	  If 1, then save the end-of-time-segment values to a file.
#	  If 2, then save all values to a file.
# Returns:
#	- the distance covered by the center of mass.
#	- result_details: 10x7 matrix, with one row per timepoint (i.e., at
#	  t=10,...,90,100). The first 5 columns are the positions of the 5 legs.
#	  Then the COM position and velocity.
#
# The system is just 5 legs & 4 springs+muscles; there is no intrinsic
# difference between the head and the tail. However, since we start in the
# position leg #0 x=0 and leg #4 x=2000, then it makes sense to call leg #4
# the head. This means that increasing x values correspond to moving the head
# forwards.
def manducaFitness(legs, muscles, record=0):
    # Error checking our input parameters.
    nTimeSeg = legs.shape[0]	# Number of time segments (usually 10).
    # assert (nTimeSeg == 10)	# Comment this out if desired.
    assert (legs.shape == (nTimeSeg,5))		# 10 time slots x 5 legs.
    assert (muscles.shape == (nTimeSeg,4))	# 10 time slots x 4 muscles.
    assert (((legs==1)|(legs==0)).all())	# Legs are 1 or 0
    assert (((muscles==0)|(muscles==100)).all())#Musc 0 or 100

    # If we are told to record, then open the output file to record into.
    if (record>0):
        fileID = open_outfile()
    resultDetails=np.zeros((nTimeSeg,7))	# Allocate debug-return matrix.

    # Prepare to loop. First set up the time steps.
    tpts = np.linspace (0, 100, nTimeSeg+1)	# 1x11 vector of timepoints

    # Initialize the running initial-state vector for each mini-sim
    x0 = np.array([0,500,1000,1500,2000])	# Positions of the 5 legs at t=0
    xprime0 = np.zeros((5))			# Velocities "  "     "

    # The distance covered by Manduca will be the difference between the head
    # of Manduca (at x=2000) at t=0 vs. t=100.
    manducaCOM_T0 = np.mean (x0);		# Location of the COM at t=0

    # The main simulation loop.
    for i in range(tpts.size-1):		# For each time interval.
        # Set globals to communicate the leg-frozen & muscle-force choices to
        # odeSlopes(). Its function parameters are just the integration
        # variables (leg positions & velocities)
        global muscRow, legLockedRow
        legLockedRow=legs[i,:]	# 1x5 vector of legs locked for this interval
        muscRow = muscles[i,:]

        # See the odeSlopes() header for why we must force derivatives to 0.
        # The code in odeSlopes() does this job during the simulation; the code
        # right here does it for the first timestep of any mini-sim.
        for ll in range(5):
            if (legLockedRow[ll]):
                xprime0[ll]=0

        # Divide each simulation interval into 10 visible timepoints for debug
        tptsD=np.linspace(tpts[i],tpts[i+1],11)
        initVals = np.hstack ((x0, xprime0))

        # odeint returns an array with one row per requested timepoint, one
        # column per variable
        from scipy.integrate import odeint
        x = odeint (odeSlopes, initVals, tptsD)

        # The final row gives the values at the end of the simulation interval.
        # We use them to make 5-element vectors for position & velocity of the
        # 5 legs, to use as initial conditions for the next time interval.
        x0 = x[-1,0:5]			# position of the 5 legs at sim end
        xprime0 = x[-1,5:]		# velocity of ""

        # Save our end-of-sim results for this segment.
        if (record > 0):
            start = (0 if (record==2) else t.size-1)
            for r in range(start,tptsD.size):
                s = '{},  {},{},{},{},{}, {},{},{},{},{}, {},{},{},{}\n'.format(
                    tptsD[r], x[r,0],x[r,1],x[r,2],x[r,3],x[r,4],
                    legLockedRow[0],legLockedRow[1],legLockedRow[2],
                    legLockedRow[3],legLockedRow[4],
                    muscRow[0],muscRow[1],muscRow[2],muscRow[3])
                fileID.write (s)
        resultDetails[i,0:5] = x[-1,0:5]	# Final lumped-mass positions
        resultDetails[i,5] = np.mean(x[-1,0:5])	# COM position
        resultDetails[i,6] = np.mean(x[-1,5:10])# COM velocity
    # end of for each of the 10 timepoints.

    # 'x0' is left over from the final simulation interval. We grab the final
    # position of the COM to compute the distance traveled.
    COM_distance = x0.mean() - manducaCOM_T0

    if (record>0):
        fileID.close()
    return ((COM_distance,resultDetails))

# The ODE-implementation function odeSlopes(), which gets passed to odeint().
# Inputs:
#	- 'x' is a 10x1 column vector of the variables at time 't'.
# Outputs:
#	- 'xprime', a 10x1 column vector of the first derivatives (i.e., slopes)
# The first 5 variables are leg position; then next 5 are leg velocity.
#
# odeSlopes() is given the current values of all of the variables, and must
# return their slopes. There are two tricks:
# 1. The real inputs to our system are the muscle and viscous-body forces on the
#    body segments; the outputs we want are the body-segment positions. So this
#    is f=ma -- but acceleration is x'', not x'. Thus we not only have 5 x
#    variables, but also introduce 5 more variables v. At each timestep, we
#    look at the body-segment positions to determine their stretch and thus get
#    the forces on them. This gives us the acceleration, which is the desired
#    derivatives v' for our 5 'v' variables. We then merely copy x'=v to get the
#    5 derivatives of the 'x' variables.
# 2. While it's easy to calculate the forces from muscles and from viscous
#    damping, that still leaves the ground reaction forces on the legs. If a
#    leg is unlocked, then it has no friction, and all is easy. If a leg is
#    locked, however, then the ground reaction force is harder to calculate.
#    We avoid this by merely noting that in this case, we must have the leg's
#    v=0 and x=constant. We force this into the derivatives separately.
#
# Here's more detail on the f=ma equations.
# In this intuitive description, we'll call the ten variables x1-x5 and v1-v5.
# Note the viscous-damping terms work in the same direction as the Hookian
# terms. So if you stretch a spring very quickly, it fights back more. Real-life
# metal springs don't do this much, but most real-life biomaterials do. Since
# our spring is really soft tissue, it makes sense to give it visco-elasticity.
#	v0' = (k(x1-x0-L0) + c(v1-v0) + M01)/m
#	v1' = (k(x2-x1-L0) - k(x1-x0-L0) + c(v2-v1) + c(v0-v1)+ M12-M01)/m
#	v2' = (k(x3-x2-L0) - k(x2-x1-L0) + c(v3-v2) + c(v1-v2)+ M23-M12)/m
#	v3' = (k(x5-x3-L0) - k(x3-x2-L0) + c(v4-v3) + c(v3-v3)+ M34-M23)/m
#	v4' =              (-k(x5-x3-L0)            + c(v4-v4)     -M34)/m
def odeSlopes(x, t):
    c = 2;	# Viscosity constant.
    m = 1;	# Mass.
    k = 1;	# Elastic spring constant.
    L0 = 500;	# Resting spring length.
    global muscRow, legLockedRow

    # Use more intuitive names for the muscles. So M01 is the muscle between
    # the rearmost two legs
    (M01, M12, M23, M34) = muscRow

    # Derivative of the position is just the velocity
    xprime = np.zeros(10)
    xprime[0:5] = x[5:10]

    xprime[5]= (1/m) * (-k*x[0] + k*x[1] - c*x[5] + c*x[6] - k*L0 + M01)

    xprime[6]= (1/m) * (-k*x[1] + k*x[2] - c*x[6] + c*x[7] - k*L0 + M12 + \
                         k*x[0] - k*x[1] + c*x[5] - c*x[6] + k*L0 - M01)

    xprime[7]= (1/m) * (-k*x[2] + k*x[3] - c*x[7] + c*x[8] - k*L0 + M23 + \
                         k*x[1] - k*x[2] + c*x[6] - c*x[7] + k*L0 - M12)

    xprime[8]= (1/m) * (-k*x[3] + k*x[4] - c*x[8] + c*x[9] - k*L0 + M34 + \
                         k*x[2] - k*x[3] + c*x[7] - c*x[8] + k*L0 - M23)

    xprime[9]= (1/m) * ( k*x[3] - k*x[4] + c*x[8] - c*x[9] + k*L0 - M34)

    for i in range(5):
        if (legLockedRow[i]):
            xprime[i] = xprime[i+5] = 0

    np.set_printoptions (formatter={'float': '{: 6.3f}'.format}, linewidth=100)
    #print ('OdeFunc: t=', t, ', locked=', legLockedRow, ', musc=', M01, M12, M23, M34)
    #print ('       x=', x[0:5], "*", x[5:10])
    #print ("       x'=", xprime[0:5], "*", xprime[5:10],'\n')
    return (xprime)

def open_outfile():
    full_name = 'manduca_output_long.txt'

    ##from subprocess import check_output
    ##cmdout = check_output ('whoami', universal_newlines=True)
    ### print ('cmdout=', cmdout)

    ### Windows will return something like "joel\joelg\n" for domain\username.
    ### Unix just returns "joelg\n"
    ##from re import search
    ##slash = search('\\\\', cmdout)
    ##if (slash):
    ##    # We're on Windows.
    ##    # On the EECS lab systems, the domain will be 'hlgn'.
    ##    domain = cmdout [1:slash.start()]
    ##    user = cmdout [slash.start()+1:-1]	# Remove the final '\n'.
    ##    dir = ('q:\\es93CD\\2016f\\manduca_outputs\\' if (domain=='hlgn') \
    ##            else ('c:\\Users\\'+user+'\Documents\\'))
    ##else:
    ##    # We're on Unix
    ##    dir='/h/joelg/courses/python/manduca'
    ##    user = cmdout[0:-1]	# Remove the final \n
    ##full_name = dir+'/manduca_output_'+user+'.txt'

    print ('Recording to file', full_name)
    fileID = open(full_name,'w')
    fileID.write ('Time x_leg1 x_leg2 x_leg3 x_leg4 x_leg5 lock1..5 musc1..4\n')
    return (fileID)

import numpy as np