from PIL import Image
import re
import os

def paste_obj(img_path, object_path, X, Y, output_folder="object"):
    
    base_image = Image.open(img_path).convert("RGB")
    object_image = Image.open(object_path).convert("RGB")
    
    base_image.paste(object_image, (X, Y), object_image)
    base_image.save(img_path)

    match = re.search(r'(\d+)\.png$', object_path)
    line_number = int(match.group(1))

    text_file_path = img_path.replace('.png', 'txt')
    with open(text_file_path, 'r') as file:
            for i, line in enumerate(file):
                if i == line_number:
                    obj_info = line
    X, y = X / base_image.width, y / base_image.height

    with open(object_path, 'w') as file:
        info = [obj_info[0], X, y, obj_info[3], obj_info[4]]
        info = ' '.join(str(x) for x in info)+"\n"
        file.write(info)

# 객체 저장
    output_file_name = f"cropped_{line_number + 1}.png"
    output_file_name = os.path.join(output_folder, output_file_name)
    object_image.save(output_file_name)


