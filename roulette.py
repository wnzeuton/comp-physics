from vpython import *

scene.background = vec(0.2, 0.2, 0.2)
scene.forward = vec(0, -1, 0.2)  # bird's eye view
scene.up = vec(0, 0, 1)

# Number order
nums = [0, 28, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13, 1, 00, 
        27, 10, 25, 29, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35, 14, 2]

# Base
cylinder(pos=vec(0, -0.6, 0), axis=vec(0, 0.2, 0), radius=6, color=vec(0.4, 0.4, 0.4))
ring(pos=vec(0, 0, 0), axis=vec(0, 1, 0), radius=5, thickness=0.1, color=color.black)
cone(pos=vec(0, 0, 0), axis=vec(0, 0.7, 0), radius=2.5, color=color.black)

# Pockets
pockets = []
for i in range(38):
    a = i * (2 * pi / 38)
    mid = a + (pi / 38)
    r = 4.5
    p = box(pos=vec(r * cos(mid), -0.2, r * sin(mid)),
            size=vec(0.6, 0.4, 0.6),
            color=vec(0.05, 0.05, 0.05))
    p.axis = vec(cos(mid), 0, sin(mid))
    p.up = vec(0, 1, 0)
    pockets.append(p)

# Labels
labels = []
for i in range(38):
    a = i * (2 * pi / 38)
    mid = a + (pi / 38)
    n = nums[i]

    if i == 0 or i == 19:
        col = vec(0, 1, 0)
    elif i % 2 == 1:
        col = vec(1, 0, 0)
    else:
        col = vec(0.1, 0.1, 0.1)

    label = box(pos=vec(4.8 * cos(mid), 0.01, 4.8 * sin(mid)),
                size=vec(0.6, 0.02, 0.4),
                color=col)
    label.axis = vec(cos(mid), 0, sin(mid))
    label.up = vec(0, 1, 0)
    labels.append(label)

    # Text (flat)
    t = text(text=str(n), height=0.3, depth=0.02, color=color.white,
             align='center', pos=label.pos + vec(0, 0.01, 0))
    t.rotate(angle=pi/2, axis=vec(1, 0, 0))       
    t.rotate(angle=mid + pi, axis=vec(0, 1, 0))  
    labels.append(t)

# Dividers
bars = []
for i in range(38):
    a = i * (2 * pi / 38)
    x = 5 * cos(a)
    z = 5 * sin(a)
    bar = box(pos=vec(x, 0.2, z), size=vec(0.02, 0.3, 0.1), axis=vec(x, 0, z), color=color.white)
    bars.append(bar)

# Wheel
wheel = compound(pockets + labels + bars)
    
# Spin animation
#t = 0
#while True:
#    rate(30)
#    t += 0.05
#    wheel.rotate(angle=0.03, axis=vec(0, 1, 0), origin=vec(0, 0, 0))

def logistic(r, X):
    return r*X*(1-X)
    
seed = 0.8
r = 4

X =[]
X[0] = seed

def rng():
    X.append(logistic(r, X[-1]))
    print(X[-1])

for i in range(10):
    rng()

print(X)