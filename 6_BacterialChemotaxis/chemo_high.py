
# The routines in this file implement bacterial chemotaxis at a high level.
# They are not an exact match for the reactions that scientists eventually
# discovered, but they are a proof of concept that chemotaxis *could* work
# using a simple memory and random swim.

import random
TIME_STEP = 1

# The routine that implements high-level chemotaxis
# It is just an implementation of the algorithm we discussed in class.
def chemotaxis():
    x = y = 0
    concOld = sample (x,y)
    Vx, Vy = pick_random_direction()
    print ("Initially: x=",x,', y=',y, ", conc=", concOld)
    for i in range(200):
        x,y = swim (x,y, Vx, Vy)
        concNew = sample (x,y)
        print ("Swam to [{:.2f},{:.2f}], where distance={:.2f} and [sugar]={:f}".format (x,y,(x-50)**2 + (y-50)**2,concNew))
        if (concNew <= concOld):
            Vx, Vy = pick_random_direction()
        concOld = concNew
display()

# Pick a random direction and return it.
# The random direction is an (x,y) pair. It is always normalized such that
# x*x + y*y = 1.
# To be precise, we're picking a velocity vectory. However, the swimming speed
# will always be one, so we're really only picking the direction.
def pick_random_direction():
    # First pick the x and y components of the direction.
    x = random.uniform(-1,1)
    y = random.uniform(-1,1)

    # Now normalize to have magnitude=1.
    adj = 1 / ((x*x + y*y)**.5)
    print ("new direction: x={:.3f}, y={:.3f}".format(x*adj, y*adj))
    return (x*adj, y*adj)

# Swim for one TIME_STEP at Vx,Vy (which we got from pick_random_direction()),
# and return the new x,y location.
# You call it as follows:
#        x,y = swim (x,y, Vx, Vy)
# Note that swim() saves away the bacteria's path so that we can make an
# animated movie later.
def swim (x, y, Vx, Vy):
    x = x + Vx*TIME_STEP
    y = y + Vy*TIME_STEP
    newPoint (x,y)	# save away the E.coli's path
    return (x,y)

# Return the sugar concentration at any [x,y] location.
# Our field has sugar at x=50, y=50.
# It then tails off slowly around that.
def sample (x,y):
    distance = (x-50)**2 + (y-50)**2	# Actually distance**2, but that's fine
    distance = max (distance, 1)	# To avoid /0 if x,y=(50,50)
    return (10/distance)		# So small distance => return big number

###############################################################
# This part of the file deals with showing an animated movie of our chemotaxis.
# It is based on Python's matplotlib package (which does all kinds of plotting),
# and specifically on the matplotlib.animate package (which focuses on
# animation).
###############################################################

# Declare global variables to save away the path that our EColi followed.
# Then display() will make it into a movie.
def display_setup():
    global saveX, saveY
    saveX = []	# SaveX and saveY are each arrays, with the same length
    saveY = []	# So saveX[i] and saveY[i] form one (x,y) coordinate.

# Save away a new point that we just swam to.
def newPoint (x,y):
    global saveX, saveY
    saveX.append(x)
    saveY.append(y)

# The top-level animation function.
def display():
    # First, create a figure to draw on; with axes, etc.
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import matplotlib.animation as animation
    fig, axes = plt.subplots()
    xmin=0; xmax=1; ymin=0; ymax=1
    axes.axis ([xmin,xmax,ymin,ymax])	# Set the axes to range from [-1,1].
    axes.set_autoscale_on(False)	# Make sure they stay at [-1,1].

    # Create/draw the sugar object in the middle. It never moves.
    axes.add_patch (patches.Circle ((.5,.5), radius=.03, facecolor='r'))

    # Now create the bacteria icon (which will move around)
    global pat, nInterps	# To communicate with per_frame()
    pat = patches.Rectangle ((0,0),.03,.03, facecolor='b')
    axes.add_patch (pat)

    print ("Starting animation")
    # Note that FuncAnimation is an *object*, so we must assign it to something
    # "blit=True" is a trick that makes the animation run fast. It says to
    # draw the axes and the sugar once only, and then in every frame just
    # redraw the EColi.
    nInterps=4		# Numb of interpolated frames between each saveXY point
    nFrames = (nInterps+1)*(len(saveX)-1)
    ani = animation.FuncAnimation(fig, per_frame, frames=nFrames,
                                  interval=1, blit=True, repeat=False)
    print ("Finished animation")
    plt.show()

# Our per-frame animation function. It takes the frame number and returns a
# list of objects that have moved (in fact there is only one; the EColi).
# It also must update those object(s), which we do with the pat.set_x and set_y.
#
# The hard part is figuring out where to draw the bacteria.
# Consider 3 data items and nInterps=4.
# Then frame #0 is data[0]; #1-4 mix [0] and [1]; #5 is data[1]; #6-9
# mix [1] and [2], and #10 is data[2], with 11 frames total.
def per_frame(f):
    global pat, saveX, saveY, nInterps
    recip = 1/(nInterps+1)
    i0 = int (f*recip+.00001)
    alpha = (f - i0*(nInterps+1)) * recip
    x = saveX[i0] + (saveX[i0+1]-saveX[i0])*alpha
    y = saveY[i0] + (saveY[i0+1]-saveY[i0])*alpha
    #print ("Animating frame #",f,"->",x,y)
    pat.set_x (x/100 - .015)    # x/100 is the rectangle's center; -.015 
    pat.set_y (y/100 - .015)    # gets you the lower-left corner.

    return [pat]	# Always return a list of the changed items.

random.seed(0)
display_setup()
chemotaxis()