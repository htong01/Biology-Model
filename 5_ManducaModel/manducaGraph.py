# manducaGraph
# This function animates a beautiful movie of one or more Manducas racing along.
# It works from a file that has saved data from a prior simulation run.
#
# Inputs:
#	mode: -	0 means display each file as a horizontally-moving worm;
#		one file (i.e., one worm) per line in the movie. In this
#		case, 'arg' is how many seconds the full movie should last and
#		'varargin' is an alternating list of (the name of a file of
#		worm data, followed by a label for that worm).
#	      - 1 means display one worm only, but display it as a sequence
#		of 'arg' stills, one over the other. In this case, 'varargin'
#		is the name of exactly one file of worm data.
#	arg, varargin: as indicated above.
# A common call might then be
#	manducaGraph (0, 20, 'C:\users\johnM\matlab\graph1.txt', 'Slow worm',
#			     'C:\users\johnM\matlab\graph2.txt', 'Fast worm');
# This would display both worms (one from graph1.txt and one from graph2.txt)
# racing against each other. The two animated worms would be labeled
# 'Slow worm' and Fast worm'.
#
# Another common call might be
#	manducaGraph (1, 20, 'C:\users\johnM\matlab\graph1.txt')
# This would take the worm-motion data from graph1.txt, pull out 20 stills at
# evenly-spaced times, and display them.
#
# The worm-data files are typically produced by manducaFitness(), which can
# be told to save all simulation data into a file.

# Constants.
FPS = 30		# frames per second.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

def manducaGraph (mode, arg, *rest):
    global points
    # Build points[n_frames,15,n_worms]
    # The 2nd dimension is 15: t, 5 x values, 5 leg_locked and 4 muscle_on.
    # The 3rd dimension is always the number of worms to draw one above another.
    # The 1st dimension is the number of frames to time-sequence for each worm.
    if (mode==0):		# video of one or more worms racing.
        # Read the file(s) and build points[n_frames][15 items][n_worms]
        wall_time = int(arg)
        n_frames = 1 + wall_time*FPS
        if (len(rest) & 1 != 0):
            raise Exception ('Missing label name for file')

        n_files = len(rest)//2
        labels = [rest[2*f+1] for f in range(n_files)]
        points = np.empty ((n_frames,15,n_files))
        for f in range(n_files):
            points[:,:,f] = read_file (rest[2*f], n_frames)
    elif (mode==1):		# a few stills of one worm.
        # In this mode, we just read one file of data (from one worm).
        # Then we extract 'n_stills' evenly-spaced stills from it to
        # build points[1][15 items][n_stills].
        n_stills = arg
        points = np.empty ((1,15,n_stills))
        pts = read_file (rest[0], n_stills)
        # We now take our N frames, extracted from one worm over time, and
        # pretend that they are 1 frame each from N worms. That will result in
        # a sequence of N stills.
        for st in range(n_stills):
            points[:,:,st] = pts[st,:]
        labels = ['t='+str(100*st/(n_stills-1)) for st in range(n_stills)]
    else:
        raise Exception ('Illegal mode: must be 0 or 1')

    # We now have points[n_display_timepoints][15][n_worms]. Run the movie.
    display (points, labels)

# Inputs:
#     -	file: a filename. The file has one line per simulation timepoint.
#	Each line is comma-separated values with the format
#	time, x1,x2,x3,x4,x5, lock1...lock5, musc1...musc5
#     - n_frames: the number of frames to return. So if the file contains data
#	from t=0 to t=100 and we want to return 3 frames, then we will sample
#	every 50s of simulated time.
# Return a 2D array where row #i is the simulation data at frame #i.
# So the first row is for t=0. The last row is for the simulation end time 
# which is always t=100).
# The returned array has the same number of columns (with the same meaning) as
# the simulation file.
def read_file (file, n_frames):
    print ('Sampling file', file, 'to create',n_frames,'frames.')

    # Read the file, starting at the 2nd line (the top line is a comment).
    # Now we have an array where each line is
    #	(time, x1,x2,x3,x4,x5, lock1...lock5, musc1...musc5)
    with open (file, 'r') as fp:
        lines = fp.readlines() # one list item per line.
        # The top line is just a comment
        del lines[0]
        n_rows = len(lines)
        n_cols = len(lines[0].split(','))
        # Do a double-nested list comprehension to get the data.
        pts_list = [[float(val) for val in line.split(',')] for line in lines]
        raw = np.array (pts_list)

    # Sanity check that we have 15 columns.
    assert (raw.shape[1] == 15) # time, x1-5, 5 lock values, 4 muscles.
    # Sanity check that the leg-lock values are all 0 or 1.
    assert ((raw[:,6:11]==0) | (raw[:,6:11]==1)).all()
    # And the muscle values are all 0 or 100.
    assert ((raw[:,11:15]==0) | (raw[:,11:15]==100)).all()

    # How often must we sample to get n_frames frames?
    # Note the .00001; we want to ensure that the final value of desired_t below
    # is not actually *bigger* than raw[-1,0]; that would make us skip the last
    # point
    t_final = raw[-1,0] - .00001
    interval = t_final/(n_frames-1)

    # Now do the interpolation.
    # Note that the file may occasionally have such small timesteps that,
    # when we print out with finite precision, it seems like two consecutive
    # rows share the same time. The algorithm below is robust to that.

    # It should always be true that desired_t = interval * (points_row-1).
    desired_t = 0		# The timepoint we want numbers for.
    points_row = 0		# We will put this row in points(points_row,:).

    # The big picture: this loop keeps stepping through 'raw' until desired_t
    # is in [row r.time, row r+1.time]. Then it interpolates to find the data at
    # desired_t (and any other desired timepoints that are also in the interval)
    # The first time around the loop, desired_t=0 and the interval really is
    # closed on the left; afterwards, it is always (].
    # At the bottom of this loop, we will always have desired_t > raw[r+1].time,
    # since we will have kept incrementing desired_t until it is out of the
    # interval.
    points = np.empty((n_frames,15))
    for r in range(raw.shape[0]-1):	# For every row pair (r,r+1)
        time1 = raw[r,0]		# timepoint for this table row
        time2 = raw[r+1,0]		# timepoint for the next table row
        while (desired_t <= time2):
            inter = interpolate(raw,r,desired_t)
            points[points_row,:] = interpolate(raw,r,desired_t)
            desired_t += interval
            points_row += 1
    return (points)

# Given:
#	- raw: an array of (time, x1,x2,x3,x4,x5,lock1...lock5) for all
#	  timepoints that were integration timesteps.
#	- t: the timepoint we really want.
#	- r: says where to find t=next_interval in 'raw'.
# Assume that the desired time 't' obeys raw(r,1)<= t <= raw(r+1,1).
# Perform linear interpolation based on that time and return a full 15-element
# row vector where:
#	- [0] is the desired time 't'
#	- [1:5] are the interpolated 'x' positions of the five body segments.
#	- [6:10] are the lock conditions from raw(r,6:10)
#	- [11:14] are the muscles from raw(r,11:14).
def interpolate (raw,r,t):
    ###print ('Interpolating row',r,'and',r+1,'for time=',t)
    assert ((raw[r,0]<=t) & (raw[r+1,0]>=t))
    frac = (t-raw[r,0])/(raw[r+1,0]-raw[r,0])
    # Interpolate the X values (1:5). Also interpolate time as a sanity check.
    points = np.empty((15))
    points[0:6] = raw[r,0:6] + frac*(raw[r+1,0:6]-raw[r,0:6])
    assert (abs (points[0]-t) < .0001)

    # The leg-lock values just get dragged along.
    points[6:15] = raw[r,6:15]		# Leg-lock values & muscles.

    # Very occasionally, the Matlab ODE solver will squish the worm so much that
    # a front leg gets pushed behind a back leg! Fix that here -- we really
    # should fix the ODEs instead :-(, but I've not gotten around to debugging
    # it.
    for i in range (2,6):
        points[i] = max (points[i-1],points[i])
    return (points)

############################################################
# The rest of the file is for window display
############################################################

# Set up the plot window.
# We create axes, scaled so that:
#	* x ranges over the min/max x values from the simulation.
#	* y ranges from 0 to n_worms; i.e., each worm is allocated a vertical
#	  space of 1.
def display (points, labels):
    n_worms = points.shape[2]
    print ('making',n_worms,'worms')

    # Get min & max value in 'points'. Make sure to only min/max over the X
    # values (i.e., columns 1:5), not the leg-locks & muscles.
    x_min = np.min(points[:,1:6,:])
    x_max = np.max(points[:,1:6,:])

    # Set up the figure and its axes.
    fig,axes = plt.subplots()
    axes.axis ([x_min,x_max,0,n_worms])
    axes.set_autoscale_on(False)
    # print ('x limits=', axes.get_xlim(), ', y limits=', axes.get_ylim())

    draw_labels (labels, axes)		# Label each worm with text on the left
    init_pats(n_worms, axes)		# Create all of the moving shapes

    msecPerFrame = 1000/FPS
    ani = animation.FuncAnimation(fig, per_frame, frames=points.shape[0],
                                  interval=msecPerFrame, blit=True,
                                  repeat=False)
    print ("Finished animation")
    plt.show()

# Create all of the rectangles that make up the legs and body segments for all
# of the worms. Just put them anywhere at all; per_frame() will move them.
# Each worm has:
# - 5 legs. A leg is a single vertical rectangle.
# - 4 body segments. Each one is a horizontal rectangle (perhaps with a bit of
#   curvature), as well as a horizontal line in it if the segment's muscle is on
# We keep all of these objects in
# - Legs[5][n_worms]
# - BodySegs[4][2][n_worms]. For this, [*][0][*] is the main-segment rectangle,
#   and [*][1][*] is the corresponding muscle-on band.
def init_pats(n_worms, axes):
    global legs, bodySegs, allPatches
    legs = np.empty ((5, n_worms), dtype=object)
    bodySegs = np.empty ((4, 2, n_worms), dtype=object)

    for w in range(n_worms):
        for l in range(5):	# Build the red legs
            pat = patches.Rectangle ((0,0),.1,.1, facecolor='r')
            axes.add_patch (pat)
            legs[l][w] = pat

        for bs in range(4):
            pat = patches.Rectangle ((0,0),.1,.1, facecolor='g')
            axes.add_patch (pat)	# Green body segments
            bodySegs[bs][0][w] = pat
            pat = patches.Rectangle ((0,0),.1,.1, facecolor='k')
            axes.add_patch (pat)	# Black muscle-on bands
            bodySegs[bs][1][w] = pat

    # Collect up all of the rectangles into one big list, so that per_frame()
    # can return the list.
    allPatches = [legs[l][w] for l in range(5) for w in range(n_worms)]
    bs = [bodySegs[bs][0][w] for bs in range(4) for w in range(n_worms)]
    m = [bodySegs[bs][1][w] for bs in range(4) for w in range(n_worms)]
    allPatches.extend (bs)
    allPatches.extend (m)

# The per-frame animation function.
# Inputs: 'points' is a full array with[n_timepoints][data][n_worms] (where
#	n_timepoints is the number of frames to be displayed).
# Remember that our display axes are:
#	* x ranges over the min/max x values from the simulation.
#	* y ranges from 0 to n_worms; i.e., each worm is allocated a vertical
#	  space of 1.
def per_frame (f):
    global legs, bodySegs, points, allPatches
    for y in range(legs.shape[1]):	# For each worm (& draw worm #i at y=i)
        # Make a slice with just this frame & worm. It has [0:5]=legX,
        # [6:10]=legLocked, [10:14]=muscle
        pts = points[f,1:,y]
        leg_width=30
        for l in range(5):
            legX = pts[l]; lock=pts[l+5]
            # A leg is 'width' wide, centered at 'x'.
            # Its top is at y+.5; it drops down to y+(lock?.3:.4).
            x_l = legX-leg_width/2
            y_b = y + (.4 - lock/10)
            legs[l][y].set_bounds (x_l,y_b, leg_width, y+.5-y_b)

        for bs in range(4):
            x1 = pts[bs]; x2=pts[bs+1]; musc=pts[bs+10]
            # Draw the segment from x1+(leg_width/2) to x2-(leg_width/2).
            # However, it may be that x2-x1 <= leg_width, in which case the body
            # part would vanish -- in that case, we pretend that leg is skinnier
            if (x1 + leg_width >= x2):
                leg_width = (x2-x1)/4

            # The height goes from y=.7 to y=.5.
            # So the LL is (x1+(leg_width/2),.5).
            LL_x = x1+(leg_width/2)
            dx = x2-(leg_width/2) - LL_x
            bodySegs[bs][0][y].set_bounds (LL_x,.5+y, dx,.2)

            # If the muscle is on, draw a black band across the segment.
            bodySegs[bs][1][y].set_visible (musc==100)
            bodySegs[bs][1][y].set_bounds (LL_x,.58+y, dx,.04)

    # We must return a list of everything that's moving this frame. Just assume
    # that everything moves (which it mostly does), and thus return the same
    # list of all rectangles all the time.
    return allPatches

# Draw the names of the worm(s), on the left side of the screen.
def draw_labels (labels, axes):
    L = len(labels)
    for i,label in enumerate(labels):
        y = (i+.5)
        axes.text (.05,y,label)

# Actually run the program.
# manducaGraph (0, 30, 'crawl6_final_output.txt', 'worm@20')