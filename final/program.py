Web VPython 3.2

import random

scene = canvas(background=vec(.8, .9, 1))

collisioncount = 0
volume = 1000
heat = 2
scene.append_to_caption("\n Collision Count = ")
counter = wtext(text=collisioncount)
scene.append_to_caption("\n Volume = ")
displayvolume = wtext(text = volume)
scene.append_to_caption(" meters ^3\n")

displayvolume.text = volume

r = findr(volume)

piston = cylinder(pos = vec(0, -1.5*r, 0), axis = vec(0, 2.5*r, 0), radius = r, color=color.white, opacity = 0.4, emmisive = True)

volSlider = slider(bind = setVolume, min = 1000, max = 200000, value = volume, step = 1, length = 300, width = 13, left = 35, top = 10, bottom = 10)
scene.append_to_caption("\n")
heatSlider = slider(bind = setHeat, min = 0.1, max = 3, value = 2, step = 0.05, length = 300, width = 13, left = 35, top = 10, bottom = 10)

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
    displayvolume.text = volume
    r = findr(volume)
    for object in objects:
#        object.pos *= (volume / oldVolume) ** 1/3
        object.pos *= pow((volume / oldVolume), 1/3)
    updPiston(r)
    
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
        speed = random.uniform(heat - 0.5, heat + 0.5)
        particle.vel = vector.random() / 5 * speed
        particle.mass = 1
        particle.color = color.blue
        particle.emissive = True
        particle.radius = 0.2
        
        objects.append(particle)
    
spawn_quantity = 1

def set_spawn_quantity():
    global spawn_quantity
    
    spawn_quantity = int(set_spawn_menu.selected)
    
scene.append_to_caption('\n\n')

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
    
    collisioncount = 0


gauge = None
def draw_gauge():
    global gauge
    gauge = cylinder(pos=vec(10,-2,0), axis=vec(1,0,0), length = 3, radius = 0.1, color = color.red)

draw_gauge()    

pressure = None


timer = 0
dt = 0.01
raw_pressure_interval = 0.05
smoothed_pressure = None
alpha = 0.1
while True:
    rate(1/dt)
    global pressure
    move(objects)
    collision(objects)
    counter.text = collisioncount
    timer += dt
    
    if(timer > raw_pressure_interval):
        timer = 0
        raw_pressure = collisioncount / (raw_pressure_interval * volume)
#        print(raw_pressure)
        if(not smoothed_pressure):
            smoothed_pressure = raw_pressure
        smoothed_pressure = alpha * raw_pressure + (1 - alpha) * smoothed_pressure
        collisioncount = 0
    
    print(smoothed_pressure)
    if(smoothed_pressure):
        gauge.axis.x = cos( smoothed_pressure / 2.5 * pi ) * -3
        gauge.axis.y = sin( smoothed_pressure / 2.5 * pi ) * 3
