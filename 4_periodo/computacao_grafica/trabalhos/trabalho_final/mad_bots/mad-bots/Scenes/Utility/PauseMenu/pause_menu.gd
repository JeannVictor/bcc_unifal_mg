extends Control

@onready var animation_player: AnimationPlayer = $AnimationPlayer
@onready var level_up: Node = get_tree().get_first_node_in_group("player").get_node("%LevelUp")
@onready var v_box_container: VBoxContainer = $Panel/VBoxContainer

signal paused()
signal resumed()

func _ready():
	v_box_container.position = Vector2(-916.75,-9)
	animation_player.play("RESET")
	connect("paused",Callable(level_up,"paused_menu"))
	connect("resumed",Callable(level_up,"resumed_menu"))

func resume():
	emit_signal("resumed")
	get_tree().paused = false
	animation_player.play_backwards("blur")

func pause():
	emit_signal("paused")
	get_tree().paused = true
	animation_player.play("blur")


func testEsc():
	if Input.is_action_just_pressed("esc") and !get_tree().paused:
		pause()
		v_box_container.position = Vector2(20.25, -5) 
	elif Input.is_action_just_pressed("esc") and get_tree().paused:
		resume()
		v_box_container.position = Vector2(-916.75,-9)

func _on_resume_pressed() -> void:
	resume()


func _on_restart_pressed() -> void:
	for child in get_tree().get_nodes_in_group("loot"):
		child.queue_free()
	for child in get_tree().get_nodes_in_group("attack"):
		child.queue_free()
		
	resume()
	get_tree().reload_current_scene()


func _on_quit_pressed() -> void:
	for child in get_tree().get_nodes_in_group("loot"):
		child.queue_free()
	for child in get_tree().get_nodes_in_group("attack"):
		child.queue_free()
		
	resume()
	get_tree().change_scene_to_file("res://Scenes/Utility/MainMenu/MainMenu.tscn")

func _process(_delta):
	testEsc()
