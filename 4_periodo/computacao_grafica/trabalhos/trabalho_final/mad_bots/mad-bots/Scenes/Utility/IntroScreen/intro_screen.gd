extends Control

@onready var animation_player: AnimationPlayer = $AnimationPlayer

func _ready() -> void:
	animation_player.play("TitleFade")
	await animation_player.animation_finished
	animation_player.play("TextFade")


func _on_continue_pressed() -> void:
	get_tree().call_deferred("change_scene_to_file","res://Scenes/Utility/MainMenu/MainMenu.tscn")
