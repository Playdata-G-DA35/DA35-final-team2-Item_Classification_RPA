import chromadb
import os
import sys
import django

# Django 설정 초기화
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GoodMarket.settings')
django.setup()

def get_chromadb_collection(collection_name="product_images", db_path="./chroma_db_data"):
    client = chromadb.PersistentClient(path=db_path)
    try:
        return client.get_collection(name=collection_name)
    except ValueError as e:
        if 'does not exist' in str(e):
            print(f"Collection '{collection_name}' does not exist. Creating new collection.")
            return client.create_collection(name=collection_name)
        raise ValueError(f"ChromaDB collection error: {str(e)}")

def list_stored_embeddings():
    # ChromaDB 컬렉션 가져오기
    images_collection = get_chromadb_collection()
    
    # 저장된 데이터 조회
    stored_data = images_collection.get(include=['embeddings', 'metadatas'])
    
    if not stored_data or not stored_data.get('embeddings'):
        print("Error: No embeddings found in ChromaDB.")
        return

    print("Stored embeddings in ChromaDB:")
    for idx, emb in enumerate(stored_data['embeddings']):
        image_id = stored_data['metadatas'][idx]['product_file_id']
        print(f"Image ID: {image_id}")
        

if __name__ == "__main__":
    list_stored_embeddings()
