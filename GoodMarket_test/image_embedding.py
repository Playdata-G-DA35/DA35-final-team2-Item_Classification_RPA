import torch
from torchvision import transforms
from PIL import Image
import torchvision.models as models
import torch.nn as nn





class ImageEmbeddingModel:
    def __init__(self, weight_path, class_num, img_path):
        self.img_width, self.img_height, self.img_channel = 224, 224, 3
        # 임베딩 모델 구조
        self.emb_model = self.create_model(weight_path, class_num, embedding=True)
        # 카테고리 구분 모델 구조
        self.csf_model = self.create_model(weight_path, class_num, embedding=False)
        # 이미지 전처리
        self.img_tensor = self.preprocess_image(img_path)

    ### 두 모델 구조 만들어주는 함수
    def create_model(self, weight_file, class_num, embedding):
        # 모델 초기화  및 가중치 불러오기
        base_model = models.resnet50(weights=None)
        base_model.fc = nn.Linear(2048, class_num)
        
        base_model.load_state_dict(torch.load(weight_file, map_location='cpu'))
        base_model.eval()

        if embedding:
            # 이미지 분류 레이어 제거
            base_model = torch.nn.Sequential(*(list(base_model.children())[:-1]))
        
        return base_model
    
    ### 이미지 전처리 함수
    def preprocess_image(self, img_path):
        # 이미지 로드
        img = Image.open(img_path).convert('RGB')
        # 이미지 변환 정의
        preprocess = transforms.Compose([
            transforms.Resize((self.img_height, self.img_width)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        # 이미지 전처리
        img_tensor = preprocess(img)
        img_tensor = img_tensor.unsqueeze(0)  # 배치 차원 추가 (1, 3, 224, 224)

        return img_tensor
    
    ### 임베딩 결과를 리턴하는 함수
    def get_embedding(self):
        # # 모델을 평가 모드로 설정
        self.emb_model.eval()

        with torch.no_grad():
            # 예측 및 1차원 배열로 변환
            embedding = self.emb_model(self.img_tensor)

        return embedding.view(-1)

    ### 카테고리 예측 결과를 리턴하는 함수
    def get_category(self):
        self.csf_model.eval()
        
        with torch.no_grad():
            category = self.csf_model(self.img_tensor)

        return category


def main(img_path, cate_big):
    model_info_dict = {"onepiece":[r"C:\Users\USER\Desktop\GoodMarket\059.pth", 3]}

    weight = model_info_dict[cate_big][0]
    class_num = model_info_dict[cate_big][1]
    
    base_model = ImageEmbeddingModel(weight, class_num, img_path)
    emb_vec = base_model.get_embedding()
    cate = base_model.get_category()

    return emb_vec, cate

if __name__ == "__main__":
    test_img = r"C:\Users\USER\Pictures\Screenshots\스크린샷 2024-07-17 160254.png"
    emb_vec, category = main(test_img, "onepiece")
    max_value, max_index = torch.max(category, dim=1)
    print("임베딩 size:", emb_vec.shape, "\n카테고리:", max_index.item())