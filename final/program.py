 Web VPython 3.2

""" 
Read Me:
Our program simulates gas particles moving around within an enclosed cylindrical 
volume. Counting the number of collisions happening per second, it calculates a
unitless 'pressure' that is displayed on the gauge. To use our program, select a
number of particles you want to spawn, click spawn particles, and then watch as
they bounce around. You can also click clear to despawn all of the balls. You 
can also dynamically adjust the volume of the cylinder and the temperature, which
affects the speed of the particles, to see how they impact the behavior of the 
system. By clicking one of the check boxes next to either the temperature or 
volume, you can isolate that variable and begin graphing how that variable 
affects the pressure. Isolating the variables is necessary because if you are 
trying to plot pressure vs volume or temperature, changing the other will change
the pressure without changing the variable being graphed. Once isolated, it
will begin to plot the values onto a graph to demonstrate the ideal gas law. 
Once you stop isolating the variables and then isolate a variable again, it will
clear the graphs to prevent the same issue. 
"""

import random

scene = canvas(background=vec(.8, .9, 1))
scene.userzoom = True
scene.userspin = False
scene.userpan = False

collisioncount = 0
volume = 1000
heat = 2

scene.append_to_caption("\n Volume = ")
displayvolume = wtext(text = volume)
scene.append_to_caption(" meters ^3\n")
#displayvolume = wtext(text = volume)
#scene.append_to_caption(" meters ^3\n")

#displayvolume.text = volume

r = findr(volume)

piston = cylinder(pos = vec(0, -1.5*r, 0), axis = vec(0, 2.5*r, 0), radius = r, color=color.white, opacity = 0.4, emmisive = True)

volSlider = slider(bind = setVolume, min = 1000, max = 200000, value = volume, step = 1, length = 300, width = 13, left = 5, top = 10, bottom = 10)

scene.append_to_caption("\nHeat\n")

heatSlider = slider(bind = setHeat, min = 0.001, max = 6, value = 2, step = 0.05, length = 300, width = 13, left = 5, top = 10, bottom = 10)

scene.append_to_caption("\n\nIsolation Mode: ")
def update_isolation_choice():
    pass  # dummy function, required by menu bind

isolation_menu = menu(bind=update_isolation_choice, choices=["None", "Isolate Volume", "Isolate Temperature", "Isolate Particles"])

pressure_plot = gcurve(color=color.red)
x_axis_label = label(pos=vec(8, -5, 0), text="Variable Value", height=12, box=False)
y_axis_label = label(pos=vec(4, 5, 0), text="Pressure", height=12, box=False, align="center")


def begin_isolation():
    global isolation_mode, isolation_values, isolation_index
    isolation_mode = isolation_menu.selected
    isolation_index = 0
    pressure_plot.delete()
    set_ui_enabled(False)
    
    if isolation_mode == "Isolate Volume":
        isolation_values = list(range(1000, 10001, 250))
        x_axis_label.text = "Volume (m^3)"
    elif isolation_mode == "Isolate Temperature":
        isolation_values = [round(x * 0.1, 1) for x in range(5, 51, 2)]
        x_axis_label.text = "Temperature (T)"
    elif isolation_mode == "Isolate Particles":
        isolation_values = list(range(1, 51, 2))
        x_axis_label.text = "Particle Count"
    else:
        x_axis_label.text = "Variable Value"
        set_ui_enabled(True)

def findr(v):
    return pow((v / (2*pi)), (1/3))

def updPiston(r):
    piston.pos = vec(0, -1.5*r, 0)
    piston.axis = vec(0, 2.5*r, 0)
    piston.radius = r


def setVolume():
    global volume
    oldVolume = volume
    volume = volSlider.value
#    displayvolume.text = volume
    r = findr(volume)
    for object in objects:
#        object.pos *= (volume / oldVolume) ** 1/3
        object.pos *= pow((volume / oldVolume), 1/3)
    updPiston(r)
    gauge.pos *= pow((volume / oldVolume), 1/3)
    gauge.size *= pow((volume / oldVolume), 1/3)
    lab.pos.x = -r
    
def setHeat():
    global heat
    global avgVelocity
    
    newHeat = heatSlider.value
    for object in objects:
        object.vel *= newHeat / heat
    
    avgVelocty = newHeat
    heat = newHeat

objects = []

def spawn_particle():
    global objects
    
    for i in range(spawn_quantity):
        particle = sphere(pos = vec(0,0,0))
        max_diff = min(heat, 0.5)
        speed = random.uniform(heat - max_diff, heat + max_diff)
        particle.vel = vector.random() / 5 * speed
        particle.mass = 1
        particle.color = color.blue
        particle.emissive = True
        particle.radius = 0.2
        
        objects.append(particle)
        particle_count.text = len(objects)
    
spawn_quantity = 1

def set_spawn_quantity():
    global spawn_quantity
    
    spawn_quantity = int(set_spawn_menu.selected)
    
scene.append_to_caption("\n Particle Count:")
particle_count = wtext(text = len(objects))
scene.append_to_caption("\n")

set_spawn_menu = menu(bind=set_spawn_quantity, choices=[1,5,10,15,20])
    
spawn = button(bind=spawn_particle, text = "Spawn particle")
clear = button(bind=clear, text = "Clear")


def move(objects):
    for object in objects:
        object.pos += object.vel

def collision(objects):
    for obj1 in objects:
        container_collision(obj1)
        for obj2 in objects:
            if(obj1 != obj2):
                sphere_sphere_collision(obj1, obj2)

def sphere_sphere_collision(s1, s2):
    dist = mag(s1.pos - s2.pos)
    
    if dist < s1.radius + s2.radius:

        n = norm(s1.pos - s2.pos)
        
        v_rel = s1.vel - s2.vel
        vel_along_normal = dot(v_rel, n)
        
        if vel_along_normal > 0:
            return
        
        m1 = s1.mass
        m2 = s2.mass
        
        impulse = (2 * vel_along_normal) / (m1 + m2)
        
        s1.vel = s1.vel - (impulse * m2) * n
        s2.vel = s2.vel + (impulse * m1) * n
    
def container_collision(obj):
    global collisioncount
    #x_z collision
    
    dx = obj.pos.x - piston.pos.x
    dz = obj.pos.z - piston.pos.z
    
    
    dist_squared = (dx*dx + dz*dz)
    boundary = (piston.radius - obj.radius - 0.2)**2

    if dist_squared > boundary:
        
        normal_vec = norm(vec(dx, 0, dz))
    
        dot_vec = dot(obj.vel, normal_vec)
        
        obj.vel.x = obj.vel.x - 2 * dot_vec * normal_vec.x
        obj.vel.z = obj.vel.z - 2 * dot_vec * normal_vec.z
        
        dist = sqrt(dist_squared)
        overlap = dist - (piston.radius - obj.radius - 0.2)
        obj.pos.x -= normal_vec.x * overlap
        obj.pos.z -= normal_vec.z * overlap
        
        collisioncount+=1
        
        
    #y collision
    if obj.vel.y > 0 and obj.pos.y > piston.pos.y + piston.radius * 2.5 - obj.radius - 0.15:
        obj.vel.y *= -1
        collisioncount+=1
        
    if obj.vel.y < 0 and obj.pos.y < piston.pos.y + obj.radius + 0.15:
        obj.vel.y *= -1
        collisioncount += 1

def clear():
    global objects
    global collisioncount
    
    for object in objects:
        object.visible = False
    objects = []
    particle_count.text = 0
    collisioncount = 0


gauge = []
needle = None
def draw_gauge(init_pos):
    global gauge
    global needle
    
    backing = cylinder(pos = init_pos + vec(0,0,0), axis=vec(0,0,1), length = 0.05, radius = 4, emissive = True)
    needle = cylinder(pos=init_pos, axis=vec(-1,0,0), length = 3, radius = 0.1, color = color.red, emissive = True)
    
    gauge = compound([backing, needle], pos=init_pos)
    
    

draw_gauge(vec(10,0,0))    



pressure = 0
lab = label(pos=vec(-piston.radius, 0, 0), text=pressure, xoffset=-60, yoffset=50, space=0, height=16, border=4, font='sans', background = vec(0,0,0))

isolation_mode = "None"
isolation_index = 0
isolation_values = []
def set_ui_enabled(state):
    volSlider.disabled = not state
    heatSlider.disabled = not state
    spawn.disabled = not state
    clear.disabled = not state
    set_spawn_menu.disabled = not state
def begin_isolation():
    global isolation_mode, isolation_values, isolation_index
    isolation_mode = isolation_menu.selected
    isolation_index = 0
    pressure_plot.delete()
    set_ui_enabled(False)
    
    if isolation_mode == "Isolate Volume":
        isolation_values = list(range(1000, 10001, 250))
    elif isolation_mode == "Isolate Temperature":
        isolation_values = [round(x * 0.1, 1) for x in range(5, 51, 2)]
    elif isolation_mode == "Isolate Particles":
        isolation_values = list(range(1, 51, 2))
    else:
        set_ui_enabled(True)
def apply_isolation_step():
    global volume, heat, spawn_quantity
    value = isolation_values[isolation_index]
    
    if isolation_mode == "Isolate Volume":
        old_volume = volume
        volume = value
        volSlider.value = value
        r = findr(volume)
        updPiston(r)
        for o in objects:
            o.pos *= pow((volume / old_volume), 1/3)
        gauge.pos *= pow((volume / old_volume), 1/3)
        gauge.size *= pow((volume / old_volume), 1/3)
        lab.pos.x = -r
        displayvolume.text = volume
        
    elif isolation_mode == "Isolate Temperature":
        for obj in objects:
            obj.vel *= value / heat
        heatSlider.value = value
        heat = value
        
    elif isolation_mode == "Isolate Particles":
        clear()
        spawn_quantity = value
        spawn_particle()

def wait_for_pressure_step():
    global smoothed_pressure, timer, collisioncount
    timer = 0
    smoothed_pressure = None
    t = 0
    interval = raw_pressure_interval
    while t < 1.0:
        rate(1 / dt)
        move(objects)
        collision(objects)
        raw = collisioncount / (interval * volume)
        if smoothed_pressure is None:
            smoothed_pressure = raw
        smoothed_pressure = alpha * raw + (1 - alpha) * smoothed_pressure
        collisioncount = 0
        t += interval
    return smoothed_pressure


timer = 0
dt = 0.01
raw_pressure_interval = 0.01
smoothed_pressure = None
alpha = 0.05
while True:
    rate(1/dt)
    global pressure
    move(objects)
    collision(objects)
    
    
    timer += dt
    
    if(timer > raw_pressure_interval):
        timer = 0
        raw_pressure = collisioncount / (raw_pressure_interval * volume)
#        print(raw_pressure)
        if(not smoothed_pressure):
            smoothed_pressure = raw_pressure
        smoothed_pressure = alpha * raw_pressure + (1 - alpha) * smoothed_pressure
        collisioncount = 0
        
        lab.text = round(smoothed_pressure, 2)
    
#    print(smoothed_pressure)
    if(smoothed_pressure):
        gauge.axis.x = cos( smoothed_pressure / 6 * pi ) * 3
        gauge.axis.y = sin( smoothed_pressure / 6 * pi ) * -3
        
    if isolation_menu.selected != isolation_mode and isolation_menu.selected != "None":
        begin_isolation()

    if isolation_mode != "None":
        if isolation_index < len(isolation_values):
            apply_isolation_step()
            pres = wait_for_pressure_step()
            pressure_plot.plot(isolation_values[isolation_index], pres)
            isolation_index += 1
        else:
            pressure_plot.delete()
            isolation_mode = "None"
            isolation_menu.selected = "None"
            set_ui_enabled(True)
