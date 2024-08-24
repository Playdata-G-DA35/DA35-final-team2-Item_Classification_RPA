# test_import.py

import sys
import time
import torch
from image_embedding import main

if __name__ == "__main__":
    # 커맨드라인 인수로부터 이미지 경로를 받습니다
    test_img = sys.argv[1]

    s = time.time()

    # Call the main function with the updated image
    emb_vec, category = main(test_img, "onepiece")

    # Find the maximum value and index in the category tensor
    max_value, max_index = torch.max(category, dim=1)

    # Print the embedding size and the category index to the terminal
    print(f"임베딩 size: {emb_vec.shape}\n카테고리: {max_index.item()}")

    # Print the time taken for the process
    print("Processing time:", time.time() - s)
