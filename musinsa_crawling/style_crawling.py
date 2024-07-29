import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import method.py

def main():
    urls_and_categories = [
        ('https://www.musinsa.com/categories/item/001005?device=mw', '상의/맨투맨'),
        ('https://www.musinsa.com/categories/item/001002?device=mw', '상의/셔츠_블라우스'),
        ('https://www.musinsa.com/categories/item/001004?device=mw', '상의/후드티'),
        ('https://www.musinsa.com/categories/item/001006?device=mw', '상의/니트_스웨터'),
        ('https://www.musinsa.com/categories/item/001010?device=mw', '상의/긴소매'),
        ('https://www.musinsa.com/categories/item/001001?device=mw', '상의/반소매'),
        ('https://www.musinsa.com/categories/item/001011?device=mw', '상의/민소매')
    ]

    save_path = './'  # 파일 저장 경로
    max_count = 100  # 가져올 필터링된 href 개수

    for url, category in urls_and_categories:
        # item_path 설정
        item_path = category
        
        # 필터링된 hrefs 가져오기
        method.get_filtered_hrefs(url, save_path, max_count*2, item_path)

        filtered_file = os.path.join(save_path, item_path, 'url.txt')  # 필터링된 URL 파일
        text_file = os.path.join(save_path, item_path, 'text.txt')  # 텍스트 저장 파일
        image_folder = os.path.join(save_path, item_path)  # 이미지 저장 폴더

        # 텍스트와 이미지 추출
        method.extract_text_and_images(filtered_file, text_file, image_folder, max_count)

if __name__ == '__main__':
    main()
