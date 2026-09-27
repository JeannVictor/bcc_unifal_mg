# Custom AnimationPlayer class for enemy character animations
extends AnimationPlayer
class_name Enemy_AnimationPlayer

# Export variables for node references - these will appear in the inspector
@export var enemy_path : NodePath  # Path to the enemy node
@onready var enemy = get_node(enemy_path)  # Reference to the enemy node

@export var spriteWalk_path : NodePath ## Path to walk sprite node
@export var spriteAttack_path : NodePath ## Path to attack sprite node
@export var spriteHurt_path : NodePath ## Path to hurt sprite node
@export var spriteDeath_path : NodePath ## Path to death sprite node

@onready var spriteWalk = get_node(spriteWalk_path)  # Reference to walk sprite
@onready var spriteAttack = get_node(spriteAttack_path)  # Reference to attack sprite
@onready var spriteHurt = get_node(spriteHurt_path)  # Reference to hurt sprite
@onready var spriteDeath = get_node(spriteDeath_path)  # Reference to death sprite

# Animation control variables
var can_play_new_animation := true  # Control flag to prevent animation interruptions
var flipped: bool  # Track if sprite should be flipped
var last_result: bool = false  # Store the last direction result
var z_pos : int = 0  # Calculated Z position for depth sorting

# Calculate the total range of possible Z values for depth sorting
var INTERVALE_Z : int = abs(RenderingServer.CANVAS_ITEM_Z_MIN) + abs(RenderingServer.CANVAS_ITEM_Z_MAX)

signal death_animation_finished  # Signal emitted when death animation finishes
func _ready() -> void:
	# Connect signals to handle animation events
	animation_finished.connect(_on_animation_finished)

var last_direction: bool  # Store the last movement direction

func flip_walk_sprite() -> void:
	# Flip the walk sprite based on movement direction
	var current_direction: bool = enemy.velocity.x < 0  # true for left, false for right/stopped
	if current_direction != last_direction:
		spriteWalk.flip_h = current_direction
		last_direction = current_direction

# Main function to process sprite animation and properties
func process_sprite() -> void:
	var dir = set_direction()  # Get current direction
	
	# Mirror sprites based on movement direction
	spriteWalk.flip_h = dir
	spriteAttack.flip_h = dir
	spriteHurt.flip_h = dir
	spriteDeath.flip_h = dir
	
	# Calculate Z position based on Y coordinate for depth sorting (isometric/perspective)
	# Higher Y position = higher Z index (appears in front)
	# negative coordinates inversion need fixing
	var pos : int = int(enemy.global_position.y)
	z_pos = (pos)%RenderingServer.CANVAS_ITEM_Z_MAX if (pos>=0) else (pos)%RenderingServer.CANVAS_ITEM_Z_MIN

	# Apply Z index to both sprites
	spriteWalk.z_index = z_pos
	spriteAttack.z_index = z_pos
	spriteHurt.z_index = z_pos
	spriteDeath.z_index = z_pos

	# Apply horizontal offset if flipped
	if flipped:
		spriteWalk.offset.x *= -1
		spriteAttack.offset.x *= -1
		spriteHurt.offset.x *= -1
		spriteDeath.offset.x *= -1


# Determine sprite direction based on enemy velocity
func set_direction() -> bool:
	# Store current direction based on velocity
	var current_direction: bool = enemy.velocity.x < 0  # true for left, false for right/stopped
	
	# Check if direction has changed
	flipped = (current_direction != last_result)
	
	# Update last result and return direction
	last_result = current_direction
	return current_direction

# Called when an animation starts playing
func custom_play(anim_name: String) -> void:
	if anim_name == "death":
		can_play_new_animation = false
		spriteWalk.visible = false  # Hide both sprites initially
		spriteAttack.visible = false
		spriteHurt.visible = false
		spriteDeath.visible = true		
		play("death")
		return
	if (not can_play_new_animation):
		return  # Exit if new animations are locked
	spriteWalk.visible = false  # Hide both sprites initially
	spriteAttack.visible = false
	spriteHurt.visible = false
	spriteDeath.visible = false

	# Show appropriate sprite based on animation type
	match_animation(anim_name)
	
	play(anim_name)  # Play the specified animation

var last_animation = 0
func match_animation(anim_name: String) -> void:
	match anim_name:
		"taking_damage":
			if not spriteDeath.visible:  # Only allow if death animation is not active
				spriteHurt.visible = true  # Show hurt sprite
		"attack":
			if not spriteDeath.visible and not spriteHurt.visible:  # Only allow if death or damage animation is not active
				can_play_new_animation = false  # Lock animations during attack
				spriteAttack.visible = true  # Show attack sprite
		"walk":
			if not spriteDeath.visible and not spriteHurt.visible and not spriteAttack.visible:  # Only allow if no higher-priority animations are active
				spriteWalk.visible = true  # Show walk sprite
		"RESET":
			if not spriteDeath.visible:  # Only allow if death animation is not active
				spriteWalk.visible = true  # Show walk sprite

# Called when an animation finishes playing
func _on_animation_finished(anim_name: String) -> void:
	if anim_name == "death":
		death_animation_finished.emit()  # Emit signal when death animation finishes
		return  # Do nothing if death animation finished
	can_play_new_animation = true  # Allow new animations to play
