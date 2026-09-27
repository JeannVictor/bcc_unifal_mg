extends ProgressBar

@onready var timer = get_node("%Timer")
@onready var damage_bar = get_node("%DamageBar")
@onready var label = get_node("%Label")

# This variable represents the health value of an entity. 
# It uses a setter function (_set_health) to handle changes to the health value, 
# allowing for additional logic or constraints to be applied whenever the health is modified.
var health = 0 : set = _set_health

func _set_health(new_health : int):
	var prev_health = health
	health = clamp(new_health, 0, max_value)
	label.text = str("Hp: ", health)
	value = health
	if health <= 0:
		queue_free()
	
	if health < prev_health:
		timer.start()
	else:
		damage_bar.value = health


func init_health(_health : int):
	health = _health
	max_value = _health
	value = _health
	damage_bar.max_value = _health
	label.text = str("Hp: ", _health)
	damage_bar.value = _health

func update_max_health(amount: int):
	var new_max = max_value + amount
	max_value = new_max if (new_max > 0) else 1.0
	health = min(health, max_value)
	value = health
	damage_bar.max_value = max_value
	label.text = str("Hp: ", health)

	if amount < 0:
		timer.start()
	else:
		damage_bar.value = health


# Called when the timer times out; updates the damage bar to match the current health.
func _on_timer_timeout() -> void:
	damage_bar.value = health
