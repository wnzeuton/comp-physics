Web VPython 3.2


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
    global interval
    res = seed
    while(res == seed or lower_bound < 0.3 or upper_bound > 0.7):
        X.append(logistic(r, X[-1]))
        res = X[-1]
    
    n = (upper_bound - lower_bound ) / 38
    interval = (res - lower_bound) / n
    print( interval  - interval  % 1 )
    return int(interval - interval % 1)

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
    
    bowl = box(
    pos=vec(5.75*cos(mid),.25,5.75*sin(mid)), size = vec(.25,1.1,1.5),
    axis= -vec(8*cos(mid),-15,8*sin(mid)),
    up=vec(label.pos.z,0,-label.pos.x),
    color=vec(80/255,49/255,29/255))
    
    labels.append(bowl)

#text labels


    t = text(
    text=str(n),
    height=0.3,
    depth=0.02,
    color=color.white,
    align='center',
    pos=label.pos + vec(0, 0.012, 0),
    axis=vec(0, 1, 0),                      
    up=(-(label.pos + vec(0,0.01,0))),
    axis=vector(label.pos.z,0,-label.pos.x)
)


    labels.append(t)


# Dividers
bars = []
for i in range(38):
    a = i * (2 * pi / 38)  # edge of pocket
    inner_r = 4.3
    outer_r = 4.8

    start = vec(inner_r * cos(a), 0.2, inner_r * sin(a))
    end = vec(outer_r * cos(a), 0.2, outer_r * sin(a))
    direction = norm(end - start)

    mid = (start + end) / 2
    length = mag(end - start)

    bar = box(
    pos=vec(mid.x, 0.01, mid.z),           # low on the wheel
    axis=direction,
    size=vec(length, 0.1, 0.14),          # short and flat
    color=color.white
)

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

#bol
ball = sphere(
    pos=vec(4.3, 0.05, 0),  # near rim
    radius=0.1,
    color=color.white,
    make_trail=True,
    retain=2
)


#bowl


    


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

def smoothstep(x):
    return x * x * (3 - 2 * x)

def spin():
    t = 0
    total_time = 6
    spin_speed = 0.015

    ball_angle = 0
    ball_speed = 0.12
    ball_radius = 4.3
    ball_y = 0.05

    result_index = int(random() * 38)
    result_angle = result_index * (2 * pi / 38) + (pi / 38)
    print("Winning index:", result_index, "| Number:", nums[result_index], "| Angle:", result_angle)

    total_spin_angle = 0
    lock_start_angle = None

    # Fixed camera for testing
    cam_distance = 13
    cam_height = 3
    cam_angle = pi / 4
    cam_x = cam_distance * cos(cam_angle)
    cam_z = cam_distance * sin(cam_angle)
    scene.center = vec(0, 0, 0)
    scene.forward = norm(vec(0, 0, 0) - vec(cam_x, cam_height, cam_z))
    scene.up = vec(0, 1, 0)
    scene.range = 6

    while t < total_time:
        rate(1 / dt)
        t += dt
        progress = min(1, t / total_time)

        ease_start = 0.8
        ease_factor = (progress - ease_start) / (1 - ease_start)
        ease = smoothstep(ease_factor) if progress > ease_start else 0

        # Rotate wheel
        spin_angle = spin_speed
        total_spin_angle += spin_angle
        wheel.rotate(angle=spin_angle, axis=vec(0, 1, 0), origin=vec(0, 0, 0))

        # Ball spin
        if ease == 0:
            ball_speed *= 0.992
            ball_angle += ball_speed
        else:
            if lock_start_angle is None:
                lock_start_angle = ball_angle
            ball_angle = (1 - ease) * lock_start_angle + ease * (result_angle)

        ball.pos = vec(ball_radius * cos(ball_angle), ball_y, ball_radius * sin(ball_angle))
        
        # Lock final
    wheel.rotate(angle=-total_spin_angle, axis=vec(0, 1, 0), origin=vec(0, 0, 0))
    ball.pos = vec(ball_radius * cos(-result_angle), ball_y, ball_radius * sin(-result_angle))

    print("Ball landed cleanly in:", nums[result_index])

spin()


#print(X)
    

