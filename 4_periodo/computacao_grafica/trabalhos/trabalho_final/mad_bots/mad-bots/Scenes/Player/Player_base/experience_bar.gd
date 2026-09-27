extends TextureProgressBar

@onready var lbl_level = get_node("%lbl_level")  # Reference to the level label GUI element
@onready var levelPanel = get_node("%LevelUp")  # Reference to the level-up panel GUI element

var experience = 0
var experience_level = 1
var collected_experience = 0

func calculate_experience(gem_exp):
	var exp_required = calculate_experiencecap()
	collected_experience += gem_exp
	if experience + collected_experience >= exp_required:
		collected_experience -= exp_required-experience
		experience_level += 1
		experience = 0
		exp_required = calculate_experiencecap()
		levelPanel.show_levelup_panel()	
		calculate_experience(0)
	else:
		experience += collected_experience
		collected_experience = 0

	set_expbar(experience, exp_required)

func calculate_experiencecap():
	var exp_cap = experience_level
	if experience_level < 20:
		exp_cap = experience_level*5
	elif experience_level < 40:
		exp_cap = 95 * (experience_level-19)*8
	else:
		exp_cap = 255 + (experience_level-39)*12
		
	return exp_cap

func set_expbar(set_value_xp = 1, set_max_value = 100):
	value = set_value_xp
	max_value = set_max_value
	lbl_level.text = str("Level: ", experience_level)
