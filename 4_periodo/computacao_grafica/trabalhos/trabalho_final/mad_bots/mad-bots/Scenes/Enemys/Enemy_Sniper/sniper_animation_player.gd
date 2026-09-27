extends Enemy_AnimationPlayer

func process_sprite() -> void:
	var dir = set_direction()  # Get current direction
	
	# Mirror sprites based on movement direction
	spriteWalk.flip_h = dir
	spriteAttack.flip_h = dir
	spriteHurt.flip_h = dir
	spriteDeath.flip_h = dir
	
	# Calculate Z position based on Y coordinate for depth sorting (isometric/perspective)
	# Higher Y position = higher Z index (appears in front)
	# negative coordinates inversion need fixing
	var pos : int = int(enemy.global_position.y)
	z_pos = (pos)%RenderingServer.CANVAS_ITEM_Z_MAX if (pos>=0) else (pos)%RenderingServer.CANVAS_ITEM_Z_MIN

	# Apply Z index to both sprites
	spriteWalk.z_index = z_pos
	spriteAttack.z_index = z_pos
	spriteHurt.z_index = z_pos
	spriteDeath.z_index = z_pos

	# Apply horizontal offset if flipped
	if flipped:
		spriteWalk.offset.x *= -1
		spriteAttack.offset.x *= -1
		spriteHurt.offset.x *= -1
		spriteDeath.offset.x *= -1
		enemy.attack.marker.position.x *= -1
