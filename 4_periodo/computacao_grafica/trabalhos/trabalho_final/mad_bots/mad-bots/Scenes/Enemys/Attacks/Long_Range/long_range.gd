extends Node2D

@onready var cooldown = $Cooldown_timer        # Timer to manage attack cooldowns
@onready var player = get_tree().get_first_node_in_group("player")
@onready var marker = $Marker2D
@onready var delay_timer = $DelayTimer

@export var projectile_scene: PackedScene
@export var fire_rate: float = 1.5
@export var damage: int = 10
@export var pierce: int = 1
@export var attack_range: float = 500.0
@export var projectile_speed: float = 300.0
@export var knockback_amount: float = 0.0



var can_attack: bool = true
func start_attack(target_position: Vector2) -> void:
	var target_direction = (target_position - marker.global_position).normalized()
	can_attack = false
	delay_timer.start()
	await delay_timer.timeout 
	var projectile_instance = projectile_scene.instantiate()
	get_tree().root.add_child(projectile_instance)
	projectile_instance.global_position = marker.global_position
	projectile_instance.damage = damage
	projectile_instance.direction = target_direction
	projectile_instance.pierce = pierce
	projectile_instance.range_travel = attack_range
	projectile_instance.speed = projectile_speed
	projectile_instance.knockback_amount = knockback_amount
	projectile_instance.rotation  = target_direction.angle()
	cooldown.start(fire_rate)
	
func _on_cooldown_timer_timeout() -> void:
	can_attack = true
	pass # Replace with function body.
