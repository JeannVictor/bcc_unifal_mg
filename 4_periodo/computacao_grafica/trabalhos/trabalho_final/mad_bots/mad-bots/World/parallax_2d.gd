extends Parallax2D

@onready var sprite = $Sprite2D

# Lista de texturas disponíveis
var map_textures = [
	"res://Assets/Maps/grass.png",
	"res://Assets/Maps/earth.png",
	"res://Assets/Maps/bloquete.png"
]

func _ready():
	randomize()  # garante que o sorteio mude a cada execução

	# Escolhe uma das texturas aleatoriamente
	var random_index = randi() % map_textures.size()
	var texture_path = map_textures[random_index]

	# Carrega e aplica ao Sprite2D
	var texture = load(texture_path)
	if texture:
		sprite.texture = texture
		print("Mapa selecionado:", texture_path)
	else:
		push_error("Não foi possível carregar a textura: " + texture_path)
