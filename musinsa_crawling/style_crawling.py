import os
import time
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import multiprocessing
from multiprocessing import Pool
import method

def main():
    urls_and_categories = [
        #('https://www.musinsa.com/categories/item/001002?device=mw&sortCode=3m', '셔츠_블라우스'),
        #('https://www.musinsa.com/categories/item/001001?device=mw&sortCode=3m', '반소매'),
        #('https://www.musinsa.com/categories/item/001006?device=mw&sortCode=3m', '니트_스웨터'),
        #('https://www.musinsa.com/categories/item/001005?device=mw&sortCode=3m', '맨투맨'),
        ('https://www.musinsa.com/categories/item/003009?device=mw&sortCode=3m', '숏팬츠'),
        ('https://www.musinsa.com/categories/item/003002?device=mw&sortCode=1y', '데님팬츠'),
        ('https://www.musinsa.com/categories/item/003007?device=mw&sortCode=1y', '코튼팬츠')
        #
    ]

    save_path = '../dataset/'  # 파일 저장 경로
    max_count = 5000  # 가져올 필터링된 href 개수
    num_of_process = 8 # 프로세스 개수

    for url, category in urls_and_categories:
        
        # 필터링된 hrefs 가져오기
        method.get_filtered_hrefs(url, save_path, max_count, category)

        url_file_path = os.path.join(save_path, '상의', category, f'{category}_url.txt')  # 필터링된 URL 파일 경로
        image_path = os.path.join(save_path, '상의', category)  # 이미지 저장 폴더 경로
        
        # 수집한 url 읽기
        #with open(text_file_path, 'w', encoding='utf-8') as text_out_file:
        with open(url_file_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f]
        
        index_list = []
        for num in range(num_of_process):
            if num == num_of_process - 1:
                index_list.append(range((len(urls)//num_of_process) * num, len(urls)))
            else:
                index_list.append(range((len(urls)//num_of_process) * num, (len(urls)//num_of_process) * (num + 1)))
            #print(index_list[num])
        
        args = []

        # 0 ~ 15, 16 ~ 31, 32 ~ 47 48 49        
        for num in range(num_of_process):
            text_file_path = os.path.join(save_path, '상의', category, f'{category}_text{num}.txt')  # 텍스트 저장 경로

            start = (max_count//num_of_process) * num + num
            end = (max_count//num_of_process) * (num + 1) + num
            print((start, end))
            
            if num == num_of_process - 1:
                args.append((url_file_path, index_list[num], text_file_path, image_path, category, start, max_count - 1))
            else:
                args.append((url_file_path, index_list[num], text_file_path, image_path, category, start, end))

        pool = Pool(processes= num_of_process)
        pool.starmap(method.extract_text_and_images, args)

        # 텍스트와 이미지 추출
        #method.extract_text_and_images(url_file_path, text_file_path, image_path,category, max_count)

if __name__ == '__main__':
    main()
