from PIL import Image
import os

def reverse_image(image_path):
    img = Image.open(image_path)
    reversed_img = img.transpose(Image.FLIP_LEFT_RIGHT)
    
    # 새로운 파일 경로 생성
    base, ext = os.path.splitext(image_path)
    reversed_image_path = f"{base}_reversed{ext}"
    reversed_img.save(reversed_image_path)
    
    return reversed_image_path
