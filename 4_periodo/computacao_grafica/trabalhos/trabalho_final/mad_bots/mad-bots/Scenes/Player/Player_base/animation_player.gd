# Custom AnimationPlayer class for player character animations
extends AnimationPlayer
class_name Player_AnimationPlayer

# Export variables for node references - these will appear in the inspector
@export var player_path : NodePath  # Path to the player node
@onready var player = get_node(player_path)  # Reference to the player node

@export var spriteWalk_path : NodePath  # Path to the walk sprite
@onready var spriteWalk = get_node(spriteWalk_path)  # Reference to walk sprite

@export var spriteIdle_path : NodePath  # Path to the idle sprite
@onready var spriteIdle = get_node(spriteIdle_path)  # Reference to idle sprite

@export var spriteTakingDamage_path : NodePath  # Path to the damage sprite
@onready var spriteTakingDamage = get_node(spriteTakingDamage_path)  # Reference to damage sprite

# Animation and rendering variables
var flipped: bool  # Track if sprite should be flipped
var last_result: bool = false  # Store the last direction result
var z_pos : int = 0  # Calculated Z position for depth sorting

# Calculate the total range of possible Z values for depth sorting
var INTERVALE_Z : int = abs(RenderingServer.CANVAS_ITEM_Z_MIN) + abs(RenderingServer.CANVAS_ITEM_Z_MAX)


# Main function to process sprite animation and properties
func process_sprite() -> void:
	var dir : bool = set_direction()
	
	# Mirror all sprites based on movement direction (left is true, right is false)
	spriteWalk.flip_h = dir
	spriteIdle.flip_h = dir
	spriteTakingDamage.flip_h = dir
	
	# Calculate Z position based on Y coordinate for depth sorting
	# Higher Y position = higher Z index (appears in front)
	var pos : int = int(player.global_position.y)
	z_pos =  (pos)%RenderingServer.CANVAS_ITEM_Z_MAX if (pos>=0) else (pos)%RenderingServer.CANVAS_ITEM_Z_MIN
	
	
	# Apply Z index to all sprites for consistent depth sorting
	spriteWalk.z_index = z_pos
	spriteIdle.z_index = z_pos
	spriteTakingDamage.z_index = z_pos

	# Apply horizontal offset if flipped
	if flipped:
		spriteWalk.offset.x *= -1
		spriteIdle.offset.x *= -1
		spriteTakingDamage.offset.x *= -1

func set_direction() -> bool:
	# Handle case when player is not moving horizontally
	if player.velocity.x == 0:
		flipped = false  # No flip needed when stationary
		return last_result  # Return the last known direction
	
	# Determine if player is moving left (true) or right (false)
	var going_left = player.velocity.x < 0
	
	# Check if direction has changed from the previous frame
	flipped = (going_left != last_result)
	
	# Update the stored direction for next frame comparison
	last_result = going_left
	
	return going_left




# Called when an animation starts playing
func custom_play(anim_name: String) -> void:
	# Hide all sprites initially
	spriteWalk.visible = false
	spriteIdle.visible = false
	spriteTakingDamage.visible = false

	# Show appropriate sprite based on animation type
	match anim_name:
		"walk":
			spriteWalk.visible = true
		"idle":
			spriteIdle.visible = true
		"taking_damage":
			spriteTakingDamage.visible = true
	play(anim_name)  # Play the specified animation
