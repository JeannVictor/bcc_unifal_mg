extends Area2D
class_name Projectile


var direction = Vector2.ZERO
var speed = 400
var damage = 1
var knockback_amount = 1
var pierce = 1
var can_kill = true
var have_to_kill = false
var range_travel : float = 1
signal shake_camera(intensity, duration)

@export var shake_camera_on_hit = false
@export var shake_intensity = 5
@export var shake_duration = 0.1


func _ready():
	body_entered.connect(_on_body_entered)

func _physics_process(delta: float) -> void:
	if (have_to_kill):
		kill()
	var distance : Vector2 = direction.normalized() * speed * delta
	range_travel -= distance.length()
	global_position += distance
	if (range_travel <= 0):
		kill()

func _on_body_entered(body):
	if body:
		pierce -= 1
		specific_property_process()
		if pierce < 0:
			kill()
		
		

func specific_property_process():
	pass

func kill():
	if can_kill:
		if shake_camera_on_hit:
			emit_signal("shake_camera",shake_intensity,shake_duration)
		queue_free()
	else:
		have_to_kill = true
