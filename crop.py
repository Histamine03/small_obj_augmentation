from PIL import Image
import os

def xywh_to_corners(xywh, img_width, img_height):
    cls, x, y, width, height = xywh
    x = x * img_width
    y = y * img_height
    width = width * img_width
    height = height * img_height
    x_top = x - (width / 2)
    x_bottom = x + (width / 2)
    y_top = y - (height / 2)
    y_bottom = y + (height / 2)
    print(x_top, y_top, x_bottom, y_bottom)
    return x_top, y_top, x_bottom, y_bottom

def crop_image(image_path, bbox):
    image = Image.open(image_path)
    cropped_image = image.crop(bbox)
    return cropped_image

def save_cropped_images(image_folder, file_name, output_folder="object"):
    cropped_images = []
    txt_file_name = file_name.replace('.png', '.txt')
    
    txt_file_path = os.path.join(image_folder, txt_file_name)
    img_file_path = os.path.join(image_folder, file_name)
    
    image = Image.open(img_file_path)
    img_width, img_height = image.size
    
    output_directory = os.path.join(image_folder, output_folder)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    with open(txt_file_path, "r") as f:
        for index, line in enumerate(f.readlines()):
            class_id, x, y, width, height = map(float, line.strip().split())
            bbox = xywh_to_corners((class_id, x, y, width, height), img_width, img_height)
            cropped_img = crop_image(img_file_path, bbox)

            output_file_name = f"cropped_{index}.png"
            output_file_path = os.path.join(output_directory, output_file_name)
            cropped_img.save(output_file_path)
            cropped_images.append(output_file_path)
    return cropped_images
