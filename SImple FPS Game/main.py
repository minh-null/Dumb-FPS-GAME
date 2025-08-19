from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.first_person_controller import FirstPersonController

import os
import sys
from random import uniform

if getattr(sys, "frozen", False):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
else:
    base_path = os.path.dirname(os.path.abspath(__file__))


def update():
    #frame
    if held_keys['escape']:
        application.quit()
    
    #Movement thing :33
    if held_keys['control']:
        player.speed = 10
    else:
        player.speed = 5
        
    if held_keys["space"]:
        player.jump_height = 5
    
    if mouse.left:
        shoot()

app = Ursina()

ground = Entity(
    model='cube', 
    texture='grass', 
    collider='box', 
    scale=(50,1,50))

#=========================Objekt and Maps============================
wall = Entity(model='cube', color=color.azure, scale=(2,2,2), position=(5,1,5), collider='box')
wall2 = Entity(model='cube', color=color.orange, scale=(2,3,1), position=(-3,1.5,2), collider='box')

tree = Entity(
    model='tree.obj',
    texture='tree.png', 
    scale=2,
    position=(3,0,3),
    collider='box'
)

gun = Entity(
    parent=camera,
    model='Glock17.obj',
    scale=0.2,
    position=(1, -0.75, 1.5),
    rotation=(5, -180, 0),
    shader=lit_with_shadows_shader,
    normal_map='Glock17_Normal.png',
    roughness_map='Glock17_Roughness.png',
    metallic_map='Glock17_Metalness.png'
)

gun.always_on_top = True

gun_origin_pos = gun.position
gun_origin_rot = gun.rotation

def shoot():
    random_yaw = uniform(-2, 2)   # yaw <-->
    random_pitch = uniform(3, 6)  # pitch up-down

    gun.animate_rotation((gun_origin_rot[0] + random_pitch,
                          gun_origin_rot[1] + random_yaw,
                          gun_origin_rot[2]),
                         duration=0.05, curve=curve.out_expo)

    gun.animate_rotation(gun_origin_rot,
                         duration=0.2, delay=0.05, curve=curve.in_out_quint)

    gun.animate_position((gun_origin_pos[0],
                          gun_origin_pos[1],
                          gun_origin_pos[2] - 0.2),
                         duration=0.05, curve=curve.out_expo)

    gun.animate_position(gun_origin_pos,
                         duration=0.2, delay=0.05, curve=curve.in_out_quint)
    
    

#====================================================================


#Light
DirectionalLight().look_at(Vec3(1,-1,-1))

#player
player = FirstPersonController()

app.run()
