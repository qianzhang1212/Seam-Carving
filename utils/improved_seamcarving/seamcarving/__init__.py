from image_sc import image_seam_carving
from video_sc import video_seam_carving

def seam_carving(data, width_change, height_change, use_integers=True):
	instance = None
	if data.ndim == 3:
		instance = image_seam_carving(data, width_change, height_change, use_integers)
	else:
		instance = video_seam_carving(data, width_change, height_change, use_integers)

	result = instance.generate()
	return result
