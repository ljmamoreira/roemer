# amoreira@ubi.pt, ljmamoreira@gmail.com
# November 2024
# Simple model for Earth, Jupiter, Io kinematics. Circular coplanar orbits.
# Generates list of observation times for visible Io emersions from and
#   occultations in Jupiter's shadow, together with distance traveled by light,
#   distance to Jupiter and distance to Io, both at the time of observation.

import numpy as np
import math as ma
import datetime as dttm
import matplotlib.pyplot as plt

PI = ma.pi
C = 2.003988804E-3
C2 = C**2

RJ = 5.2            # Jupiter's orbital radius (UA)
rJ = 6.67326E-4     # Jupiter's radius (UA)
RT = 1.0            # Earth's orbital radius (UA)
TT = 398.88*24*3600 # Synodic year (s)
wT = 2 * PI / TT
RI = 2.819e-3       # Io's orbital radius (UA)
TI = 152853.5047    # Io's synodical period
wI = 2 * PI / TI
aT = PI     # Earth phase constant (PI-> Jupiter conjunction; 0-> Opposition)
aI = 0.0    # Io phase constant
dt = 1.0


def event_coords(t, sn, so):
    to = t - dt
    te = to - so * (t - to)/(sn - so)
    xe = RJ + RI * ma.cos(aI + wI * te)
    ye = RI * ma.sin(aI + wI * te)
    return te, xe, ye

event_pending = False
in_shadow = False

# Coordinates of event not yet observed (neccessary declaration of the vars)
xe = 0
ye = 0
te = 0

emerg = []
occul = []
for i in range(int(TT/dt)):
    t = i * dt
    xT = RT * ma.cos(aT + wT * t)
    yT = RT * ma.sin(aT + wT * t)
    xI = RJ + RI * ma.cos(aI + wI * t)
    yI =      RI * ma.sin(aI + wI * t)
    # Check for visible occultation
    if (not in_shadow) and (-rJ < yI < 0) and (xI > RJ): # Occultation
        in_shadow = True
        if yT < 0:    # Visible from Earth
            event_pending = True
            sn = yI + rJ
            so = yIo + rJ
            te, xe, ye = event_coords(t, sn, so)
    # Check for visible emergence
    elif (in_shadow) and (yI > rJ) and (xI > RJ): # Emergence
        in_shadow = False
        if yT > 0:      # Visible from Earth
            event_pending = True
            sn = yI - rJ
            so = yIo - rJ
            te, xe, ye = event_coords(t, sn, so)
    elif event_pending: # Check for observations
        d2 = (xT - xe)**2 + (yT - ye)**2 - C2 * (t - te)**2
        if d2 < 0: # Event observed!
            event_pending = False
            to = t - dt
            tob = to - d2o * (t - to)/(d2 - d2o)        ## A
            de = ((xT - xe)**2 + (yT - ye)**2)**0.5
            dI = ((xT - xI)**2 + (yT - yI)**2)**0.5
            dJ = ((xT - RJ)**2 + yT**2)**0.5
            if yT > 0:
                emerg.append([tob, de, dI, dJ])
            else:
                occul.append([tob, de, dI, dJ])
        else:
            d2o = d2 #Needed for linear interpolation at ## A
    xIo = xI
    yIo = yI
