extends Area2D


var damage = 1
var disabled = true

var direction = Vector2.ZERO
var knockback_amount = 1
var attacker_position = Vector2.ZERO

signal expired
@onready var collision = $CollisionShape2D
@onready var sprite = $Sprite2D

@export var enable_time = 0.1
@export var sprite_enable_time = 0.1
@export var explosion_cooldown = 0.1

var enabled_time: float = 0.0
var sprite_enabled_time: float = 0.0

func enable():
	disabled = false
	enabled_time = enable_time
	sprite_enabled_time = sprite_enable_time
	collision.set_deferred("disabled", false)
	sprite.visible = true


func _process(delta):
	if not disabled:
		enabled_time -= delta
		if enabled_time <= 0:
			disabled = true
			collision.set_deferred("disabled", true)
			emit_signal("expired")
	if sprite.visible:
		sprite_enabled_time -= delta
		if sprite_enabled_time <= 0:
			sprite.visible = false
		

func set_knockback_property(_damage: int, _direction: Vector2, _knockback_amount: float, _attacker_position: Vector2) -> void:
	damage = _damage
	direction = _direction
	knockback_amount = _knockback_amount
	attacker_position = _attacker_position

func set_size(size: float) -> void:
	var shape = collision.shape
	if shape is CircleShape2D:
		shape.radius = size / 2
		collision.shape = shape
	sprite.scale = Vector2.ONE * (size / sprite.texture.get_size().x)


