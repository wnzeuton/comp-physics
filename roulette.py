from vpython import *


scene.background = vec(0.3, 0.02, 0.02)
scene.forward = vec(0, -1, 0.2) # bird's eye view
scene.up = vec(0, 0, 1)




# randomization
def logistic(r, X):
    return r * X * (1 - X)

seed = 0.71
r = 4

lower_bound = 0.3
upper_bound = 0.7

X = [seed]

def rng():
    res = seed
    while(res == seed or lower_bound < 0.3 or upper_bound > 0.7):
        X.append(logistic(r, X[-1]))
        res = X[-1]
    
    n = (upper_bound - lower_bound ) / 38
    interval = (res - lower_bound) / n
    print( interval  - interval  % 1 )











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

    label = box(
    pos=vec(4.8 * cos(mid), 0.01, 4.8 * sin(mid)),
    size=vec(0.6, 0.02, 0.4),
    color=col
)
    label.axis = vec(cos(mid), 0, sin(mid))
    label.up = vec(0, 1, 0)
    labels.append(label)

    t = text(
    text=str(n),
    height=0.3,
    depth=0.02,
    color=color.white,
    align='center',
    pos=label.pos + vec(0, 0.02, 0),
    axis=vec(0, 1, 0),                      
    up=vec(cos(mid), 0, sin(mid))           
)






    labels.append(t)


    # Face it outward correctly
# faces the outer ring

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

# Casino ground (green felt table)
green_felt = cylinder(
    pos=vec(0, -0.601, 0),
    axis=vec(0, 0.01, 0),
    radius=30,
    color=vec(0, 0.3, 0)
)


# lighting
light_main = sphere(pos=vec(0, 5.5, 0), radius=0.6, color=vec(1, 0.8, 0.4), emissive=True)
light_side1 = sphere(pos=vec(3, 5.5, 3), radius=0.25, color=vec(1, 0.6, 0.2), emissive=True)
light_side2 = sphere(pos=vec(-3, 5.5, -3), radius=0.25, color=vec(1, 0.6, 0.2), emissive=True)

shadow_ring = ring(
    pos=vec(0, -0.599, 0),
    axis=vec(0, 1, 0),
    radius=5.3,
    thickness=0.4,
    color=vec(0.05, 0.05, 0.05),
    opacity=0.15
)




casino_wall = cylinder(
    pos=vec(0, -5, 0),
    axis=vec(0, 10, 0),
    radius=30,
    color=vec(0.4, 0.05, 0.05),
    opacity=1
)

casino_ceiling = box(
    pos=vec(0, 5, 0),
    size=vec(60, 0.2, 60),
    color=vec(0.2, 0.02, 0.02)
)





    
# Spin animation
#t = 0
#while True:
#    rate(30)
#    t += 0.05
#    wheel.rotate(angle=0.03, axis=vec(0, 1, 0), origin=vec(0, 0, 0))

dt = 0.01
def spin():
    t = 0
    total_time = 5
    spin_speed = 0.015

    initial_radius = 18
    final_radius = 5
    cam_height = 2.5

    orbit_speed = pi / 6
    scene.range = 6

    while t < total_time:
        rate(1/dt)
        t += dt

        wheel.rotate(angle=spin_speed, axis=vec(0, 1, 0), origin=vec(0, 0, 0))

        progress = (t / total_time) ** 1.8

        radius = initial_radius - (initial_radius - final_radius) * progress

        angle = progress * orbit_speed * total_time
        cam_x = radius * cos(angle)
        cam_z = radius * sin(angle)
        cam_y = cam_height

        scene.center = vec(0, 0, 0)
        scene.forward = norm(vec(0, 0, 0) - vec(cam_x, cam_y, cam_z))
        scene.up = vec(0, 1, 0)






        

spin()

def logistic(r, X):
    return r*X*(1-X)
    
seed = 0.4
r = 3.9

lower_bound = 0.3
upper_bound = 0.7

X = [seed]


def rng(n):
    global nums
    for i in range(n):
        #print("roll " + str(i))
        res = logistic(r, X[-1])
        while(res < lower_bound or res > upper_bound):
            print(res)
            X.append(logistic(r, X[-1]))
            res = X[-1]
            
        n = (upper_bound - lower_bound ) / 37
        interval = (res - lower_bound) / n
        #print(interval - (interval % 1))
        interval = int(interval  - (interval  % 1 ) - 1)
        #print(nums[0])
        #print(interval)
        print(nums[interval])
        #print(nums[interval  - (interval  % 1 ) - 1])

rng(10000)

#print(X)