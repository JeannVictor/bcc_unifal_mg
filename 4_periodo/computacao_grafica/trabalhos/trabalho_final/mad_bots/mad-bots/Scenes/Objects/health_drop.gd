extends Area2D

@export var experience = 1

var spr_green = preload("res://Assets/Textures/GUI/icons/1 Icons/6/Skillicon6_16.png")
var spr_blue = preload("res://Assets/Textures/GUI/icons/1 Icons/13/Skillicon13_16.png")
var spr_red = preload("res://Assets/Textures/GUI/icons/1 Icons/11/Skillicon11_16.png")

var target = null
var speed = -5
var float_offset = 0.0
var float_amplitude = 1.0
var float_frequency = 1.0


@onready var sprite = $Sprite2D
@onready var collision = $CollisionShape2D
@onready var sound = $snd_collected

func _ready():
	if experience < 11:
		return
	elif experience < 21:
		sprite.texture = spr_blue
	else:
		sprite.texture = spr_red
		
func _physics_process(delta):
	#up and down floating effect
	float_offset += delta
	sprite.position.y += float_amplitude * sin(float_offset * float_frequency * PI * 2)
	if float_offset > 1.0:
		float_offset -= 1.0

	if target != null:
		global_position = global_position.move_toward(target.global_position, speed)
		speed += 40*delta

func collect():
	sound.play()
	collision.call_deferred("set","disabled",true)
	sprite.visible = false
	return experience
	
func _on_snd_collected_finished():
	queue_free()
	

	
	
