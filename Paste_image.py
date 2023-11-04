from PIL import Image
import re
import os

def paste_obj(img_path, object_path, X, Y, output_folder="object"):

    base_image = Image.open(img_path).convert("RGBA")
    object_image = Image.open(object_path).convert("RGBA")

    position = (int(X), int(Y))
    base_image.paste(object_image, position, object_image.split()[3])
    base_image.save(img_path)
    
    match = re.search(r'(\d+)\.png$', object_path)
    if match:
        line_number = int(match.group(1))
    else:
        print("No line number found in object path.")
        return

    text_file_path = img_path.replace('.png', '.txt')
    if not os.path.exists(text_file_path):
        print(f"Label file {text_file_path} not found.")
        return

    with open(text_file_path, 'r') as file:
        lines = file.readlines()

    if line_number < len(lines):
        parts = lines[line_number].split()
        if len(parts) == 5:
            parts[1] = str(X / base_image.width)  # x_center 업데이트
            parts[2] = str(Y / base_image.height)  # y_center 업데이트
            lines[line_number] = ' '.join(parts) + '\n'
        else:
            print("Label format incorrect.")
            return
    else:
        print("Line number exceeds the number of lines in the label file.")
        return

# 라벨 파일 저장
    with open(text_file_path, 'w') as file:
        file.writelines(lines)

# 객체 이미지 저장
    output_file_name = f"cropped_{line_number}.png"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path = os.path.join(output_folder, output_file_name)
    object_image.save(output_path)

# 객체 저장
    output_file_name = f"cropped_{line_number + 1}.png"
    output_file_name = os.path.join(output_folder, output_file_name)
    object_image.save(output_file_name)