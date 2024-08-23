from image_embedding import main
import time
import torch

s = time.time()
test_img = r"C:\Users\USER\Pictures\Screenshots\스크린샷 2024-07-17 160254.png"
emb_vec, category = main(test_img, "onepiece")
max_value, max_index = torch.max(category, dim=1)
print("임베딩 size:", emb_vec.shape, "\n카테고리:", max_index.item())

print(time.time() - s)