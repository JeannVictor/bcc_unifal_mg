extends CharacterBody2D
class_name Enemy

# Node references
@onready var experience_gem_scene : PackedScene = preload("res://Scenes/Objects/experience_gem.tscn")
@onready var health_drop_scene : PackedScene = preload("res://Scenes/Objects/health_drop.tscn")

@onready var hurtbox = $HurtBox  # Hurtbox area
@onready var player = get_tree().get_first_node_in_group("player")  # Get player reference from group
@onready var collision_shape = $CollisionShape2D

@export var attack_path : NodePath  ## Path to the attack system node
@onready var attack = get_node(attack_path)  # Reference to attack system

@export var animation_path : NodePath
@onready var animation = get_node(animation_path)   # Animation controller

# Enemy properties
@export var speed: float   ## Movement speed
@export var max_health: int  ## Maximum health points the enemy can have
@export var drop_reward: int  ## Experience given to player upon defeat
@export var invincibility_time: float  ## Time the enemy is invincible after being hit


var direction_to_player : Vector2 = Vector2.ZERO  # Direction towards player
var current_health: int  # Current health points (starts at max health)
var init_knockback: Vector2 = Vector2.ZERO
var current_knockback: Vector2 = Vector2.ZERO  # Stores the current knockback force applied to the enemy
var knockback_recovery: float  ## How quickly knockback force decays (higher = faster recovery)
var knockback_cummulative_recovery: float = 0.0


func _ready() -> void:
	knockback_recovery = 1.0 / invincibility_time
	current_health = max_health
	# Connect the hurt signal from the hurtbox to our damage processing function
	hurtbox.hurt.connect(hurt)
	# Connect the death animation finished signal to queue_free the enemy
	animation.death_animation_finished.connect(_on_dead)
	hurtbox.invincibility_time = invincibility_time

func _physics_process(delta : float) -> void:
	if not player:
		return  # Exit if player is not found

	# Calculate direction to player every frame
	direction_to_player = (player.global_position - global_position)
	move_or_attack(delta)


func move_or_attack(delta : float):
	var distance_to_player = direction_to_player.length()
	direction_to_player = direction_to_player.normalized()
	

	velocity = Vector2.ZERO
	if current_knockback != Vector2.ZERO:
		# Apply knockback in invincibility time
		# Ex.: if knockback = 100, travel 100 pixels in invincibility_time seconds
		knockback_cummulative_recovery += delta * knockback_recovery
		current_knockback = init_knockback.lerp(Vector2.ZERO, knockback_cummulative_recovery)
		
		# Play hit animation when knockback is active
		animation.custom_play("taking_damage")
		velocity = current_knockback  # Override movement with knockback force

		move_and_slide()
		return  # Skip further movement/attack processing while being knocked back

	elif attack.can_attack:
		# Attack when in range
		animation.custom_play("attack")
		attack.start_attack(player.global_position)

	elif animation.can_play_new_animation:
		# Move towards player	
		velocity = speed * direction_to_player
		animation.process_sprite()
		animation.custom_play("walk")	
		move(distance_to_player)

func move(_distance_to_player: float) -> void:
	move_and_slide()
		

func hurt(damage, direction, knockback_amount, attackerPosition) -> void:
	if (direction == Vector2.ZERO):
		direction = (global_position - attackerPosition).normalized()
	# Apply damage to player's health
	current_health -= damage
	
	# Calculate and apply knockback force in the specified direction
	init_knockback = direction * knockback_amount
	
	# It just works better this way
	init_knockback *= 2/invincibility_time 

	current_knockback = init_knockback
	knockback_cummulative_recovery = 0.0


	if current_health <= 0:
		attack.can_attack = false
		collision_shape.call_deferred("set","disabled",true)
		animation.custom_play("death")


func _on_dead():
	var rand = randi() % 100
	if rand < 97:
		var gem = experience_gem_scene.instantiate()
		gem.experience = drop_reward
		gem.global_position = global_position
		get_tree().root.add_child(gem)

	else:
		var health_drop = health_drop_scene.instantiate()
		health_drop.experience = drop_reward
		health_drop.global_position = global_position
		get_tree().root.add_child(health_drop)

		
	queue_free()

		
