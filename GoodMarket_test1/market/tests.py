import torch
from torchvision import transforms
from PIL import Image
import torchvision.models as models
import torch.nn as nn
import os
import sys
import django

# 현재 스크립트의 위치에서 부모 디렉토리로 올라가서 프로젝트 경로를 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Django 설정 모듈 지정 및 초기화
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GoodMarket.settings')  # 'GoodMarket.settings'는 Django 프로젝트 설정 파일 경로
django.setup()

from market.models import ProductFile

class ImageEmbeddingModel:
    def __init__(self, weight_path, class_num, img_path):
        self.img_width, self.img_height, self.img_channel = 224, 224, 3
        self.emb_model = self.create_model(weight_path, class_num, embedding=True)
        self.csf_model = self.create_model(weight_path, class_num, embedding=False)
        self.img_tensor = self.preprocess_image(img_path)

    def create_model(self, weight_file, class_num, embedding):
        base_model = models.resnet50(weights=None)
        base_model.fc = nn.Linear(2048, class_num)
        base_model.load_state_dict(torch.load(weight_file, map_location='cpu'))
        base_model.eval()

        if embedding:
            base_model = torch.nn.Sequential(*(list(base_model.children())[:-1]))
        
        return base_model
    
    def preprocess_image(self, img_path):
        img = Image.open(img_path).convert('RGB')
        preprocess = transforms.Compose([
            transforms.Resize((self.img_width, self.img_height)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        img_tensor = preprocess(img)
        img_tensor = img_tensor.unsqueeze(0)
        return img_tensor
    
    def get_embedding(self):
        with torch.no_grad():
            embedding = self.emb_model(self.img_tensor)
        return embedding.view(-1)

    def get_category(self):
        with torch.no_grad():
            category = self.csf_model(self.img_tensor)
        return category

def embed_and_classify_product_images(model_info_dict):
    # 모든 ProductFile 객체 가져오기
    product_files = ProductFile.objects.all()

    for product_file in product_files:
        img_path = product_file.file.path
        cate_big = "onepiece"  # 카테고리에 맞는 모델 정보 사용
        
        # 임베딩 추출 및 카테고리 예측
        base_model = ImageEmbeddingModel(
            weight_path=model_info_dict[cate_big][0], 
            class_num=model_info_dict[cate_big][1], 
            img_path=img_path
        )
        emb_vec = base_model.get_embedding()
        category = base_model.get_category()

        image_id = str(product_file.product_file_id)
        embedding_vector = emb_vec.tolist()
        
        max_value, max_index = torch.max(category, dim=1)
        print(f"임베딩 size: {emb_vec.shape}, 카테고리: {max_index.item()}")
        print(f"이미지 {image_id}의 임베딩과 카테고리가 추출되었습니다.")

# 모델 정보 딕셔너리
model_info_dict = {
    "onepiece": [r"C:\Users\USER\Desktop\GoodMarket_test\059.pth", 3]
}

if __name__ == "__main__":
    embed_and_classify_product_images(model_info_dict)
