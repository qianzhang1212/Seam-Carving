from seam_carving import SeamCarver

import os



def image_resize_without_mask(filename_input, filename_output, new_height, new_width):
    obj = SeamCarver(filename_input, new_height, new_width)
    obj.save_result(filename_output)


def image_resize_with_mask(filename_input, filename_output, new_height, new_width, filename_mask):
    obj = SeamCarver(filename_input, new_height, new_width, protect_mask=filename_mask)
    obj.save_result(filename_output)


def object_removal(filename_input, filename_output, filename_mask):
    obj = SeamCarver(filename_input, 0, 0, object_mask=filename_mask)
    obj.save_result(filename_output)

def image_content_amplification(filename_input, filename_output):
    obj = SeamCarver(filename_input, 0, 0)
    obj.save_result(filename_output)

if __name__ == '__main__':
    """
    Put image in in/images folder and protect or object mask in in/masks folder
    Ouput image will be saved to out/images folder with filename_output
    """

    folder_in = 'in'
    folder_out = 'out'

    filename_input = 'cat.png'
    filename_output = 'cat_result.png'
    filename_mask = 'bus_mask_bw.png'
    new_height = 200
    new_width = 512

    input_image = os.path.join(folder_in, filename_input)
    input_mask = os.path.join(folder_in, filename_mask)
    output_image = os.path.join(folder_out, filename_output)

    #image_resize_without_mask(input_image, output_image, new_height, new_width)
    #image_resize_with_mask(input_image, output_image, new_height, new_width, input_mask)
    #object_removal(input_image, output_image, input_mask)
    image_content_amplification(input_image,output_image)








