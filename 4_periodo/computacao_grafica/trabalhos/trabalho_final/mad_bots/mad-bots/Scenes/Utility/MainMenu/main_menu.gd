extends Node2D

@onready var main_buttons: VBoxContainer = $MainButtons
@onready var options: TextureRect = $Options
@onready var level_selector: TextureRect = $LevelSelector


func _ready():
	main_buttons.visible = true
	options.visible = false
	level_selector.visible = false

func _on_start_pressed() -> void:
	main_buttons.visible = false
	level_selector.visible = true

func _on_options_pressed() -> void:
	main_buttons.visible = false
	options.visible = true


func _on_quit_pressed() -> void:
	get_tree().quit()


func _on_back_options_pressed() -> void:
	main_buttons.visible = true
	options.visible = false


func _on_back_level_selector_pressed() -> void:
	main_buttons.visible = true
	level_selector.visible = false


func _on_level_1_pressed() -> void:
	TransitionScreen.transition()
	await TransitionScreen.on_transition_finished
	ResourcesDb.world_selected = "res://World/world1.tscn"
	get_tree().call_deferred("change_scene_to_file", "res://World/world1.tscn")

func _on_level_2_pressed() -> void:
	TransitionScreen.transition()
	await TransitionScreen.on_transition_finished
	ResourcesDb.world_selected = "res://World/world2.tscn"
	get_tree().call_deferred("change_scene_to_file", "res://World/world2.tscn")

func _on_level_3_pressed() -> void:
	TransitionScreen.transition()
	await TransitionScreen.on_transition_finished
	ResourcesDb.world_selected = "res://World/world3.tscn"
	get_tree().call_deferred("change_scene_to_file", "res://World/world3.tscn")


func _on_history_pressed() -> void:
	get_tree().call_deferred("change_scene_to_file", "res://Scenes/Utility/IntroScreen/IntroScreen.tscn")
