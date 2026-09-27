extends Node2D


@export var orbit_radius: float = 200
@export var orbit_speed: float = 0.25  # Rotações por segundo

@onready var player = get_parent()

var array_guns_count: int = 0
var target_position: Vector2 = Vector2.ZERO

func add_gun(gun_name: String, atributtes_percentage: Dictionary):
	if ResourcesDb.PACKEDSCENES["Guns"].has(gun_name):
		var gun_instance = ResourcesDb.PACKEDSCENES["Guns"][gun_name].instantiate()
		add_child(gun_instance)
		gun_instance.gun_update("damage", atributtes_percentage["damage"])
		gun_instance.gun_update("fire_rate", atributtes_percentage["fire_rate"])
		gun_instance.gun_update("projectile_speed", atributtes_percentage["projectile_speed"])
		gun_instance.gun_update("fire_range", atributtes_percentage["fire_range"])
		gun_instance.gun_update("knockback_amount", atributtes_percentage["knockback_amount"])
		gun_instance.gun_update("pierce", atributtes_percentage["pierce"])
		gun_instance.gun_update("explosion_size", atributtes_percentage["explosion_size"])
		
		array_guns_count += 1
		
	else:
		print("Gun not found in available guns.")
		return

	var i : int = 0
	for gun in self.get_children():
		var angle = i * TAU / array_guns_count
		gun.set_meta("angle", angle)
		gun.rotation = angle
		gun.global_position = player.global_position + Vector2(cos(angle), sin(angle)) * orbit_radius
		i += 1


func start_fire():
	for gun in self.get_children():
		gun.can_fire = true

func stop_fire():
	for gun in self.get_children():
		gun.can_fire = false


func _process(delta):
	for gun in self.get_children():
		var angle = gun.get_meta("angle") + orbit_speed * delta
		gun.set_meta("angle", angle)
		gun.global_position = player.global_position + Vector2(cos(angle), sin(angle)) * orbit_radius
	
func update_guns(atributte: String, value: float):
	for gun in self.get_children():
		gun.gun_update(atributte, value)
