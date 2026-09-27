extends Node2D

# Node references for the attack system components
@onready var attack_area = $Attack_area          # Area that actually applies damage/knockback
@onready var delay = $Delay_timer                # Timer to control attack timing
@onready var cooldown = $Cooldown_timer        # Timer to manage attack cooldowns

# Export variables to configure attack properties in the inspector
@export var damage : int                         # Damage dealt by the attack
@export var knockback_force : int = 0            # Force applied for knockback effect
@export var attack_range : float = 50.0               # Range within which the attack can be initiated


var can_attack = false						# Flag to control if attack can be initiated
var cooldown_complete = true
# Signal emitted when player enters detection range and attack can begin

func _ready():
	# Connect signals to their respective handler functions
	delay.timeout.connect(_on_delay_timeout)
	cooldown.timeout.connect(_on_attack_cooldown_timeout)


# Initiates the attack sequence with specified angle
func start_attack(target_position: Vector2) -> void:
	if (not cooldown_complete):
		return  # Exit if still in cooldown

	var direction = (target_position - global_position).normalized()
	# Prevent further attacks until cooldown completes
	cooldown_complete = false
	cooldown.start()
	# Configure the attack area with damage and knockback properties
	attack_area.set_knockback_property(damage, direction, knockback_force)
	
	# Start delay timer before attack area becomes active
	delay.start()

# Called when the delay timer finishes
func _on_delay_timeout():
	# Activate the attack area to apply damage/knockback
	attack_area.tempToggle()

# Called when the cooldown timer finishes
func _on_attack_cooldown_timeout():
	cooldown_complete = true


func _on_attack_area_body_entered(_body: Node2D) -> void:
	can_attack = true 


func _on_attack_area_body_exited(_body: Node2D) -> void:
	can_attack = false
