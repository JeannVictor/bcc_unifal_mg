extends Control

@onready var animation_player: AnimationPlayer = $AnimationPlayer

func _ready() -> void:
	animation_player.play("death_screen")
	

func _on_restart_pressed() -> void:
	for child in get_tree().get_nodes_in_group("loot"):
		child.queue_free()
	for child in get_tree().get_nodes_in_group("attack"):
		child.queue_free()
		
	get_tree().change_scene_to_file(ResourcesDb.world_selected)


func _on_quit_pressed() -> void:
	for child in get_tree().get_nodes_in_group("loot"):
		child.queue_free()
	for child in get_tree().get_nodes_in_group("attack"):
		child.queue_free()
		
	get_tree().change_scene_to_file("res://Scenes/Utility/MainMenu/MainMenu.tscn")
