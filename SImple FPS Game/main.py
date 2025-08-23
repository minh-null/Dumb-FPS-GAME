from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.first_person_controller import FirstPersonController
from random import uniform
import pygame
from json import load, dump
from enum import Enum, auto, IntEnum
import os
import sys
from dataclasses import dataclass, field
from typing import Optional, Any
import networkx as nx
import datetime

if getattr(sys, "frozen", False): #Rip som ;-; (atleast its python version)
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

app = Ursina()

ground = Entity(
    model='cube', 
    texture='grass', 
    collider='box', 
    scale=(50,1,50))

wall = Entity(model='cube', color=color.azure, scale=(2,2,2), position=(5,1,5), collider='box')
wall2 = Entity(model='cube', color=color.orange, scale=(2,3,1), position=(-3,1.5,2), collider='box')
tree = Entity(model='tree.obj', texture='tree.png', scale=2, position=(3,0,3), collider='box')

player = FirstPersonController()

gun_holder = Entity(parent=camera, position=(1,-0.75,1.5))
gun = Entity(
    parent=gun_holder,
    model='Glock17.obj',
    scale=0.2,
    rotation=(5,-180,0),
    shader=lit_with_shadows_shader,
    normal_map='Glock17_Normal.png',
    roughness_map='Glock17_Roughness.png',
    metallic_map='Glock17_Metalness.png'
)

gun_origin_pos = gun_holder.position
gun_origin_rot = gun_holder.rotation

fire_rate = 0.15
time_since_last_shot = 0

def shoot():
    time = datetime.datetime.now().strftime("%H-%M-%S")
    print(str(time), "Bang!")
    bullet = Entity(model='cube', color=color.azure, scale=(2,2,2), collider='box')
    bullet_origin_pos = (5, 10, 5)
    
def update():
    time = datetime.datetime.now().strftime("%H-%M-%S")
    if held_keys['escape']:
        print(str(time), "player press _escape_")
        application.quit()

    player.speed = 5
    if held_keys['w']:
        print(str(time), "player press _w_" )
        
    if held_keys['a']:
        print(str(time), "player press _a_" )
        
    if held_keys['s']:
        print(str(time), "player press _s_" )
        
    if held_keys['d']:
        print(str(time), "player press _d_" )
        
    if held_keys['control']:
        player.speed = 7
        print(str(time), "player press _control_" )
        
    if held_keys["space"]:
        player.jump_height = 3
        print(str(time), "player press _space_" )
        if held_keys['control']:
            player.jump_height = 5
            print(str(time), "player press _space_ & _control_" )

def input(key):
    if key == 'left mouse down':
        print("player press _left-mouse-button_" )
        shoot()

app.run()