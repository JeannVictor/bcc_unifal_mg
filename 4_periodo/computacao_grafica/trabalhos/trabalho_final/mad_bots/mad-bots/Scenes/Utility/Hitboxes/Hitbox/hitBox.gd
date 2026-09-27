extends Area2D

@export_enum ("DisableForTime", "EnableForTime") var DisableHitBoxType = 0
@onready var collision = $CollisionShape2D
@onready var disableTimer = $TogleeTimer

var damage = 1
var disable = true
var direction = Vector2.ZERO
var knockback_amount = 1
var attacker_position = Vector2.ZERO

func _ready():
	match DisableHitBoxType:
		0: #DisableForTime
			disable = true	
		1: #EnableForTime
			disable = false
	set_deferred("monitorable", disable)
	disableTimer.timeout.connect(_on_disable_hit_box_timer_timeout)
	attacker_position = global_position

func tempToggle():
	
	set_deferred("monitorable", not disable)
	disableTimer.start()


func _on_disable_hit_box_timer_timeout():
	set_deferred("monitorable",disable)

func set_knockback_property(damage_set: int, direction_set: Vector2, knockback_amount_set: int, attacker_position_set: Vector2 = Vector2.ZERO):
	damage = damage_set
	direction = direction_set
	knockback_amount = knockback_amount_set
	attacker_position = attacker_position_set
