extends Node2D

@onready var sprite: Sprite2D = $Sprite2D
@onready var projectile_spawn_point: Marker2D = $ProjectileSpawnPoint
@onready var enemyDetector = $EnemyDetector
@onready var sound_player: AudioStreamPlayer = $AudioStreamPlayer

@export var init_damage: int = 100 ## Damage dealt by the gun
@export var init_fire_rate: float = 0.5 ## Time in seconds between shots
@export var init_projectile_speed: float = 4000 ## Speed of the projectile
@export var init_fire_range : float = 400
@export var init_knockback_amount: float = 500 ## Knockback force applied to enemies hit
@export var pierce: int = 1 ## How many enemies the projectile can pierce through
@export var init_explosion_size: float = 100.0 ## Size of the explosion effect

# Update gun stats functions
var damage: int
var fire_rate: float
var projectile_speed: float
var fire_range : float
var knockback_amount: float
var explosion_size: float

var current_cooldown: float = 0.0
var can_fire = false


@export var projectile_scene: PackedScene  ## The projectile scene to instantiate

func _ready():
	damage = init_damage
	fire_rate = init_fire_rate
	projectile_speed = init_projectile_speed
	fire_range = init_fire_range
	knockback_amount = init_knockback_amount
	explosion_size = init_explosion_size
	
	#temporario, depois criar função para mudar o projétil na interface
	enemyDetector.connect("start_fire", _on_start_fire)
	enemyDetector.connect("stop_fire", _on_stop_fire)
	enemyDetector.get_child(0).shape.radius = fire_range

func _process(delta: float):
	current_cooldown += delta
	if current_cooldown >= fire_rate and can_fire:
		current_cooldown = 0
		fire(enemyDetector.closest_enemy_position())

func fire(target_pos: Vector2):	
	sound_player.play()
	var projectile_instance = projectile_scene.instantiate()
	get_tree().root.add_child(projectile_instance)
	var target_direction = (target_pos - projectile_spawn_point.global_position).normalized();
	self.rotation = target_direction.angle()
	projectile_instance.global_position = projectile_spawn_point.global_position
	projectile_instance.damage = damage
	projectile_instance.direction = target_direction
	projectile_instance.pierce = pierce
	projectile_instance.range_travel = fire_range
	projectile_instance.speed = projectile_speed
	projectile_instance.knockback_amount = knockback_amount
	projectile_instance.rotation  = target_direction.angle()
	if projectile_instance.has_method("set_explosion_size"):
		projectile_instance.set_explosion_size(explosion_size)
	
	
func _on_start_fire():
	can_fire = true
func _on_stop_fire():
	can_fire = false




func gun_update(upgrade_type: String, value: float):
	match upgrade_type:
		"damage":
			damage = (int)(init_damage * value)
		"fire_rate":
			fire_rate = max(0.01, init_fire_rate/value)
		"projectile_speed":
			projectile_speed = (init_projectile_speed * value)
		"fire_range":
			fire_range = (init_fire_range * value)
			enemyDetector.get_child(0).shape.radius = fire_range
		"knockback_amount":
			knockback_amount = init_knockback_amount * value
		"pierce":
			pierce += (int)(value)
		"explosion_size":
			explosion_size = init_explosion_size * value
		_:
			print("Unknown upgrade type: ", upgrade_type)

func set_current_projectile(projectile_name: String):
	if ResourcesDb.PACKEDSCENES["Projectiles"].has(projectile_name):
		projectile_scene = ResourcesDb.PACKEDSCENES["Projectiles"][projectile_name]
	else:
		print("Projectile not found in available projectiles.")
