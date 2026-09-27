extends CharacterBody2D
class_name Player

# Node Paths - These export variables allow you to assign nodes in the inspector
@export var animationPlayer_path : NodePath  ## Path to the AnimationPlayer node that controls player animations
@onready var animation = get_node(animationPlayer_path)  # Reference to the AnimationPlayer

@export var hurtbox_path : NodePath  ## Path to the Hurtbox area node that detects incoming attacks
@onready var hurtbox = get_node(hurtbox_path)  # Reference to the Hurtbox area

@export var attack_path : NodePath  ## Path to the attack system node
@onready var gunsOrbiter = get_node(attack_path)  # Reference to attack system

@export var grab_area : NodePath  ## Path to the area used for grabbing items
@onready var grabArea = get_node(grab_area)  # Reference to the grab

#GUI
@onready var expBar = get_node("%ExperienceBar")  # Reference to the experience bar GUI element
@onready var healthbar = get_node("%Healthbar") # Reference to the health bar GUI element
@onready var levelPanel = get_node("%LevelUp")  # Reference to the level-up panel GUI element
@onready var damage_popup_layer = get_node("%DamagePopupLayer") as ColorRect  # Reference to the damage popup layer
@onready var fps_label = get_node("%FpsLabel")  # Reference to the FPS label in the main scene

# Player Stats - Configurable properties that can be adjusted in the inspector
@export var player_velocity_init: int = 200  ## Base movement speed of the player in pixels per second
@export var pickup_range_init: float = 100  ## Range within which the player can pick up items
@export var max_health: int = 1000  ## Maximum health points the player can have
@export var initial_gun: String = "Futuristic Chicago"  ## Name of the initial gun to equip
@export var invincibility_time: float = 0.5  ## Time the player is invincible after being hit
var player_velocity: int
var pickup_range: float

var current_health
var atributtes_percentage : Dictionary = { # Dictionary to track percentage-based upgrades
	"player_velocity" : 1.0,
	"pickup_range" : 1.0,
	"fire_rate" : 1.0,
	"fire_range" : 1.0,
	"knockback_amount" : 1.0,
	"damage" : 1.0,
	"projectile_speed" : 1.0,
	"pierce": 0.0,
	"explosion_size": 1.0
}

var init_knockback: Vector2 = Vector2.ZERO
var current_knockback: Vector2 = Vector2.ZERO  # Stores the current knockback force applied to the enemy
var knockback_recovery: float  ## How quickly knockback force decays (higher = faster recovery)
var knockback_cummulative_recovery: float = 0.0


# "Futuristic Chicago": preload("res://Scenes/Player/Guns/futuristic_chicago.tscn"), # Corrected file path
# 		"Rocket Launcher": preload("res://Scenes/Player/Guns/rocket_launcher.tscn"), # Corrected file path
# 		"Desert Sniper": preload("res://Scenes/Player/Guns/desert_sniper.tscn"),
# 		"M45": preload("res://Scenes/Player/Guns/m_45.tscn"),
# 		"F547": preload("res://Scenes/Player/Guns/f_547.tscn"),
# 		"K6554": preload("res://Scenes/Player/Guns/k_6554.tscn"),
# 		"RRR7": preload("res://Scenes/Player/Guns/rrr_7.tscn"),
# 		"T58": preload("res://Scenes/Player/Guns/t_58.tscn"),
# 		"G65": preload("res://Scenes/Player/Guns/g_65.tscn")
func _ready() -> void:
	player_velocity = player_velocity_init
	pickup_range = pickup_range_init
	hurtbox.hurt.connect(hurt)
	grabArea.get_child(0).shape.radius = pickup_range
	healthbar.init_health(max_health)
	current_health = max_health
	knockback_recovery = 1.0 / invincibility_time
	hurtbox.invincibility_time = invincibility_time
	gunsOrbiter.add_gun(initial_gun, atributtes_percentage)

func _physics_process(delta: float) -> void:
	fps_label.text = "FPS: %d" % Engine.get_frames_per_second()
	movement(delta)

func movement(delta: float):
	# Get input from movement keys (WASD or arrow keys)
	var x_mov = Input.get_action_strength("right") - Input.get_action_strength("left")
	var y_mov = Input.get_action_strength("down") - Input.get_action_strength("up")
	var mov = Vector2(x_mov, y_mov).normalized()  # Normalize to prevent diagonal movement being faster
	
	# Update sprite direction and animations
	animation.process_sprite()
	
	# Set velocity based on player input and ensure it reflects the updated player_velocity
	velocity = mov * player_velocity
	
	# Handle different animation states based on player condition
	if current_knockback != Vector2.ZERO:
		# Apply knockback in invincibility time
		# Ex.: if knockback = 100, travel 100 pixels in invincibility_time seconds
		knockback_cummulative_recovery += delta * knockback_recovery
		current_knockback = init_knockback.lerp(Vector2.ZERO, knockback_cummulative_recovery)
		
		# Play hit animation when knockback is active
		animation.custom_play("taking_damage")
		velocity = current_knockback  # Override movement with knockback force

	elif mov != Vector2.ZERO:
		# Play walk animation when moving
		animation.custom_play("walk")	
	else:
		# Play idle animation when stationary
		animation.custom_play("idle")
		
	# Apply movement and handle collisions
	move_and_slide()

func hurt(damage, direction, knockback_amount, attackerPosition = Vector2.ZERO) -> void:
	if (direction == Vector2.ZERO):
		direction = (global_position - attackerPosition).normalized()
	# Apply damage to player's health
	current_health -= damage
	healthbar.health = current_health

	if current_health <= 0:
		for loot in get_tree().get_nodes_in_group("loot"):
			loot.queue_free()
	
			
		get_tree().call_deferred("change_scene_to_file", "res://Scenes/Utility/GameOver/game_over.tscn")
		call_deferred("queue_free")
		return


	var tween = damage_popup_layer.create_tween()
	tween.tween_property(damage_popup_layer, "color", Color(1, 0, 0, 0.3), 0.1)
	tween.tween_property(damage_popup_layer, "color", Color(1, 0, 0, 0), 0.2)

	# Calculate and apply knockback force in the specified direction
	# Calculate and apply knockback force in the specified direction
	init_knockback = direction * knockback_amount
	# Adjust knockback based on invincibility time, I find this formula testing values in desmos
	init_knockback *= 2/invincibility_time 

	current_knockback = init_knockback
	knockback_cummulative_recovery = 0.0


func _on_grab_area_area_entered(area: Area2D) -> void:
	if area.is_in_group("loot"):
		area.target = self


func _on_collect_area_area_entered(area: Area2D) -> void:
	if area.is_in_group("loot"):
		var gem_value = area.collect()
		# For not level up instantly when died
		if (healthbar.health > 0):
				if area.is_in_group("health_drop"):
					heal_player(gem_value*10)
				else:
					expBar.calculate_experience(gem_value)


## UPGRADE FUNCTIONS ##

# a item_option emits the signal selected_upgrade with the upgrade name as argument
func upgrade_character(upgrade : String):
	for i in range(ResourcesDb.UPGRADES[upgrade]["functions"].size()):
		callv(ResourcesDb.UPGRADES[upgrade]["functions"][i], ResourcesDb.UPGRADES[upgrade]["arguments"][i])
	
	# After upgrading, hide the level-up panel
	levelPanel.hide_levelup_panel()

func heal_player(heal_amount : int):
	current_health += heal_amount
	current_health = min(current_health, max_health)
	healthbar.health = current_health

func update_player_velocity(percentage : float):
	atributtes_percentage["player_velocity"] += percentage
	atributtes_percentage["player_velocity"] = max(atributtes_percentage["player_velocity"], 0.01)
	player_velocity = player_velocity_init * atributtes_percentage["player_velocity"]
	

func update_max_health(health_amount : int):
	# Adjust the player's maximum health and reset current health to max
	max_health = max(max_health + health_amount, 1)
	current_health = min(current_health, max_health)
	healthbar.update_max_health(health_amount)

func add_gun(gun_name: String):
	gunsOrbiter.add_gun(gun_name, atributtes_percentage)

func update_guns(atributte: String, percentage : float):
	atributtes_percentage[atributte] += percentage
	atributtes_percentage[atributte] = max(atributtes_percentage[atributte], 0.01)
	gunsOrbiter.update_guns(atributte, atributtes_percentage[atributte])

func update_pickup_range(range_percentage: float):
	atributtes_percentage["pickup_range"] += range_percentage
	atributtes_percentage["pickup_range"] = max(atributtes_percentage["pickup_range"], 0.01)
	pickup_range = pickup_range_init * atributtes_percentage["pickup_range"]
	grabArea.get_child(0).shape.radius = pickup_range
