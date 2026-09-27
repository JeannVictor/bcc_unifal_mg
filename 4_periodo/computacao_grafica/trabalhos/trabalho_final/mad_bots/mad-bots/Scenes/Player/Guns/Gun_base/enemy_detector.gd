extends Area2D

var enemies_in_range: Array = []

signal start_fire()
signal stop_fire()

func _ready():
	connect("body_entered", Callable(self, "_on_body_entered"))
	connect("body_exited", Callable(self, "_on_body_exited"))

func _on_body_entered(body: Node2D):
	if body.is_in_group("enemy"):
		enemies_in_range.append(body)
	emit_signal("start_fire")

func _on_body_exited(body: Node2D):
	enemies_in_range.erase(body)
	if enemies_in_range.is_empty():
		emit_signal("stop_fire")

func closest_enemy_position() -> Vector2:
	if enemies_in_range.is_empty():
		return Vector2.ZERO
	
	var closest_enemy = enemies_in_range[0]
	var closest_dist_squared = global_position.distance_squared_to(closest_enemy.global_position)
	
	for i in range(1, enemies_in_range.size()):
		var enemy = enemies_in_range[i]
		var dist_squared = global_position.distance_squared_to(enemy.global_position)
		if dist_squared < closest_dist_squared:
			closest_dist_squared = dist_squared
			closest_enemy = enemy
	
	return closest_enemy.global_position
