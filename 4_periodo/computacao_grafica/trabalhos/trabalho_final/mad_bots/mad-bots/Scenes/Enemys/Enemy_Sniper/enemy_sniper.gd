extends Enemy

@export var repel_radius: float = 100.0
@export var repel_hysteresis: float = 10.0
var target_velocity: Vector2 = Vector2.ZERO
var is_repelled: bool = false
var in_hysteresis: bool = false

func move(distance_to_player: float) -> void:
	# Use hysteresis to avoid flickering at the repel radius boundary.
	if distance_to_player <= repel_radius - repel_hysteresis:
		in_hysteresis = false
		is_repelled = true
	elif distance_to_player <= repel_radius + repel_hysteresis:
		in_hysteresis = true
	else:
		in_hysteresis = false
		is_repelled = false
	

	if in_hysteresis:
		velocity = Vector2.ZERO
		animation.custom_play("RESET")
	elif is_repelled:
		velocity = -direction_to_player * speed
		animation.process_sprite()
	move_and_slide()
