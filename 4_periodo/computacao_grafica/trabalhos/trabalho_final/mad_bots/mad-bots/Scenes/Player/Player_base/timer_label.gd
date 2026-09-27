extends Label

@export var time: float ## Time in seconds for the scene to 

func _process(delta):
	time -= delta
	text = format_time(time+1)

	if (time <= 0):
		get_tree().call_deferred("change_scene_to_file", "res://Scenes/Utility/WinScreen/WinScreen.tscn")
	

func format_time(t):
	var minutes = int(t / 60)
	var seconds = int(t) % 60
	return "%02d:%02d" % [minutes, seconds]
