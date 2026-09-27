extends Resource

class_name Spawn_info

@export var time_start:int ## Time to start spawning this enemy
@export var time_end:int ## Time to stop spawning this enemy
@export var enemy:Resource ## The enemy to spawn
@export var enemy_num:int ## The number of enemies to spawn per spawn cycle
@export var enemy_spawn_delay:int ##The delay between enemy spawns

var spawn_delay_counter = 0
