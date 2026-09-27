extends AnimatableBody2D
@onready var sprite = $Sprite2D

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	var pos = int(global_position.y)
	sprite.z_index = (pos)%RenderingServer.CANVAS_ITEM_Z_MAX if (pos>=0) else (pos)%RenderingServer.CANVAS_ITEM_Z_MIN
	
