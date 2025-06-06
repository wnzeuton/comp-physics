Web VPython 3.2
import random
scene.background = vec(0.3, 0.02, 0.02)
scene.forward = vec(0, -1, 0.2)
scene.up = vec(0, 0, 1)


nums = [0, 28, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13, 1, 00,
        27, 10, 25, 29, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35, 14, 2]

cylinder(pos=vec(0, -0.6, 0), axis=vec(0, 0.2, 0), radius=6, color=vec(0.4, 0.4, 0.4))
ring(pos=vec(0, 0, 0), axis=vec(0, 1, 0), radius=5, thickness=0.1, color=color.black)
cone(pos=vec(0, 0, 0), axis=vec(0, 0.7, 0), radius=2.5, color=color.black)

pockets = []
for i in range(38):
    a = i * (2 * pi / 38)
    mid = a + (pi / 38)
    r = 4.5
    p = box(pos=vec(r * cos(mid), -0.2, r * sin(mid)), size=vec(0.6, 0.4, 0.6), color=vec(0.05, 0.05, 0.05))
    p.axis = vec(cos(mid), 0, sin(mid))
    p.up = vec(0, 1, 0)
    pockets.append(p)

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
    label = box(pos=vec(4.8 * cos(mid), 0.01, 4.8 * sin(mid)), size=vec(0.6, 0.02, 0.4), color=col)
    label.axis = vec(cos(mid), 0, sin(mid))
    label.up = vec(0, 1, 0)
    labels.append(label)
    bowl = box(pos=vec(5.75*cos(mid),.25,5.75*sin(mid)), size=vec(.25,1.1,1.5), axis= -vec(8*cos(mid),-15,8*sin(mid)), up=vec(label.pos.z,0,-label.pos.x), color=vec(80/255,49/255,29/255))
    labels.append(bowl)
    t = text(text=str(n), height=0.3, depth=0.02, color=color.white, align='center', pos=label.pos + vec(0, 0.012, 0), axis=vec(0, 1, 0), up=(-(label.pos + vec(0,0.01,0))), axis=vector(label.pos.z,0,-label.pos.x))
    labels.append(t)

bars = []
for i in range(38):
    a = i * (2 * pi / 38)
    inner_r = 4.3
    outer_r = 4.8
    start = vec(inner_r * cos(a), 0.2, inner_r * sin(a))
    end = vec(outer_r * cos(a), 0.2, outer_r * sin(a))
    direction = norm(end - start)
    mid = (start + end) / 2
    length = mag(end - start)
    bar = box(pos=vec(mid.x, 0.01, mid.z), axis=direction, size=vec(length, 0.1, 0.14), color=color.white)
    bars.append(bar)

wheel = compound(pockets + labels + bars)

green_felt = cylinder(pos=vec(0, -0.601, 0), axis=vec(0, 0.01, 0), radius=30, color=vec(0, 0.3, 0))
ball = sphere(pos=vec(4.3, 0.05, 0), radius=0.1, color=color.white, make_trail=True, retain=5)

light_main = sphere(pos=vec(0, 5.5, 0), radius=0.6, color=vec(1, 0.8, 0.4), emissive=True)
light_side1 = sphere(pos=vec(3, 5.5, 3), radius=0.25, color=vec(1, 0.6, 0.2), emissive=True)
light_side2 = sphere(pos=vec(-3, 5.5, -3), radius=0.25, color=vec(1, 0.6, 0.2), emissive=True)
shadow_ring = ring(pos=vec(0, -0.599, 0), axis=vec(0, 1, 0), radius=5.3, thickness=0.4, color=vec(0.05, 0.05, 0.05), opacity=0.15)
casino_wall = cylinder(pos=vec(0, -5, 0), axis=vec(0, 10, 0), radius=30, color=vec(0.4, 0.05, 0.05), opacity=1)
casino_ceiling = box(pos=vec(0, 5, 0), size=vec(60, 0.2, 60), color=vec(0.2, 0.02, 0.02))

scene.camera.pos = vec(8, 4.8, 8)
scene.camera.axis = vec(-8, -4.3, -8)
scene.up = vec(0, 1, 0)


# UI elements
skip_spins = False
instant_finish = False

def toggle_skip():
    global skip_spins
    skip_spins = True

def finish_instant():
    global instant_finish
    instant_finish = True

scene.append_to_caption("\nHow many spins? ")
spin_input = winput(bind=None, prompt="Put number of spins and Enter")
scene.append_to_caption("\n")
skip_button = button(text="Finish Animations Normally", bind=toggle_skip)
scene.append_to_caption("\t             ")
finish_button = button(text="Finish It Already", bind=finish_instant)
scene.append_to_caption("\nRestart to do another simulation")

# Wait until user enters a value
while spin_input.text == "":
    rate(10)

spins = int(spin_input.text)


def wait(seconds):
    t = 0
    dt = 0.01
    while t < seconds:
        rate(1 / dt)
        t += dt

def logistic(r, X):
    return r*X*(1-X)

def isnan(x):
    return x != x

seed = random.uniform(0, 1.0)
r = 4

lower_bound = 0.4
upper_bound = 0.6

X = [seed]

def rng():
    global X, r
    if not isinstance(X, list) or len(X) == 0:
        X = [random.uniform(0, 1.0)]
    res = logistic(r, X[-1])
    if not (0 <= res <= 1) or isnan(res):
        res = random.uniform(lower_bound, upper_bound)
        X.append(res)
    elif lower_bound < res < upper_bound:
        X.append(res)
    tries = 0
    max_tries = 100
    while (res < lower_bound or res > upper_bound) and tries < max_tries:
        res = logistic(r, X[-1])
        if not (0 <= res <= 1) or isnan(res):
            res = random.uniform(lower_bound, upper_bound)
        X.append(res)
        tries += 1
    n = (res - lower_bound) / (upper_bound - lower_bound) * 38
    return int(max(0, min(37, n)))


def camera_position(progress, cam_ang, cont, ball_pos):
    r_start = 13
    r_end = 4.7
    y_start = 4.5
    y_end = 0.6
    r = r_start * (1 - cont) + r_end * cont
    y = y_start * (1 - cont) + y_end * cont + 0.4 * sin(3 * pi * progress)
    x = r * cos(cam_ang)
    z = r * sin(cam_ang)
    return vec(x, y, z)

def spin():
    if instant_finish:
        idx = rng()
        final_ang = idx * (2 * pi / 38) + (pi / 38)
        ball.pos = vec(4.3 * cos(final_ang), 0.05, 4.3 * sin(final_ang))
        return idx

    t = 0
    max_time = 6
    dt = 0.01
    wheel_vel = 0.015
    ang = 0
    vel = 0.12
    ball_r = 4.3
    ball_y = 0.05
    idx = rng()
    final_ang = idx * (2 * pi / 38) + (pi / 38)
    total_rot = 0
    easing = False
    ease_time = 0
    ease_dur = max_time * 0.4
    ease_vel = 0
    ease_acc = 0

    while t < max_time:
        if skip_spins:
            break
        rate(1 / dt)
        t += dt
        prog = t / max_time
        total_rot += wheel_vel
        wheel.rotate(angle=wheel_vel, axis=vec(0, 1, 0), origin=vec(0, 0, 0))
        if not easing and prog >= 0.6:
            easing = True
            ease_time = 0
            curr = ang % (2 * pi)
            tgt = final_ang % (2 * pi)
            if tgt < curr:
                tgt += 2 * pi
            diff = tgt - curr
            ease_vel = vel
            ease_acc = 2 * (diff - ease_vel * ease_dur) / (ease_dur ** 2)
        if not easing:
            vel *= 0.992
            ang += vel
        else:
            ang += ease_vel * dt + 0.5 * ease_acc * dt * dt
            ease_vel += ease_acc * dt
            ease_time += dt
        ball.pos = vec(ball_r * cos(ang), ball_y, ball_r * sin(ang))
        cont = min(1, max(0, (prog - 0.6) / 0.4))
        cam_ang = (1 - cont) * (2 * pi * prog) + cont * ang
        cam_pos = camera_position(prog, cam_ang, cont, ball.pos)
        focus = vec(0, 0, 0) * (1 - cont) + ball.pos * cont * 0.6
        scene.center = focus + vec(0, 0.5 * cont, 0)
        scene.forward = norm(focus - cam_pos + vec(0, -0.9 * cont, 0))
        scene.up = vec(0, 1, 0)
        scene.range = 6 - 2.2 * cont

    wheel.rotate(angle=-total_rot, axis=vec(0, 1, 0), origin=vec(0, 0, 0))
    ball.pos = vec(ball_r * cos(final_ang), ball_y, ball_r * sin(final_ang))
    if not skip_spins:
        wait(0.5)
    else:
        wait(.0001)
    return idx

bar_chart = graph(title='Live Slot Frequency', xtitle='Slot #', ytitle='Lands')
bars = gvbars(delta=0.5)
land_counts = {}

for _ in range(spins):
    result = spin()
    if result not in land_counts:
        land_counts[result] = 1
    else:
        land_counts[result] += 1
    bars.plot(result, land_counts[result])
    
    
    
def distribution(n, b):
     bell_graph = graph(title = f'Distribution of Averaged Slot Rolls (Batch Size: {b})', xtitle = "Average Slot #", ytitle = "Frequency")
     bell_bars = gvbars(delta=0.5)
     
     freq = {i * 0.5: 0 for i in range(0, int(37 / 0.5))}
     
     for i in range(n):
         sum = 0
         for j in range(b):
             sum += rng()
             
         mean = sum / b
         mean = int(mean * 2) / 2.0
         
         
         if(mean not in freq):
             freq[mean] = 1
         else:
             freq[mean] += 1
                 
     for key in freq:
         bell_bars.plot(key, freq[key] / n)

def simulate_and_stats(n):
    values = []
    for i in range(n):
        values.append(rng())
    
    mean = sum(values) / n
    
    variance = sum((x - mean) ** 2 for x in values) / n
    std_dev = sqrt(variance)
    
    print(f"Mean: {mean}")
    print(f"Standard Deviation: {std_dev}")
    
    return mean, std_dev
    
    
simulate_and_stats(spins)
distribution(spins, 20)