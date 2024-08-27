import torch
from torchvision import transforms
from PIL import Image
import torchvision.models as models
import torch.nn as nn
import chromadb
import os
import sys
import django

# 현재 스크립트의 위치에서 부모 디렉토리로 올라가서 프로젝트 경로를 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Django 설정 모듈 지정 및 초기화
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GoodMarket.settings')
django.setup()

from market.models import ProductFile

# ImageEmbeddingModel 클래스 정의
class ImageEmbeddingModel:
    def __init__(self, weight_path, class_num, img_path):
        self.img_width, self.img_height, self.img_channel = 224, 224, 3
        self.emb_model = self.create_model(weight_path, class_num, embedding=True)
        self.csf_model = self.create_model(weight_path, class_num, embedding=False)
        self.img_tensor = self.preprocess_image(img_path)

    def create_model(self, weight_file, class_num, embedding):
        base_model = models.resnet50(weights=None)
        base_model.fc = nn.Linear(2048, class_num)
        base_model.load_state_dict(torch.load(weight_file, map_location='cpu', weights_only=True))
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

# ChromaDB 유틸리티 함수
def get_chromadb_collection(collection_name="test1", db_path="./chroma_db_data"):
    client = chromadb.PersistentClient(path=db_path)
    
    try:
        return client.get_collection(name=collection_name)
    except ValueError as e:
        if 'does not exist' in str(e):
            return client.create_collection(name=collection_name)
        else:
            raise ValueError(f"ChromaDB 컬렉션 오류: {str(e)}")

# ProductFile 이미지 임베딩 및 저장 함수
def embed_and_store_product_images(model_info_dict):
    images_collection = get_chromadb_collection()
    
    # 모든 ProductFile 객체 가져오기
    product_files = ProductFile.objects.all()

    for product_file in product_files:
        img_path = product_file.file.path
        cate_big = "onepiece"  # 여기에 사용하고자 하는 카테고리를 입력하세요
        
        # 임베딩 추출 및 ChromaDB에 저장
        base_model = ImageEmbeddingModel(
            weight_path=model_info_dict[cate_big][0], 
            class_num=model_info_dict[cate_big][1], 
            img_path=img_path
        )
        emb_vec = base_model.get_embedding()
        category = base_model.get_category()

        image_id = str(product_file.product_file_id)  # 필드명 `product_file_id`로 수정
        embedding_vector = emb_vec.tolist()
        
        images_collection.add(
            embeddings=[embedding_vector], 
            ids=[image_id], 
            metadatas=[{"product_file_id": image_id}]
        )
        
        max_value, max_index = torch.max(category, dim=1)
        print(f"임베딩 size: {emb_vec.shape}, 카테고리: {max_index.item()}")
        print(f"이미지 {image_id}의 임베딩이 ChromaDB에 저장되었습니다.")

# 유사한 이미지를 여러 개 찾는 함수
def find_similar_images(img_path, cate_big, model_info_dict, top_k=4):
    base_model = ImageEmbeddingModel(
        weight_path=model_info_dict[cate_big][0], 
        class_num=model_info_dict[cate_big][1], 
        img_path=img_path
    )
    new_emb_vec = base_model.get_embedding()
    
    images_collection = get_chromadb_collection()

    stored_data = images_collection.get(include=['embeddings', 'metadatas'])

    if not stored_data or not stored_data['embeddings']:
        print("Error: No embeddings found in ChromaDB.")
        return
    
    similarities = []
    new_emb_vec = new_emb_vec.unsqueeze(0)

    for idx, stored_emb in enumerate(stored_data['embeddings']):
        stored_emb_tensor = torch.tensor(stored_emb).unsqueeze(0)
        similarity = torch.nn.functional.cosine_similarity(new_emb_vec, stored_emb_tensor)
        similarities.append((similarity.item(), stored_data['metadatas'][idx]['product_file_id']))

    similarities.sort(reverse=True, key=lambda x: x[0])
    top_similar_images = similarities[:top_k]

    for similarity, product_file_id in top_similar_images:
        try:
            product_file = ProductFile.objects.get(product_file_id=product_file_id)  # 필드명 `product_file_id`로 수정
            print(f"유사한 이미지: {product_file.file.url}, 유사도: {similarity}")
        except ProductFile.DoesNotExist:
            print(f"Error: ProductFile with id {product_file_id} does not exist.")
    
    return top_similar_images

# 모델 정보 딕셔너리
model_info_dict = {
    #"bottom" : [r"bottom가중치이름", 3],
    #"top" : [r"top가중치이름", 5],
    "onepiece": [r"059.pth", 2],
}

if __name__ == "__main__":
    embed_and_store_product_images(model_info_dict)
    find_similar_images(r"C:\Users\USER\Desktop\GoodMarket\media\test\crops\Top\310836.jpg", "onepiece", model_info_dict, top_k=4)
