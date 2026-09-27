extends AnimationPlayer

@onready var timer = $AnimationCooldown

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	timer.connect("timeout", _on_timeout)


func _on_timeout():
	play("falling_leaves")
