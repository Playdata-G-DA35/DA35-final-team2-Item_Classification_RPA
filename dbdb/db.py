import pandas as pd
import chromadb
from tqdm import tqdm
import torch
from torchvision import models, transforms
from PIL import Image
import os
import shutil

# 1. CSV 파일 읽기
embedding_csv_path = 'C:/Users/USER/Desktop/dbdb/embs.csv'
df = pd.read_csv(embedding_csv_path, header=None)

# 각 행의 인덱스를 이미지 ID로 사용
image_ids = [str(i) for i in df.index.tolist()]  # 인덱스를 문자열로 변환
embeddings = df.values.tolist()  # 모든 임베딩 벡터 추출

# 2. ChromaDB 클라이언트 설정 및 데이터 추가
client = chromadb.PersistentClient(path="./chroma_db_data")

try:
    images_collection = client.get_collection(name="images")
except ValueError as e:
    if 'does not exist' in str(e):
        images_collection = client.create_collection(name="images")  # dimension 인자 제거
    else:
        raise


# 데이터 추가
chunk_size = 1024
total_chunks = len(embeddings) // chunk_size + 1

for chunk_idx in tqdm(range(total_chunks)):
    start_idx = chunk_idx * chunk_size
    end_idx = (chunk_idx + 1) * chunk_size
    
    chunk_embeddings = embeddings[start_idx:end_idx]
    chunk_ids = image_ids[start_idx:end_idx]
    chunk_metadatas = [{"image_id": img} for img in chunk_ids]
    
    images_collection.add(embeddings=chunk_embeddings, ids=chunk_ids, metadatas=chunk_metadatas)

print("임베딩 데이터가 ChromaDB에 추가되었습니다.")

# 3. 이미지 임베딩을 위한 모델 불러오기
model = models.resnet50(pretrained=True)
model = torch.nn.Sequential(*(list(model.children())[:-1]))  # 마지막 레이어 제거
model.eval()

preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# 4. 검색할 이미지 선택 및 임베딩 생성
image_folder = 'C:/Users/USER/Desktop/dbdb/Bottom'  # 이미지 폴더 경로
query_image_filename = '3.jpg'
query_image_path = os.path.join(image_folder, query_image_filename)

if not os.path.isfile(query_image_path):
    raise FileNotFoundError(f"지정된 이미지 파일이 존재하지 않습니다: {query_image_path}")

query_image = Image.open(query_image_path).convert('RGB')
query_input_tensor = preprocess(query_image).unsqueeze(0)

with torch.no_grad():
    query_embedding = model(query_input_tensor).squeeze().numpy().tolist()


# 5. 유사 이미지 검색
result = images_collection.query(
    query_embeddings=[query_embedding],
    n_results=3  # 검색할 이미지 개수
)

# 6. 검색된 유사 이미지 파일을 'top' 폴더에 저장
top_folder = 'C:/Users/USER/Desktop/dbdb/top'
os.makedirs(top_folder, exist_ok=True)  # 'top' 폴더가 없으면 생성

for match in result["metadatas"][0]:
    image_id = match['image_id']
    # CSV의 인덱스가 실제 파일 이름이므로 직접 사용할 수 있음
    image_path = os.path.join(image_folder, f'{image_id}.jpg')  # .jpg 확장자
    if os.path.isfile(image_path):
        # 'top' 폴더로 이미지 복사
        destination_path = os.path.join(top_folder, f'{image_id}.jpg')
        shutil.copy(image_path, destination_path)
        print(f"이미지 {image_id}가 '{top_folder}' 폴더에 저장되었습니다.")
    else:
        print(f"Image file not found: {image_path}")
