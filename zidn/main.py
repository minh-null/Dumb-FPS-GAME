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
from lib.bullet import Bullet

if getattr(sys, "frozen", False): #Rip som ;-; (atleast its python version)
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

app = Ursina()

random.seed(0)
Entity.default_shader = lit_with_shadows_shader

ground = Entity(
    model='cube', 
    texture='grass', 
    collider='box', 
    scale=(50,1,50))

wall = Entity(model='cube', color=color.azure, scale=(2,2,2), position=(5,1,5), collider='box')
wall2 = Entity(model='cube', color=color.orange, scale=(2,3,1), position=(-3,1.5,2), collider='box')
tree = Entity(model='tree.obj', texture='tree.png', scale=2, position=(3,0,3), collider='box')

editor_camera = EditorCamera(enabled=False, ignore_paused=True)
player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8, collider='box')
player.collider = BoxCollider(player, Vec3(0,1,0), Vec3(1,2,1))

#Ursina docs
gun = Entity(model='cube', parent=camera, position=(.5,-.25,.25), scale=(.3,.2,1), origin_z=-.5, color=color.red, on_cooldown=False)
gun.muzzle_flash = Entity(parent=gun, z=1, world_scale=.5, model='quad', color=color.yellow, enabled=False)

shootables_parent = Entity()
mouse.traverse_target = shootables_parent

shootables_parent = Entity()
mouse.traverse_target = shootables_parent

for i in range(16):
    Entity(model='cube', origin_y=-.5, scale=2, texture='brick', texture_scale=(1,2),
        x=random.uniform(-8,8),
        z=random.uniform(-8,8) + 8,
        collider='box',
        scale_y = random.uniform(2,3),
        color=color.hsv(0, 0, random.uniform(.9, 1))
        )

def shoot():
    if not gun.on_cooldown:
        gun.on_cooldown = True
        gun.muzzle_flash.enabled = True

        # sound fx
        from ursina.prefabs.ursfx import ursfx
        ursfx([(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)], 
              volume=0.5, wave='noise', pitch=random.uniform(-13,-12), pitch_change=-12, speed=3.0)
        # reset cooldown
        invoke(gun.muzzle_flash.disable, delay=0.05)
        invoke(setattr, gun, 'on_cooldown', False, delay=0.2)

        # spawn bullet in front of camera
        Bullet(
            position=gun.world_position + gun.forward * 0.6,
            direction=camera.forward,
            speed=40
        )
        
from ursina import Entity, Vec3, color, time, destroy

class Enemy(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=shootables_parent, model='cube', scale_y=2, origin_y=-.5, color=color.light_gray, collider='box', **kwargs)
        self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.red, world_scale=(1.5,.1,.1))
        self.max_hp = 100
        self.hp = self.max_hp

    def update(self):
        dist = distance_xz(player.position, self.position)
        if dist > 40:
            return

        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)


        self.look_at_2d(player.position, 'y')
        hit_info = raycast(self.world_position + Vec3(0,1,0), self.forward, 30, ignore=(self,))
        # print(hit_info.entity)
        if hit_info.entity == player:
            if dist > 2:
                self.position += self.forward * time.dt * 5

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        if value <= 0:
            destroy(self)
            return

        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1

# Enemy()
enemies = [Enemy(x=x*4) for x in range(4)] #Ursina docs
    
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

def input(key):
    if key == 'left mouse down':
        print("player press _left-mouse-button_" )
        shoot()
        
def pause_input(key): #Ursina docs
    if key == 'tab':    # press tab to toggle edit/play mode
        time = datetime.datetime.now().strftime("%H-%M-%S")
        print(str(time, "Player press _TAB_"))
        editor_camera.enabled = not editor_camera.enabled

        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        gun.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position

        application.paused = editor_camera.enabled

pause_handler = Entity(ignore_paused=True, input=pause_input) #Ursina docs

sun = DirectionalLight() #Ursina docs
sun.look_at(Vec3(1,-1,-1))
Sky()

#UI
Button(
    text='sh', 
    parent=camera.ui, 
    model=Default, 
    radius=0.1, 
    origin=(3, 0), 
    text_origin=(0, 0), 
    text_size=0.5, 
    text_color=Default, 
    color=Default, 
    collider='box', 
    highlight_scale=1, 
    pressed_scale=1, 
    disabled=False
    )

app.run()