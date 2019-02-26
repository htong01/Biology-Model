
# Reactions:
#	1. binding: mRNA + tRNA <-> mRNA.tRNA (bF, bR)
#	2. exciting: mRNA.tRNA <-> mRNA.tRNA* (eF, eR)
#	3. Edecay: mRNA.tRNA* <-> mRNA + tRNA (dR, dF)
#	4. product: mRNA.tRNA* <-> product (pF, dR)
# We will take [mRNA] and [tRNA] as given inputs. While reactions #1,3,4 can
# generate them, their concentrations nonetheless never change.
#
# To simplify life, we won't actually simulate #4; all we really care about is
# the steady-state [mRNA.tRNA*]. Since this metabolite simply creates product,
# it serves as a fine stand-in for [product]. And if we did simulate #4, we
# would also need a product-decay term (since otherwise [product] would just
# keep increasing linearly).
# Similarly, in real life transcription will create new mRNA, and other
# processes will keep [tRNA] fairly constant. By simply assuming [mRNA] and
# [tRNA] to be constant, we can ignore those processes.

# Abbreviations:
#	mRNA.tRNA = B (bound complex)
#	mRNA.tRNA* = EB (excited bound complex)
import numpy as np
def kinetic_proofreading():
        
    bF = 1
    bR = np.array([0.0001, 0.001, 0.01, 0.1, 1])
    eF = np.array([0.0001, 0.001, 0.01, 0.1, 1])
    eR = np.array([0, .001, .01, .1, 1])
    dF = np.array([0, .001, .01, .1, 1])
    bR2 = np.array([0.01, 0.1, 1, 10, 100])
    dR = bR; dR2 = bR2
    b = 0 
    for i in range(5):
        for n in range(5):
            for m in range(5):
                for d in range(5):
                    [final_EB1,OK1] = sim (bF, bR[i], eF[n], eR[m], dF[d], dR[i])
                    [final_EB2,OK2] = sim (bF, bR2[i], eF[n], eR[m], dF[d], dR2[i])
                    a = final_EB1/final_EB2
                    if a >= 9900:
                        print(bF, bR[i], eF[n], eR[m], dF[d], dR[i])
                    if a > b:
                        b = a # find the largest ratio
    print(b)
    
    return (final_EB1,OK1)



def sim (bF, bR, eF, eR, dF, dR):
    import sim_infrastructure as si
    si.clear_sim()
    final_EB=0		# In case the sim does not converge.

    # Add metabolites here.
    si.add_metab('mRNA', 1); si.add_metab('tRNA', 1)
    si.add_metab('B', 1); si.add_metab('EB', 1)
    

    si.add_reaction (binding,'binding', ['mRNA','tRNA'], ['B'], [bF,bR])
    si.add_reaction (exciting,'exciting', ['B'], ['EB'], [eF,eR])
    si.add_reaction (Edecay,'Edecay', ['mRNA','tRNA'], ['EB'], [dF,dR])
    # si.add_reaction (product,'product',['EB','prod'],['prod','EB'], [pF pR])

    [t,y,OK] = si.steady_state_sim (2000)
    final_EB = si.final_val (y, 'EB')
    return (final_EB,OK)

######################################################

# reaction binding: inputs=mRNA, tRNA; outputs=B; params=bF, bR.
#	1. binding: mRNA + tRNA <-> mRNA.tRNA (bF, bR)
def binding(t, inputs, outputs, params):
    import sim_library as sl
    sl.checkInputs ('binding', 2,1,2, inputs, outputs, params)
    mRNA,tRNA = inputs
    [B] = outputs
    bF,bR = params

    # Note that we do not assign any flow on the inputs; they are assumed to
    # have constant concentration.
    return ([[], [bF*mRNA*tRNA - bR*B]])

# reaction exciting: inputs=B; outputs=EB; params=eR, eF.
#	2. exciting: mRNA.tRNA <-> mRNA.tRNA* (eF, eR)
def exciting(t, inputs, outputs, params):
    import sim_library as sl
    sl.checkInputs ('exciting', 1,1,2, inputs, outputs, params)
    [B]  = inputs
    [EB] = outputs
    eF,eR = params

    d = eF*B - eR*EB	# d(EB)/dt
    return ([[-d], [d]])

# reaction Edecay; inputs=mRNA, tRNA; outputs=EB, params=dF, dR.
#	3. Edecay: mRNA.tRNA* <-> mRNA + tRNA (dR, dF)
def Edecay(t, inputs, outputs, params):
    import sim_library as sl
    sl.checkInputs ('Edecay', 2,1,2, inputs, outputs, params)
    mRNA,tRNA = inputs
    [EB] = outputs
    dF,dR=params
    return ([[], [dF*mRNA*tRNA - dR*EB]])

# reaction product; inputs=EB, product; outputs=product,EB, params=pF, pR.
#	4. product: mRNA.tRNA* <-> product (pF, pR)
def product(t, inputs, outputs, params):
    import sim_library as sl
    sl.checkInputs ('product', 2,1,2, inputs, outputs, params)
    EB,product = inputs
    pF,pR=params

    d = pF*EB - pR*product
    return ([[], [d,-d]])


import time
start = time.clock()
final_EB1,OK1 = kinetic_proofreading()
end = time.clock()
print ("Total time: %f s" % (end - start))