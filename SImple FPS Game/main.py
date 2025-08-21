from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.first_person_controller import FirstPersonController
from random import uniform

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
    random_yaw = uniform(-4, 4)    
    random_pitch = uniform(10, 15)  

    gun_holder.animate_rotation(
        Vec3(gun_origin_rot.x + random_pitch,
             gun_origin_rot.y + random_yaw,
             gun_origin_rot.z),
        duration=0.08, curve=curve.out_expo
    )
    gun_holder.animate_rotation(gun_origin_rot, duration=0.2, delay=0.1, curve=curve.in_out_quint)

    gun_holder.animate_position(
        Vec3(gun_origin_pos.x, gun_origin_pos.y, gun_origin_pos.z - 0.7),
        duration=0.05, curve=curve.out_expo
    )
    gun_holder.animate_position(gun_origin_pos, duration=0.2, delay=0.1, curve=curve.in_out_quint)

    print("Bang!")

def update():
    global time_since_last_shot
    time_since_last_shot += time.dt

    if held_keys['escape']:
        print("player press _escape_" )
        application.quit()

    player.speed = 5
    
    if held_keys['control']:
        player.speed = 7
        print("player press _control_" )
    if held_keys["space"]:
        player.jump_height = 3
        print("player press _space_" )
        if held_keys['control']:
            player.jump_height = 5
            print("player press _space_ & _control_" )


def input(key):
    if key == 'left mouse down':
        print("player press _left-mouse-button_" )
        shoot()

app.run()