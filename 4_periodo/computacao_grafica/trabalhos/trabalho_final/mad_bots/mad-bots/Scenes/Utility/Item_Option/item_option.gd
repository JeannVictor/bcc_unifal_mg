extends TextureRect

@onready var lblName = $TextureName/lbl_name
@onready var lblDescription = $TextureDescription/lbl_description
@onready var lblrarity = $TextureRarity/lbl_rarity
@onready var itemIcon = $TextureRect/itemIcon

var mouse_over = false
var item = null
@onready var player = get_tree().get_first_node_in_group("player")

signal selected_upgrade(upgrade)

func _ready():
	connect("selected_upgrade",Callable(player,"upgrade_character"))
	lblName.text = ResourcesDb.UPGRADES[item]["displayname"]
	lblDescription.text = ResourcesDb.UPGRADES[item]["details"]
	lblrarity.text = ResourcesDb.UPGRADES[item]["rarity"].capitalize()

	var rarity_color = ResourcesDb.RARITY_CURVES[ResourcesDb.UPGRADES[item]["rarity"]]["color"]
	lblrarity.add_theme_color_override("font_color",Color(rarity_color))
	lblName.add_theme_color_override("font_color",Color(rarity_color))

	itemIcon.texture = load(ResourcesDb.UPGRADES[item]["icon"])

func _input(event):
	if event.is_action_pressed("click"):
		if mouse_over:
			emit_signal("selected_upgrade",item)

func _on_mouse_entered():
	mouse_over = true
	position.x += 10

func _on_mouse_exited():
	position.x -= 10
	mouse_over = false
