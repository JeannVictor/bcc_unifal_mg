extends Projectile


@onready var hitbox = $Area2D
func specific_property_process():
	hitbox.set_knockback_property(damage, Vector2.ZERO, knockback_amount, global_position)
	can_kill = false
	if (hitbox.disabled):
		hitbox.enable()

func set_explosion_size(size: float) -> void:
	hitbox.set_size(size)


func _on_area_2d_expired() -> void:
	can_kill = true
