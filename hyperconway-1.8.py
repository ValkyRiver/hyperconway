from tkinter import *
import math
import random

scale = 660
oncolor = "#0CF"
offcolor = "#FFF"
onheptcolor = "#0BE"
offheptcolor = "#EEE"
highlightcolor = "#FC0"
highlightheptcolor = "#EB0"
historycolor = "#AFC"
historyheptcolor = "#9EB"
bordercolor = "#000"
version = "1.8"

root = Tk()
C = Canvas(root)
C.pack(fill=BOTH, expand=1)
root.geometry(str(int(scale*1.94))+"x"+str(int(scale*1.1)))
root.title("HyperConway "+version)

try:
    clipboard = C.clipboard_get()
except:
    pass

UNIVERSE = [[]] # stores universe and each generation
RULE = []
GEN = 0 # current generation
DENSITY = 0.5
RADIUS = 2
SYM = False
CENTER = "X"
HOLONOMY = 0
HISTORY = False
PLAY = False
SPEED = 4

def onclick(event):
    if ((((event.x - scale*0.55) / (scale/2))**2 + ((event.y - scale*0.55) / (scale/2))**2)) <= 0.96:
        item = C.find_closest(event.x, event.y)
        tags = C.itemcget(item, "tags")
        cell = tags.split(" ")[1]
        if cell in UNIVERSE[GEN]:
            UNIVERSE[GEN].remove(cell)
        else:
            UNIVERSE[GEN].append(cell)
        for g, generation in enumerate(UNIVERSE):
            if g > GEN:
                UNIVERSE.remove(generation)
        render_universe(UNIVERSE[GEN], RULE, CENTER, HOLONOMY, HISTORY)

def change_center(event):
    global CENTER
    global HOLONOMY
    if ((((event.x - scale*0.55) / (scale/2))**2 + ((event.y - scale*0.55) / (scale/2))**2)) <= 0.4:
        item = C.find_closest(event.x, event.y)
        tags = C.itemcget(item, "tags")
        cell = tags.split(" ")[1]
        if shape(cell) == 7:
            if ((((event.x - scale*0.55) / (scale/2))**2 + ((event.y - scale*0.55) / (scale/2))**2)) <= 0.05:
                HOLONOMY = (HOLONOMY + 1) % 14
            else:
                old_center = CENTER
                CENTER = cell

                # HOLONOMY
                if old_center == "X":
                    HOLONOMY = (HOLONOMY + int(CENTER[1])*2 - 1) % 14
                elif CENTER == "X":
                    HOLONOMY = (HOLONOMY - int(old_center[1])*2 + 1) % 14
                
                elif CENTER == old_center + "L":
                    HOLONOMY = (HOLONOMY - 1) % 14
                elif CENTER == old_center + "M":
                    HOLONOMY = (HOLONOMY + 1) % 14
                elif CENTER == old_center + "R" and old_center[-1] == "R":
                    HOLONOMY = (HOLONOMY + 1) % 14
                elif CENTER == old_center + "R" and old_center[-1] != "R":
                    HOLONOMY = (HOLONOMY + 3) % 14
                
                elif CENTER + "L" == old_center:
                    HOLONOMY = (HOLONOMY + 1) % 14
                elif CENTER + "M" == old_center:
                    HOLONOMY = (HOLONOMY - 1) % 14
                elif CENTER + "R" == old_center and CENTER[-1] == "R":
                    HOLONOMY = (HOLONOMY - 1) % 14
                elif CENTER + "R" == old_center and CENTER[-1] != "R":
                    HOLONOMY = (HOLONOMY - 3) % 14

                elif CENTER == old_center[0:-1] + "L" and old_center[-1] == "M":
                    HOLONOMY = (HOLONOMY - 3) % 14
                elif CENTER == old_center[0:-1] + "L" and old_center[-1] == "R":
                    HOLONOMY = (HOLONOMY - 3) % 14
                elif CENTER == old_center[0:-1] + "M" and old_center[-1] == "R":
                    HOLONOMY = (HOLONOMY - 3) % 14

                elif CENTER[0:-1] + "L" == old_center and CENTER[-1] == "M":
                    HOLONOMY = (HOLONOMY + 3) % 14
                elif CENTER[0:-1] + "L" == old_center and CENTER[-1] == "R":
                    HOLONOMY = (HOLONOMY + 3) % 14
                elif CENTER[0:-1] + "M" == old_center and CENTER[-1] == "R":
                    HOLONOMY = (HOLONOMY + 3) % 14

                elif CENTER[-1] in "0123456" and old_center[-1] in "0123456" and int(CENTER[1])%7 == (int(old_center[1])+1)%7:
                    HOLONOMY = (HOLONOMY + 3) % 14
                elif CENTER[-1] in "0123456" and old_center[-1] in "0123456" and int(CENTER[1])%7 == (int(old_center[1])-1)%7:
                    HOLONOMY = (HOLONOMY - 3) % 14

                elif CENTER[-2:] == "MR" and old_center[-1] == "R":
                    HOLONOMY = (HOLONOMY - 1) % 14
                elif CENTER[-1] == "R" and old_center[-2:] == "MR":
                    HOLONOMY = (HOLONOMY + 1) % 14

                else: # requires finding opp_hept

                    if CENTER[-1] == "R":
                        cell2 = CENTER; recurse = 0
                        while cell2[-1] == "R":
                            cell2 = cell2[0:-1]; recurse += 1
                        if cell2[-1] in "0123456":
                            opp_hept = "X"+str((int(cell2[1])+1)%7) + (recurse*"L")
                        elif cell2[-1] == "L":
                            if cell2[-2] == "R":
                                opp_hept = cell2[0:-1] + "R" + (recurse*"L")
                            else:
                                opp_hept = cell2[0:-1] + "M" + (recurse*"L")
                        elif cell2[-1] == "M":
                            opp_hept = cell2[0:-1] + "R" + (recurse*"L")
                        if old_center == opp_hept:
                            HOLONOMY = (HOLONOMY - 1) % 14
                        elif old_center == opp_hept[0:-1]:
                            HOLONOMY = (HOLONOMY - 1) % 14

                    elif old_center[-1] == "R":
                        cell2 = old_center; recurse = 0
                        while cell2[-1] == "R":
                            cell2 = cell2[0:-1]; recurse += 1
                        if cell2[-1] in "0123456":
                            opp_hept = "X"+str((int(cell2[1])+1)%7) + (recurse*"L")
                        elif cell2[-1] == "L":
                            if cell2[-2] == "R":
                                opp_hept = cell2[0:-1] + "R" + (recurse*"L")
                            else:
                                opp_hept = cell2[0:-1] + "M" + (recurse*"L")
                        elif cell2[-1] == "M":
                            opp_hept = cell2[0:-1] + "R" + (recurse*"L")
                        if CENTER == opp_hept:
                            HOLONOMY = (HOLONOMY + 1) % 14
                        elif CENTER == opp_hept[0:-1]:
                            HOLONOMY = (HOLONOMY + 1) % 14

            render_universe(UNIVERSE[GEN], RULE, CENTER, HOLONOMY, HISTORY)

C.bind('<Button-1>', onclick)
C.bind('<Button-3>', change_center)

# CELL FORMAT

# HEPTAGONS
# X is the origin heptagon
# X0, X1, X2, X3, X4, X5, X6 are the heptagons corner from the origin
# then, the heptagons branch tree - all branches split into 3 (L M R), except if it ends in R

# HEXAGONS
# a refers to the hexagon on the left side of the edge between two heptagons
# if the edge is R, then there is also a hexagon on the right: b

# universe only stores live cells

hept_formations = { # o = ortho, m = meta, p = para, g = gyro
    (0, 0, 0, 0, 0, 0, 0): "0o",
    (1, 0, 0, 0, 0, 0, 0): "1o",
    (1, 1, 0, 0, 0, 0, 0): "2o",
    (1, 0, 1, 0, 0, 0, 0): "2m",
    (1, 0, 0, 1, 0, 0, 0): "2p",
    (1, 1, 1, 0, 0, 0, 0): "3o",
    (1, 1, 0, 1, 0, 0, 0): "3m",
    (1, 1, 0, 0, 1, 0, 0): "3p",
    (1, 0, 1, 0, 1, 0, 0): "3g",
    (1, 1, 1, 1, 0, 0, 0): "4o",
    (1, 1, 1, 0, 1, 0, 0): "4m",
    (1, 1, 0, 1, 1, 0, 0): "4p",
    (1, 1, 0, 1, 0, 1, 0): "4g",
    (1, 1, 1, 1, 1, 0, 0): "5o",
    (1, 1, 1, 1, 0, 1, 0): "5m",
    (1, 1, 1, 0, 1, 1, 0): "5p",
    (1, 1, 1, 1, 1, 1, 0): "6o",
    (1, 1, 1, 1, 1, 1, 1): "7o"
}

hex_formations = {
    (0, 0, 0, 0, 0, 0): "0a",
    (1, 0, 0, 0, 0, 0): "1x",
    (0, 1, 0, 0, 0, 0): "1h",
    (1, 1, 0, 0, 0, 0): "2a",
    (1, 0, 1, 0, 0, 0): "2x",
    (0, 1, 0, 1, 0, 0): "2h",
    (1, 0, 0, 1, 0, 0): "2c",
    (1, 1, 1, 0, 0, 0): "3a",
    (1, 1, 0, 0, 0, 1): "3b",
    (1, 0, 1, 1, 0, 0): "3c",
    (1, 1, 0, 1, 0, 0): "3d",
    (1, 0, 1, 0, 1, 0): "3x",
    (0, 1, 0, 1, 0, 1): "3h",
    (1, 1, 1, 1, 0, 0): "4a",
    (1, 1, 0, 1, 0, 1): "4x",
    (1, 1, 1, 0, 1, 0): "4h",
    (1, 1, 0, 1, 1, 0): "4c",
    (1, 1, 1, 1, 0, 1): "5x",
    (1, 1, 1, 1, 1, 0): "5h",
    (1, 1, 1, 1, 1, 1): "6a"
}

# COORDINATES OF VERTICES
# coordinates are polar-ish
# the first number is distance from center — 1 represents the boundary circle
# the second number is angle — 0 and 1 represent ends of a wedge of pi/7

def i(coords): # flip along 0 axis
    return (coords[0], -coords[1])
def j(coords): # flip along 1 axis
    return (coords[0], 2-coords[1])
def rot(coords, offset): # rotate by multiples of 2pi/7
    return (coords[0], coords[1] + (2*offset))

# DISTANCE 0.5
a0 = (0.187, 0.000)

# DISTANCE 1.5
a1 = (0.342, 0.000)
b1 = (0.431, 0.648)

# DISTANCE 2.5
a2 = (0.617, 0.192)
b2 = (0.555, 0.529)
c2 = (0.630, 0.819)

# DISTANCE 3.5
a3 = (0.763, 0.102)
b3 = (0.709, 0.263)
c3 = (0.742, 0.485)
d3 = (0.716, 0.714)
e3 = (0.777, 0.828)
f3 = (0.798, 1.000)

# DISTANCE 4.5
a4 = (0.859, 0.058)
b4 = (0.824, 0.146)
c4 = (0.848, 0.259)
d4 = (0.845, 0.389)
e4 = (0.807, 0.487)
f4 = (0.837, 0.612)
g4 = (0.830, 0.747)
h4 = (0.868, 0.809)
i4 = (0.876, 0.906)
j4 = (0.851, 1.000)

# DISTANCE 5.5
a5 = (0.927, 0.000)
b5 = (0.921, 0.055)
c5 = (0.895, 0.095)
d5 = (0.904, 0.168)
e5 = (0.889, 0.245)
f5 = (0.910, 0.300)
g5 = (0.910, 0.371)
h5 = (0.884, 0.424)
i5 = (0.895, 0.505)
j5 = (0.881, 0.586)
k5 = (0.907, 0.637)
l5 = (0.914, 0.707)
m5 = (0.902, 0.771)
n5 = (0.923, 0.810)
o5 = (0.926, 0.870)
p5 = (0.910, 0.920)
q5 = (0.925, 0.975)

# DISTANCE 6.5
a6 = (0.947, 0.000)
b6 = (0.955, 0.028)
c6 = (0.954, 0.061)
d6 = (0.939, 0.085)
e6 = (0.941, 0.132)
f6 = (0.931, 0.171)
g6 = (0.943, 0.205)
h6 = (0.945, 0.251)
i6 = (0.934, 0.290)
j6 = (0.947, 0.316)
k6 = (0.948, 0.358)
l6 = (0.933, 0.389)
m6 = (0.942, 0.431)
n6 = (0.940, 0.476)
o6 = (0.924, 0.512)
p6 = (0.936, 0.557)
q6 = (0.931, 0.611)
r6 = (0.945, 0.635)
s6 = (0.950, 0.674)
t6 = (0.937, 0.709)
u6 = (0.947, 0.746)
v6 = (0.942, 0.788)
w6 = (0.957, 0.809)
x6 = (0.962, 0.837)
y6 = (0.959, 0.863)
z6 = (0.945, 0.886)
A6 = (0.952, 0.923)
B6 = (0.945, 0.957)
C6 = (0.957, 0.986)

# DISTANCE 7.5
a7 = (0.974, 0.010)
b7 = (0.969, 0.027)
c7 = (0.974, 0.043)
d7 = (0.973, 0.064)
e7 = (0.966, 0.075)
f7 = (0.969, 0.097)
g7 = (0.968, 0.120)
h7 = (0.957, 0.138)
i7 = (0.963, 0.165)
j7 = (0.959, 0.193)
k7 = (0.968, 0.211)
l7 = (0.968, 0.235)
m7 = (0.960, 0.255)
n7 = (0.966, 0.282)
o7 = (0.963, 0.306)
p7 = (0.971, 0.322)
q7 = (0.973, 0.341)
r7 = (0.970, 0.362)
s7 = (0.960, 0.372)
t7 = (0.964, 0.400)
u7 = (0.959, 0.423)
v7 = (0.966, 0.446)
w7 = (0.965, 0.472)
x7 = (0.955, 0.490)
y7 = (0.959, 0.522)
z7 = (0.954, 0.549)
A7 = (0.963, 0.569)
B7 = (0.966, 0.596)
C7 = (0.960, 0.621)
D7 = (0.968, 0.637)
E7 = (0.970, 0.659)
F7 = (0.964, 0.680)
G7 = (0.969, 0.701)
H7 = (0.969, 0.723)
I7 = (0.963, 0.744)
J7 = (0.969, 0.766)
K7 = (0.968, 0.788)
L7 = (0.975, 0.801)
M7 = (0.976, 0.818)
N7 = (0.973, 0.832)
O7 = (0.978, 0.846)
P7 = (0.977, 0.864)
Q7 = (0.968, 0.878)
R7 = (0.971, 0.899)
S7 = (0.966, 0.920)
T7 = (0.971, 0.932)
U7 = (0.973, 0.951)
V7 = (0.969, 0.973)
W7 = (0.975, 0.990)

# SPECIAL (for hexagon-centered neighbor diagrams)
# as for the second coordinate here, 0 and 1 represent ends of a wedge of pi/3 (not pi/7) 
a8 = (0.163, 0.500)
a9 = (0.457, 0.000)
b9 = (0.421, 0.283)
c9 = (0.319, 0.534)
d9 = (0.409, 0.836)

# VERTEX COORDINATES FOR EACH CELL WITHIN DISTANCE 7 OF THE ORIGIN

vertex_coords = {
    # DISTANCE 1
    (a1, a0, rot(a0, 6), rot(a1, 6), rot(b1, 6), i(b1)): "a",

    # DISTANCE 2
    (a2, b2, b1, a1, i(b1), i(b2), i(a2)): "",
    (b2, c2, j(c2), j(b2), j(b1), b1): "Rb",

    # DISTANCE 3
    (i(a2), i(b2), i(c2), i(d3), i(c3), i(b3)): "La",
    (a3, b3, a2, i(a2), i(b3), i(a3)): "Ma",
    (b3, c3, d3, c2, b2, a2): "Ra",
    (d3, e3, f3, j(e3), j(d3), j(c2), c2): "R",

    # DISTANCE 4
    (i(a3), i(b3), i(c3), i(e4), i(d4), i(c4), i(b4)): "L",
    (a4, b4, a3, i(a3), i(b4), i(a4)): "LRb",
    (b4, c4, d4, e4, c3, b3, a3): "M",
    (e4, f4, g4, e3, d3, c3): "MRb",
    (g4, h4, i4, j4, f3, e3): "RLa",
    (j(e3), f3, j4, j(i4), j(h4), j(g4)): "RRa",
    (j(c3), j(d3), j(e3), j(g4), j(f4), j(e4)): "RRb",

    # DISTANCE 5
    (i(d4), i(e4), i(f4), i(j5), i(i5), i(h5)): "LLa",
    (i(c4), i(d4), i(h5), i(g5), i(f5), i(e5)): "LMa",
    (i(a4), i(b4), i(c4), i(e5), i(d5), i(c5)): "LRa",
    (a5, b5, c5, a4, i(a4), i(c5), i(b5), i(a5)): "LR",
    (c5, d5, e5, c4, b4, a4): "MLa",
    (e5, f5, g5, h5, d4, c4): "MMa",
    (h5, i5, j5, f4, e4, d4): "MRa",
    (j5, k5, l5, m5, h4, g4, f4): "MR",
    (m5, n5, o5, p5, i4, h4): "MRRb",
    (j4, i4, p5, q5, j(q5), j(p5), j(i4)): "RL",
    (j(h4), j(i4), j(p5), j(o5), j(n5), j(m5)): "RLRb",
    (j(f4), j(g4), j(h4), j(m5), j(l5), j(k5), j(j5)): "RR",

   # DISTANCE 6
    (i(g5), i(h5), i(i5), i(o6), i(n6), i(m6), i(l6)): "LL",
    (i(f5), i(g5), i(l6), i(k6), i(j6), i(i6)): "LLRb",
    (i(d5), i(e5), i(f5), i(i6), i(h6), i(g6), i(f6)): "LM",
    (i(b5), i(c5), i(d5), i(f6), i(e6), i(d6)): "LMRb",
    (a5, i(b5), i(d6), i(c6), i(b6), a6): "LRLa",
    (a6, b6, c6, d6, b5, a5): "LRRa",
    (d6, e6, f6, d5, c5, b5): "LRRb",
    (f6, g6, h6, i6, f5, e5, d5): "ML",
    (i6, j6, k6, l6, g5, f5): "MLRb",
    (l6, m6, n6, o6, i5, h5, g5): "MM",
    (o6, p6, q6, k5, j5, i5): "MMRb",
    (q6, r6, s6, t6, l5, k5): "MRLa",
    (t6, u6, v6, n5, m5, l5): "MRRa",
    (v6, w6, x6, y6, z6, o5, n5): "MRR",
    (z6, A6, B6, q5, p5, o5): "RLLa",
    (q5, B6, C6, j(C6), j(B6), j(q5)): "RLMa",
    (j(o5), j(p5), j(q5), j(B6), j(A6), j(z6)): "RLRa",
    (j(n5), j(o5), j(z6), j(y6), j(x6), j(w6), j(v6)): "RLR",
    (j(l5), j(m5), j(n5), j(v6), j(u6), j(t6)): "RRLa",
    (j(k5), j(l5), j(t6), j(s6), j(r6), j(q6)): "RRRa",
    (j(i5), j(j5), j(k5), j(q6), j(p6), j(o6)): "RRRb",

    # DISTANCE 7
    (i(n6), i(o6), i(p6), i(z7), i(y7), i(x7)): "LLLa",
    (i(m6), i(n6), i(x7), i(w7), i(v7), i(u7)): "LLMa",
    (i(k6), i(l6), i(m6), i(u7), i(t7), i(s7)): "LLRa",
    (i(j6), i(k6), i(s7), i(r7), i(q7), i(p7), i(o7)): "LLR",
    (i(h6), i(i6), i(j6), i(o7), i(n7), i(m7)): "LMLa",
    (i(g6), i(h6), i(m7), i(l7), i(k7), i(j7)): "LMMa",
    (i(e6), i(f6), i(g6), i(j7), i(i7), i(h7)): "LMRa",
    (i(c6), i(d6), i(e6), i(h7), i(g7), i(f7), i(e7)): "LMR",
    (i(b6), i(c6), i(e7), i(d7), i(c7), i(b7)): "LMRRb",
    (a7, b7, b6, a6, i(b6), i(b7), i(a7)): "LRL",
    (b7, c7, d7, e7, c6, b6): "LRLRb",
    (e7, f7, g7, h7, e6, d6, c6): "LRR",
    (h7, i7, j7, g6, f6, e6): "MLLa",
    (j7, k7, l7, m7, h6, g6): "MLMa",
    (m7, n7, o7, j6, i6, h6): "MLRa",
    (o7, p7, q7, r7, s7, k6, j6): "MLR",
    (s7, t7, u7, m6, l6, k6): "MMLa",
    (u7, v7, w7, x7, n6, m6): "MMMa",
    (x7, y7, z7, p6, o6, n6): "MMRa",
    (z7, A7, B7, C7, r6, q6, p6): "MMR",
    (C7, D7, E7, F7, s6, r6): "MMRRb",
    (F7, G7, H7, I7, u6, t6, s6): "MRL",
    (I7, J7, K7, w6, v6, u6): "MRRLa",
    (K7, L7, M7, N7, x6, w6): "MRRMa",
    (N7, O7, P7, Q7, y6, x6): "MRRRa",
    (Q7, R7, S7, A6, z6, y6): "MRRRb",
    (S7, T7, U7, V7, C6, B6, A6): "RLL",
    (C6, V7, W7, j(W7), j(V7), j(C6)): "RLLRb",
    (j(A6), j(B6), j(C6), j(V7), j(U7), j(T7), j(S7)): "RLM",
    (j(y6), j(z6), j(A6), j(S7), j(R7), j(Q7)): "RLMRb",
    (j(x6), j(y6), j(Q7), j(P7), j(O7), j(N7)): "RLRLa",
    (j(w6), j(x6), j(N7), j(M7), j(L7), j(K7)): "RLRRa",
    (j(u6), j(v6), j(w6), j(K7), j(J7), j(I7)): "RLRRb",
    (j(s6), j(t6), j(u6), j(I7), j(H7), j(G7), j(F7)): "RRL",
    (j(r6), j(s6), j(F7), j(E7), j(D7), j(C7)): "RRLRb",
    (j(p6), j(q6), j(r6), j(C7), j(B7), j(A7), j(z7)): "RRR"
}

def render_universe(universe=[], rule=[], center="X", holonomy=0, history=False): # holonomy is between 1 and 14
    # reset any previous calls of this function
    C.delete("clickable")
    C.delete("infotext")

    C.create_text(0.12*scale, 0.025*scale, text="Generation = " + str(GEN), font=("Arial", int(scale/50), "bold"), tags=("infotext"))
    C.create_text(0.12*scale, 0.06*scale, text="Population = " + str(len(universe)), font=("Arial", int(scale/50), "bold"), tags=("infotext"))
    C.create_text(0.97*scale, 0.025*scale, text="HyperConway " + version + " by Valky River", font=("Arial", int(scale/70), "bold"), tags=("infotext"))

    C.create_text(1.003*scale, 0.99*scale, text="Right-click center", font=("Arial", int(scale/70), "bold"), tags=("infotext"))
    C.create_text(1.001*scale, 1.01*scale, text="heptagon to rotate", font=("Arial", int(scale/70), "bold"), tags=("infotext"))
    C.create_text(0.972*scale, 1.04*scale, text="Right-click a near-center", font=("Arial", int(scale/70), "bold"), tags=("infotext"))
    C.create_text(0.963*scale, 1.06*scale, text="heptagon to change center", font=("Arial", int(scale/70), "bold"), tags=("infotext"))

    if center == "X":
        if "X" in universe:
            color = onheptcolor
        else:
            color = offheptcolor
            if history:
                for generation in range(GEN):
                    if "X" in UNIVERSE[generation]:
                        color = historyheptcolor
        C.create_polygon((a0[0] * math.sin((a0[1] + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * -math.cos((a0[1] + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * math.sin((a0[1]+2 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * -math.cos((a0[1]+2 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * math.sin((a0[1]+4 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * -math.cos((a0[1]+4 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * math.sin((a0[1]+6 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * -math.cos((a0[1]+6 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * math.sin((a0[1]+8 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * -math.cos((a0[1]+8 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * math.sin((a0[1]+10 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * -math.cos((a0[1]+10 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * math.sin((a0[1]+12 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * -math.cos((a0[1]+12 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         outline=bordercolor, fill=color, width=1, tags=("clickable", "X"))
        
        for direction in range(7):
            for cell in vertex_coords:

                if shape(vertex_coords[cell]) == 6:
                    if ("X"+str(direction)+vertex_coords[cell]) in universe:
                        color = oncolor
                    else:
                        color = offcolor
                        if history:
                            for generation in range(GEN):
                                if ("X"+str(direction)+vertex_coords[cell]) in UNIVERSE[generation]:
                                    color = historycolor
                    C.create_polygon((cell[0][0] * math.sin((cell[0][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[0][0] * -math.cos((cell[0][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[1][0] * math.sin((cell[1][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[1][0] * -math.cos((cell[1][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[2][0] * math.sin((cell[2][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[2][0] * -math.cos((cell[2][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[3][0] * math.sin((cell[3][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[3][0] * -math.cos((cell[3][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[4][0] * math.sin((cell[4][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[4][0] * -math.cos((cell[4][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[5][0] * math.sin((cell[5][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[5][0] * -math.cos((cell[5][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         outline=bordercolor, fill=color, width=1, tags=("clickable", ("X"+str(direction)+vertex_coords[cell])))
                else:
                    if ("X"+str(direction)+vertex_coords[cell]) in universe:
                        color = onheptcolor
                    else:
                        color = offheptcolor
                        if history:
                            for generation in range(GEN):
                                if ("X"+str(direction)+vertex_coords[cell]) in UNIVERSE[generation]:
                                    color = historyheptcolor
                    C.create_polygon((cell[0][0] * math.sin((cell[0][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[0][0] * -math.cos((cell[0][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[1][0] * math.sin((cell[1][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[1][0] * -math.cos((cell[1][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[2][0] * math.sin((cell[2][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[2][0] * -math.cos((cell[2][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[3][0] * math.sin((cell[3][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[3][0] * -math.cos((cell[3][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[4][0] * math.sin((cell[4][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[4][0] * -math.cos((cell[4][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[5][0] * math.sin((cell[5][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[5][0] * -math.cos((cell[5][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[6][0] * math.sin((cell[6][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         (cell[6][0] * -math.cos((cell[6][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                         outline=bordercolor, fill=color, width=1, tags=("clickable", ("X"+str(direction)+vertex_coords[cell])))

    else:
        if center in universe:
            color = onheptcolor
        else:
            color = offheptcolor
            if history:
                for generation in range(GEN):
                    if center in UNIVERSE[generation]:
                        color = historyheptcolor
        C.create_polygon((a0[0] * math.sin((a0[1] + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * -math.cos((a0[1] + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * math.sin((a0[1]+2 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * -math.cos((a0[1]+2 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * math.sin((a0[1]+4 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * -math.cos((a0[1]+4 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * math.sin((a0[1]+6 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * -math.cos((a0[1]+6 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * math.sin((a0[1]+8 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * -math.cos((a0[1]+8 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * math.sin((a0[1]+10 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * -math.cos((a0[1]+10 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * math.sin((a0[1]+12 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         (a0[0] * -math.cos((a0[1]+12 + holonomy) * (math.pi/7))*(scale/2) + (scale*0.55)),
                         outline=bordercolor, fill=color, width=1, tags=("clickable", center))
        disklist = [0, 1, 3, 7, 14, 26, 47]
        ringlist = [1, 2, 4, 7, 12, 21, 36]
        disk = find_disk(center)[1:8]
        for r, ring in enumerate(disk):
            distance = r + 1
            for c, cell0 in enumerate(ring):
                if shape(cell0) == 6:
                    if cell0 in universe:
                        color = oncolor
                    else:
                        color = offcolor
                        if history:
                            for generation in range(GEN):
                                if cell0 in UNIVERSE[generation]:
                                    color = historycolor
                    cell = list(vertex_coords)[disklist[r] + (c % ringlist[r])]; direction = int(c/ringlist[r])
                    C.create_polygon((cell[0][0] * math.sin((cell[0][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[0][0] * -math.cos((cell[0][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[1][0] * math.sin((cell[1][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[1][0] * -math.cos((cell[1][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[2][0] * math.sin((cell[2][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[2][0] * -math.cos((cell[2][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[3][0] * math.sin((cell[3][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[3][0] * -math.cos((cell[3][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[4][0] * math.sin((cell[4][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[4][0] * -math.cos((cell[4][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[5][0] * math.sin((cell[5][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[5][0] * -math.cos((cell[5][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     outline=bordercolor, fill=color, width=1, tags=("clickable", cell0))
                else:
                    if cell0 in universe:
                        color = onheptcolor
                    else:
                        color = offheptcolor
                        if history:
                            for generation in range(GEN):
                                if cell0 in UNIVERSE[generation]:
                                    color = historyheptcolor
                    cell = list(vertex_coords)[disklist[r] + (c % ringlist[r])]; direction = int(c/ringlist[r])
                    C.create_polygon((cell[0][0] * math.sin((cell[0][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[0][0] * -math.cos((cell[0][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[1][0] * math.sin((cell[1][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[1][0] * -math.cos((cell[1][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[2][0] * math.sin((cell[2][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[2][0] * -math.cos((cell[2][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[3][0] * math.sin((cell[3][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[3][0] * -math.cos((cell[3][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[4][0] * math.sin((cell[4][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[4][0] * -math.cos((cell[4][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[5][0] * math.sin((cell[5][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[5][0] * -math.cos((cell[5][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[6][0] * math.sin((cell[6][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     (cell[6][0] * -math.cos((cell[6][1] + (2*direction + holonomy)) * (math.pi/7))*(scale/2) + (scale*0.55)),
                                     outline=bordercolor, fill=color, width=1, tags=("clickable", cell0))

def drawformation(formation, x, y):
    horiz_buffer = 1.15
    horiz_offset = scale/5
    vert_buffer = 0.1
    vert_offset = scale/10
    divisor = 10
    if len(formation) == 7:
        C.create_polygon((a0[0] * math.sin((a0[1]) * (math.pi/7))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                         (a0[0] * -math.cos((a0[1]) * (math.pi/7))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                         (a0[0] * math.sin((a0[1]+2) * (math.pi/7))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                         (a0[0] * -math.cos((a0[1]+2) * (math.pi/7))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                         (a0[0] * math.sin((a0[1]+4) * (math.pi/7))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                         (a0[0] * -math.cos((a0[1]+4) * (math.pi/7))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                         (a0[0] * math.sin((a0[1]+6) * (math.pi/7))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                         (a0[0] * -math.cos((a0[1]+6) * (math.pi/7))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                         (a0[0] * math.sin((a0[1]+8) * (math.pi/7))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                         (a0[0] * -math.cos((a0[1]+8) * (math.pi/7))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                         (a0[0] * math.sin((a0[1]+10) * (math.pi/7))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                         (a0[0] * -math.cos((a0[1]+10) * (math.pi/7))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                         (a0[0] * math.sin((a0[1]+12) * (math.pi/7))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                         (a0[0] * -math.cos((a0[1]+12) * (math.pi/7))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                         outline=bordercolor, fill=highlightheptcolor, width=1)
        for gon in range(7):
            if formation[gon] == 1:
                color = oncolor
            else:
                color = offcolor
            C.create_polygon((a1[0] * math.sin((a1[1]+(gon*2)) * (math.pi/7))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                             (a1[0] * -math.cos((a1[1]+(gon*2)) * (math.pi/7))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                             (a0[0] * math.sin((a0[1]+(gon*2)) * (math.pi/7))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                             (a0[0] * -math.cos((a0[1]+(gon*2)) * (math.pi/7))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                             (a0[0] * math.sin((a0[1]-2+(gon*2)) * (math.pi/7))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                             (a0[0] * -math.cos((a0[1]-2+(gon*2)) * (math.pi/7))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                             (a1[0] * math.sin((a1[1]-2+(gon*2)) * (math.pi/7))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                             (a1[0] * -math.cos((a1[1]-2+(gon*2)) * (math.pi/7))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                             (b1[0] * math.sin((b1[1]-2+(gon*2)) * (math.pi/7))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                             (b1[0] * -math.cos((b1[1]-2+(gon*2)) * (math.pi/7))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                             (b1[0] * math.sin((-b1[1]+(gon*2)) * (math.pi/7))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                             (b1[0] * -math.cos((-b1[1]+(gon*2)) * (math.pi/7))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                             outline=bordercolor, fill=color, width=1)
    else:
        C.create_polygon((a8[0] * math.sin((a8[1]) * (math.pi/3))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                         (a8[0] * -math.cos((a8[1]) * (math.pi/3))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                         (a8[0] * math.sin((a8[1]+1) * (math.pi/3))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                         (a8[0] * -math.cos((a8[1]+1) * (math.pi/3))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                         (a8[0] * math.sin((a8[1]+2) * (math.pi/3))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                         (a8[0] * -math.cos((a8[1]+2) * (math.pi/3))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                         (a8[0] * math.sin((a8[1]+3) * (math.pi/3))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                         (a8[0] * -math.cos((a8[1]+3) * (math.pi/3))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                         (a8[0] * math.sin((a8[1]+4) * (math.pi/3))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                         (a8[0] * -math.cos((a8[1]+4) * (math.pi/3))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                         (a8[0] * math.sin((a8[1]+5) * (math.pi/3))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                         (a8[0] * -math.cos((a8[1]+5) * (math.pi/3))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                         outline=bordercolor, fill=highlightcolor, width=1)
        for gon in range(6):
            if gon % 2 == 0: #hexagon
                if formation[gon] == 1:
                    color = oncolor
                else:
                    color = offcolor
                C.create_polygon((a8[0] * math.sin((a8[1]-2+gon) * (math.pi/3))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                                 (a8[0] * -math.cos((a8[1]-2+gon) * (math.pi/3))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                                 (c9[0] * math.sin((c9[1]-2+gon) * (math.pi/3))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                                 (c9[0] * -math.cos((c9[1]-2+gon) * (math.pi/3))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                                 (d9[0] * math.sin((d9[1]-2+gon) * (math.pi/3))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                                 (d9[0] * -math.cos((d9[1]-2+gon) * (math.pi/3))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                                 (d9[0] * math.sin((-d9[1]+gon) * (math.pi/3))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                                 (d9[0] * -math.cos((-d9[1]+gon) * (math.pi/3))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                                 (c9[0] * math.sin((-c9[1]+gon) * (math.pi/3))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                                 (c9[0] * -math.cos((-c9[1]+gon) * (math.pi/3))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                                 (a8[0] * math.sin((-a8[1]+gon) * (math.pi/3))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                                 (a8[0] * -math.cos((-a8[1]+gon) * (math.pi/3))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                                 outline=bordercolor, fill=color, width=1)
            else: #heptagon
                if formation[gon] == 1:
                    color = onheptcolor
                else:
                    color = offheptcolor
                C.create_polygon((a9[0] * math.sin((a9[1]+gon-1) * (math.pi/3))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                                 (a9[0] * -math.cos((a9[1]+gon-1) * (math.pi/3))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                                 (b9[0] * math.sin((b9[1]+gon-1) * (math.pi/3))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                                 (b9[0] * -math.cos((b9[1]+gon-1) * (math.pi/3))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                                 (c9[0] * math.sin((c9[1]+gon-1) * (math.pi/3))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                                 (c9[0] * -math.cos((c9[1]+gon-1) * (math.pi/3))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                                 (a8[0] * math.sin((a8[1]+gon-1) * (math.pi/3))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                                 (a8[0] * -math.cos((a8[1]+gon-1) * (math.pi/3))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                                 (a8[0] * math.sin((-a8[1]+gon-1) * (math.pi/3))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                                 (a8[0] * -math.cos((-a8[1]+gon-1) * (math.pi/3))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                                 (c9[0] * math.sin((-c9[1]+gon-1) * (math.pi/3))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                                 (c9[0] * -math.cos((-c9[1]+gon-1) * (math.pi/3))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                                 (b9[0] * math.sin((-b9[1]+gon-1) * (math.pi/3))*(scale/divisor) + (horiz_buffer*scale + horiz_offset*x)),
                                 (b9[0] * -math.cos((-b9[1]+gon-1) * (math.pi/3))*(scale/divisor) + (vert_buffer*scale + vert_offset*y)),
                                 outline=bordercolor, fill=color, width=1)

def setrule(transition):
    if transition in RULE:
        RULE.remove(transition)
    else:
        RULE.append(transition)
    for g, generation in enumerate(UNIVERSE):
        if g > GEN:
            UNIVERSE.remove(generation)

def rulesmenu(rule=[]):
    for num, formation in enumerate(hept_formations):
        drawformation(formation, int(num/9), num%9)
        if num == 0:
            check = Checkbutton(root, text="S"+hept_formations[formation], command=lambda f="S"+hept_formations[formation]: [setrule(f)])
            if "S"+hept_formations[formation] in rule:
                check.select()
            check.place(x=1.2*scale + int(num/9)*0.2*scale, y=0.075*scale + (num%9)*0.1*scale)
        else:
            check = Checkbutton(root, text="B"+hept_formations[formation], command=lambda f="B"+hept_formations[formation]: [setrule(f)])
            if "B"+hept_formations[formation] in rule:
                check.select()
            check.place(x=1.2*scale + int(num/9)*0.2*scale, y=0.062*scale + (num%9)*0.1*scale)
            check = Checkbutton(root, text="S"+hept_formations[formation], command=lambda f="S"+hept_formations[formation]: [setrule(f)])
            if "S"+hept_formations[formation] in rule:
                check.select()
            check.place(x=1.2*scale + int(num/9)*0.2*scale, y=0.098*scale + (num%9)*0.1*scale)
    for num, formation in enumerate(hex_formations):
        drawformation(formation, int(num/10)+2, num%10)
        if num == 0:
            check = Checkbutton(root, text="S"+hex_formations[formation], command=lambda f="S"+hex_formations[formation]: [setrule(f)])
            if "S"+hex_formations[formation] in rule:
                check.select()
            check.place(x=1.2*scale + (int(num/10)+2)*0.2*scale, y=0.075*scale + (num%10)*0.1*scale)
        else:
            check = Checkbutton(root, text="B"+hex_formations[formation], command=lambda f="B"+hex_formations[formation]: [setrule(f)])
            if "B"+hex_formations[formation] in rule:
                check.select()
            check.place(x=1.2*scale + (int(num/10)+2)*0.2*scale, y=0.062*scale + (num%10)*0.1*scale)
            check = Checkbutton(root, text="S"+hex_formations[formation], command=lambda f="S"+hex_formations[formation]: [setrule(f)])
            if "S"+hex_formations[formation] in rule:
                check.select()
            check.place(x=1.2*scale + (int(num/10)+2)*0.2*scale, y=0.098*scale + (num%10)*0.1*scale)

def genbuttons():
    resetgen = Button(C, font=("Arial", int(scale/50)), text="◀◀", command = lambda: [reset_generation(), play("off")])
    prevgen = Button(C, font=("Arial", int(scale/50)), text=" ◀ ", command = lambda: [prev_generation(), play("off")])
    nextgen = Button(C, font=("Arial", int(scale/50)), text=" ▶ ", command = lambda: [next_generation(), play("off")])
    
    randomfill = Button(C, font=("Arial", int(scale/70), "bold"), text="Random", command = lambda: [random_fill(RADIUS, DENSITY, SYM)])
    radiusdown = Button(C, font=("Arial", int(scale/70)), text="◀", command = lambda: [randomfill_options("small")])
    radiusup = Button(C, font=("Arial", int(scale/70)), text="▶", command = lambda: [randomfill_options("big")])
    densitydown = Button(C, font=("Arial", int(scale/70)), text="◀", command = lambda: [randomfill_options("down")])
    densityup = Button(C, font=("Arial", int(scale/70)), text="▶", command = lambda: [randomfill_options("up")])
    clear = Button(C, font=("Arial", int(scale/70), "bold"), text="Clear", command = lambda: [random_fill(0, 0)])

    resetgen.place(x=0.03*scale, y=0.085*scale)
    prevgen.place(x=0.095*scale, y=0.085*scale)
    nextgen.place(x=0.16*scale, y=0.085*scale)
    
    randomfill.place(x=1.12*scale, y=0.99*scale)
    radiusdown.place(x=1.23*scale, y=0.97*scale)
    radiusup.place(x=1.26*scale, y=0.97*scale)
    densitydown.place(x=1.31*scale, y=0.97*scale)
    densityup.place(x=1.34*scale, y=0.97*scale)
    clear.place(x=1.388*scale, y=0.99*scale)

def randomfill_options(option=""):
    global RADIUS; global DENSITY
    if option == "big" and RADIUS < 7:
        RADIUS += 1
    elif option == "small" and RADIUS > 0:
        RADIUS -= 1
    elif option == "down" and DENSITY > 0:
        DENSITY = round((DENSITY - 0.05)*20) / 20
    elif option == "up" and DENSITY < 1:
        DENSITY = round((DENSITY + 0.05)*20) / 20
    C.delete("randomfilltext")
    C.create_text(1.257*scale, 1.025*scale, text="Radius", font=("Arial", int(scale/70), "bold"), tags=("randomfilltext"))
    C.create_text(1.257*scale, 1.045*scale, text=str(RADIUS), font=("Arial", int(scale/70), "bold"), tags=("randomfilltext"))
    C.create_text(1.338*scale, 1.025*scale, text="Density", font=("Arial", int(scale/70), "bold"), tags=("randomfilltext"))
    C.create_text(1.338*scale, 1.045*scale, text=str(DENSITY), font=("Arial", int(scale/70), "bold"), tags=("randomfilltext"))
    

def reset_generation():
    global GEN
    GEN = 0
    render_universe(UNIVERSE[GEN], RULE, CENTER, HOLONOMY, HISTORY)
        
def prev_generation():
    global GEN
    if GEN != 0:
        GEN -= 1
        render_universe(UNIVERSE[GEN], RULE, CENTER, HOLONOMY, HISTORY)

def next_generation():
    global GEN
    if GEN == len(UNIVERSE)-1:
        UNIVERSE.append(advance(RULE, UNIVERSE[GEN]))
    else:
        UNIVERSE[GEN+1] = advance(RULE, UNIVERSE[GEN])
    GEN += 1
    render_universe(UNIVERSE[GEN], RULE, CENTER, HOLONOMY, HISTORY)

def random_fill(radius, density=0.5, sym=False):
    universe = []
    numcells = [0, 1, 3, 7, 14, 26, 47, 83]
    if random.random() <= density:
        universe.append("X")
    if sym:
        for num in range(numcells[radius]):
            if random.random() <= density:
                for offset in range(7):
                    universe.append("X"+str(offset)+tuple(vertex_coords.values())[num])
    else:
        for offset in range(7):
            for num in range(numcells[radius]):
                if random.random() <= density:
                    universe.append("X"+str(offset)+tuple(vertex_coords.values())[num])
    global GEN
    GEN = 0
    UNIVERSE[GEN] = universe
    render_universe(UNIVERSE[GEN], RULE, CENTER, HOLONOMY, HISTORY)

def shape(cell):
    if cell == "":
        return 7
    elif cell[-1] in "ab":
        return 6
    else:
        return 7

def neighbors(cell): # find adjacent cells

    # HEXAGON CASE (always returns hex-hept-hex-hept-hex-hept)
    if cell[-1] == "b":
        cell2 = cell[0:-1]; recurse = 0
        while cell2[-1] == "R":
            cell2 = cell2[0:-1]; recurse += 1
        if cell2[-1] in "0123456":
            opp_hept = "X"+str((int(cell2[1])+1)%7) + ((recurse-1)*"L")
        elif cell2[-1] == "L":
            if cell2[-2] == "R":
                opp_hept = cell2[0:-1] + "R" + ((recurse-1)*"L")
            else:
                opp_hept = cell2[0:-1] + "M" + ((recurse-1)*"L")
        elif cell2[-1] == "M":
            opp_hept = cell2[0:-1] + "R" + ((recurse-1)*"L")
        return [cell[0:-1]+"a", cell[0:-1], opp_hept+"La", opp_hept, opp_hept+"a", cell[0:-2]]
    elif cell[-1] == "a" and cell[-2] in "R":
        if cell[-3] == "R":
            return [cell[0:-2]+"La", cell[0:-2]+"L", cell[0:-2]+"LRb", cell[0:-1], cell[0:-1]+"b", cell[0:-2]]
        else:
            return [cell[0:-2]+"Ma", cell[0:-2]+"M", cell[0:-2]+"MRb", cell[0:-1], cell[0:-1]+"b", cell[0:-2]]
    elif cell[-1] == "a" and cell[-2] in "M":
        return [cell[0:-2]+"La", cell[0:-2]+"L", cell[0:-2]+"LRb", cell[0:-1], cell[0:-2]+"Ra", cell[0:-2]]
    elif cell[-1] == "a" and cell[-2] in "L":
        cell2 = cell[0:-1]; recurse = 0
        while cell2[-1] == "L":
            cell2 = cell2[0:-1]; recurse += 1
        if cell2[-1] in "0123456":
            opp_hept = "X"+str((int(cell2[1])-1)%7) + (recurse*"R")
        elif cell2[-1] == "M":
            opp_hept  = cell2[0:-1] + "L" + (recurse*"R")
        elif cell2[-1] == "R":
            if cell2[-2] == "R":
                opp_hept = cell2[0:-1] + "L" + (recurse*"R")
            else:
                opp_hept = cell2[0:-1] + "M" + (recurse*"R")
        if cell[-3] == "R":
            return [opp_hept+"b", opp_hept, opp_hept+"Rb", cell[0:-1], cell[0:-2]+"Ra", cell[0:-2]]
        else:
            return [opp_hept+"b", opp_hept, opp_hept+"Rb", cell[0:-1], cell[0:-2]+"Ma", cell[0:-2]]
    elif cell[-1] == "a" and cell[-2] in "0123456":
        return ["X"+str((int(cell[1])-1)%7)+"a", "X"+str((int(cell[1])-1)%7), "X"+str((int(cell[1])-1)%7)+"Rb", cell[0:-1], "X"+str((int(cell[1])+1)%7)+"a", "X"]

    # HEPTAGON CASE
    elif cell[-1] == "R":
        cell2 = cell; recurse = 0
        while cell2[-1] == "R":
            cell2 = cell2[0:-1]; recurse += 1
        if cell2[-1] in "0123456":
            opp_hept = "X"+str((int(cell2[1])+1)%7) + (recurse*"L")
        elif cell2[-1] == "L":
            if cell2[-2] == "R":
                opp_hept = cell2[0:-1] + "R" + (recurse*"L")
            else:
                opp_hept = cell2[0:-1] + "M" + (recurse*"L")
        elif cell2[-1] == "M":
            opp_hept = cell2[0:-1] + "R" + (recurse*"L")
        if cell[-2] == "R":
            return [cell+"La", cell+"Ra", cell+"Rb", opp_hept+"a", cell+"b", cell+"a", cell[0:-1]+"LRb"]
        else:
            return [cell+"La", cell+"Ra", cell+"Rb", opp_hept+"a", cell+"b", cell+"a", cell[0:-1]+"MRb"]
    elif cell[-1] == "M":
        return [cell+"La", cell+"Ma", cell+"Ra", cell+"Rb", cell[0:-1]+"Ra", cell+"a", cell[0:-1]+"LRb"]
    elif cell[-1] == "L":
        cell2 = cell; recurse = 0
        while cell2[-1] == "L":
            cell2 = cell2[0:-1]; recurse += 1
        if cell2[-1] in "0123456":
            opp_hept = "X"+str((int(cell2[1])-1)%7) + ((recurse+1)*"R")
        elif cell2[-1] == "M":
            opp_hept = cell2[0:-1] + "L" + ((recurse+1)*"R")
        elif cell2[-1] == "R":
            if cell2[-2] == "R":
                opp_hept = cell2[0:-1] + "L" + ((recurse+1)*"R")
            else:
                opp_hept = cell2[0:-1] + "M" + ((recurse+1)*"R")
        if cell[-2] == "R":
            return [cell+"La", cell+"Ma", cell+"Ra", cell+"Rb", cell[0:-1]+"Ra", cell+"a", opp_hept+"b"]
        else:
            return [cell+"La", cell+"Ma", cell+"Ra", cell+"Rb", cell[0:-1]+"Ma", cell+"a", opp_hept+"b"]
    elif cell[-1] in "0123456":
        return [cell+"La", cell+"Ma", cell+"Ra", cell+"Rb", "X"+str((int(cell[1])+1)%7)+"a", cell+"a", "X"+str((int(cell[1])-1)%7)+"Rb"]
    elif cell[-1] == "X":
        return ["X0a", "X1a", "X2a", "X3a", "X4a", "X5a", "X6a"]

def formation(cell, universe=[]):
    neighbor_formation = []
    global hept_formations; global hex_formations
    for neighbor in neighbors(cell):
        if neighbor in universe:
            neighbor_formation.append(1)
        else:
            neighbor_formation.append(0)
    neighbor_formation2 = neighbor_formation + neighbor_formation
    neighbor_formation3 = neighbor_formation2[0:-1][::-1]
    if len(neighbor_formation) == 7:
        for offset in range(7):
            if hept_formations.get(tuple(neighbor_formation2[offset:(offset+7)])) != None:
                return hept_formations[tuple(neighbor_formation2[offset:(offset+7)])]
            if hept_formations.get(tuple(neighbor_formation3[offset:(offset+7)])) != None:
                return hept_formations[tuple(neighbor_formation3[offset:(offset+7)])]   
    elif len(neighbor_formation) == 6:
        for offset in range(3):
            if hex_formations.get(tuple(neighbor_formation2[(offset*2):(offset*2+6)])) != None:
                return hex_formations[tuple(neighbor_formation2[(offset*2):(offset*2+6)])]
            if hex_formations.get(tuple(neighbor_formation3[(offset*2):(offset*2+6)])) != None:
                return hex_formations[tuple(neighbor_formation3[(offset*2):(offset*2+6)])]

def advance(rule, universe=[]):
    universe2 = list(universe)
    universe3 = []
    for livecell in universe:
        for neighbor in neighbors(livecell):
            if neighbor not in universe2:
                universe2.append(neighbor)
    for cell in universe2:
        if cell in universe:
            if "S"+formation(cell, universe) in rule:
                universe3.append(cell)
        else:
            if "B"+formation(cell, universe) in rule:
                universe3.append(cell)
    return universe3

def compress_rule(rule):
    outer_total = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7"]
    total_formations = [3, 7, 10, 8, 5, 2, 1, 2, 3, 7, 10, 8, 5, 2, 1]
    compressed = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    string = "B"
    for transition in rule:
        compressed[outer_total.index(transition[0:2])].append(transition[2])
    for o, outer in enumerate(compressed):
        if o == 7:
            string += "/S"
        if len(outer) != 0:
            string += outer_total[o][1]
            if len(outer) != total_formations[o]:
                string += "".join(sorted(outer))
    return string

def decompress_rule(string):
    outer_total = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7"]
    formation_symbol = ["hox", "chompax", "pogchambdx", "champgox", "phomx", "oa", "o", "oa", "hox", "chompax", "pogchambdx", "champgox", "phomx", "oa", "o"]
    string_list = list(string); rule = []
    bs = ""; outer = 0
    for c, character in enumerate(string_list):
        if character == "B":
            bs = "B"
        elif character in "/S":
            bs = "S"
        elif character in "01234567":
            outer = character
            if c == len(string_list)-1:
                for letter in formation_symbol[outer_total.index(bs+outer)]:
                    rule.append(bs+str(outer)+letter)
            elif string_list[c+1] not in "pogchambdx":
                for letter in formation_symbol[outer_total.index(bs+outer)]:
                    rule.append(bs+str(outer)+letter)
        else:
            rule.append(bs+str(outer)+character)
    return rule

def buttons():
    importbutton = Button(C, font=("Arial", int(scale/70), "bold"), text="Import from clipboard", command = lambda: [import_code(C.clipboard_get()), play("off")])
    exportbutton = Button(C, font=("Arial", int(scale/70), "bold"), text="Export to clipboard", command = lambda: [export_code(RULE, UNIVERSE[GEN])])

    originbutton = Button(C, font=("Arial", int(scale/70), "bold"), text="Origin", command = lambda: [origin()])
    playbutton = Button(C, font=("Arial", int(scale/70), "bold"), text="Play/Pause", command = lambda: [play("toggle")])
    historybutton = Button(C, font=("Arial", int(scale/70), "bold"), text="History", command = lambda: [show_history()])

    speeddown = Button(C, font=("Arial", int(scale/70)), text="◀", command = lambda: [speed(-1)])
    speedup = Button(C, font=("Arial", int(scale/70)), text="▶", command = lambda: [speed(1)])

    exportbutton.place(x=0.03*scale, y=0.99*scale)
    importbutton.place(x=0.03*scale, y=1.03*scale)
    originbutton.place(x=1.01*scale, y=0.93*scale)
    historybutton.place(x=0.03*scale, y=0.95*scale)
    playbutton.place(x=0.03*scale, y=0.14*scale)

    speeddown.place(x=0.03*scale, y=0.185*scale)
    speedup.place(x=0.06*scale, y=0.185*scale)
                
def export_code(rule, universe):
    C.clipboard_clear()
    C.clipboard_append(" ".join([compress_rule(rule)] + universe))

def import_code(code):
    try:
        if code.strip()[0] == "B":
            C.delete("all")
            code_list = (code.strip()).split(" ")
            global GEN; global RULE; global UNIVERSE
            GEN = 0
            RULE = decompress_rule(code_list[0])
            if len(code_list) == 1:
                UNIVERSE = [[]]
            else:
                UNIVERSE = [code_list[1:]]
            render_universe(UNIVERSE[GEN], RULE, CENTER, HOLONOMY, HISTORY)
            rulesmenu(RULE)
            genbuttons()
            randomfill_options("")
            buttons()
            speed(0)
    except:
        pass

def find_disk(cell):
    dist0 = [cell]; dist1 = neighbors(cell); dist2 = []; dist3 = []; dist4 = []; dist5 = []; dist6 = []; dist7 = []
    for cell1 in dist1: # distance 2
        for cell2 in neighbors(cell1) + neighbors(cell1):
            if cell2 not in dist0 + dist1 + dist2 and (len(dist2) == 0 or dist2[-1] in neighbors(cell2)):
                dist2.append(cell2)
    dist2.append(dist2[0]); dist2.pop(0); dist2.append(dist2[0]); dist2.pop(0)
    for cell1 in dist2: # distance 3
        for cell2 in neighbors(cell1) + neighbors(cell1):
            if cell2 not in dist0 + dist1 + dist2 + dist3 and (len(dist3) == 0 or dist3[-1] in neighbors(cell2)):
                dist3.append(cell2)
    for cell1 in dist3: # distance 4
        for cell2 in neighbors(cell1) + neighbors(cell1):
            if cell2 not in dist0 + dist1 + dist2 + dist3 + dist4 and (len(dist4) == 0 or dist4[-1] in neighbors(cell2)):
                dist4.append(cell2)  
    dist4.append(dist4[0]); dist4.pop(0)
    for cell1 in dist4: # distance 5
        for cell2 in neighbors(cell1) + neighbors(cell1):
            if cell2 not in dist0 + dist1 + dist2 + dist3 + dist4 + dist5 and (len(dist5) == 0 or dist5[-1] in neighbors(cell2)):
                dist5.append(cell2)
    for cell1 in dist5: # distance 6
        for cell2 in neighbors(cell1) + neighbors(cell1):
            if cell2 not in dist0 + dist1 + dist2 + dist3 + dist4 + dist5 + dist6 and (len(dist6) == 0 or dist6[-1] in neighbors(cell2)):
                dist6.append(cell2)
    dist6.append(dist6[0]); dist6.pop(0)
    for cell1 in dist6: # distance 7
        for cell2 in neighbors(cell1) + neighbors(cell1):
            if cell2 not in dist0 + dist1 + dist2 + dist3 + dist4 + dist5 + dist6 + dist7 and (len(dist7) == 0 or dist7[-1] in neighbors(cell2)):
                dist7.append(cell2)
    return [dist0, dist1, dist2, dist3, dist4, dist5, dist6, dist7]

def origin():
    global CENTER
    global HOLONOMY
    CENTER = "X"
    HOLONOMY = 0
    render_universe(UNIVERSE[GEN], RULE, CENTER, HOLONOMY, HISTORY)

def show_history():
    global HISTORY
    HISTORY = not HISTORY
    render_universe(UNIVERSE[GEN], RULE, CENTER, HOLONOMY, HISTORY)

def play(arg=""):
    global PLAY
    if arg == "off":
        PLAY = False
    elif arg == "on":
        PLAY = True
    elif arg == "toggle":
        PLAY = not PLAY
    if PLAY:
        next_generation()
        if CENTER == "X":
            C.after(int(1000/SPEED) - 20, play) # speed is only approximate — it assumes next_generation() takes 20ms to process
        else:
            C.after(int(1000/SPEED) - 25, play) # it takes longer to render when the center is not at the origin (maybe 25ms?)

def speed(option):
    C.delete("speed")
    global SPEED
    speedlist = [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5,5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24, 26, 28, 30, 32]
    if speedlist.index(SPEED) + option >= 0 and speedlist.index(SPEED) + option <= len(speedlist) - 1:
        SPEED = speedlist[speedlist.index(SPEED) + option]
    C.create_text(0.056*scale, 0.238*scale, text=str(SPEED) + " / s", font=("Arial", int(scale/70), "bold"), tags=("speed"))

render_universe()
rulesmenu()
genbuttons()
randomfill_options("")
buttons()
speed(0)

root.mainloop()
        

