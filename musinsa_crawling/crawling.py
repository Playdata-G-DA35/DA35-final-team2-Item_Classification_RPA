import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui

def get_img_tag(url, name, save_path, end_num):
    # 브라우저 창 제거
    #chrome_options = Options()
    #chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--no-sandbox")
    #chrome_options.add_argument("--disable-dev-shm-usage")

    # Chrome WebDriver 설정
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))#, options=chrome_options)
    
    # 텍스트 저장 파일 경로
    text_filename = save_path + name + '.txt'

    # 이미지 저장 폴더 경로
    image_folder = save_path

    # 이미지 저장 폴더가 없으면 생성
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # 웹사이트로 이동
    driver.get(url)

    # WebDriverWait 객체 생성
    wait = WebDriverWait(driver, 3)  # 3초까지 대기

    # 텍스트 저장을 위한 파일 열기 (쓰기 모드, UTF-8 인코딩)
    with open(text_filename, 'w', encoding='utf-8') as text_file:
        # List to store generated XPaths
        xpaths = []

        # Iterate over i from 1 to 30, skipping i = 2
        for i in range(10, end_num//3 + 20):
            if i == 2:
                continue
            for x in range(1, 4):
                xpath = f'//*[@id="root"]/main/div/section[3]/div[1]/div/div[{i}]/div[{x}]/div[1]/figure/a'
                xpaths.append(xpath)

        # Variable to maintain numbering of results
        result_number = 1

        # 각 항목 처리
        for item_xpath in xpaths:
            if (result_number//6 == 0 & result_number > 2):
                pyautogui.press('pagedown')
            try:
                # 항목 클릭
                item_element = wait.until(EC.element_to_be_clickable((By.XPATH, item_xpath)))
                item_element.click()

                # 세부 페이지에서 텍스트 추출
                text_xpath = '//*[@id="root"]/div[@class="sc-29qvgg-0 iXHguF"]'
                text_element = wait.until(EC.presence_of_element_located((By.XPATH, text_xpath)))
                item_texts = text_element.text.strip().split('\n')

                # 텍스트를 하나의 줄로 연결
                item_text = ' '.join(item_texts)
                text_file.write(f"{result_number}. {item_text}\n")
                print(f"Text for item {result_number} added to file.")

                # 이미지 저장
                image_xpath = '//div[contains(@class, "swiper-slide-active")]/div/img'
                image_element = wait.until(EC.presence_of_element_located((By.XPATH, image_xpath)))
                image_url = image_element.get_attribute('src')

                # 다운로드 및 저장
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image_path = os.path.join(image_folder, f'{name}{result_number}.jpg')
                    with open(image_path, 'wb') as img_file:
                        img_file.write(image_response.content)
                    print(f"Image for item {result_number} saved as '{image_path}'.")
                    
                # 번호 증가
                result_number += 1

            except Exception as e:
                print(f"Error processing item {result_number}: {e}")
            finally:
                # 목록 페이지로 돌아가기
                driver.back()

            # 페이지 로드 대기
            time.sleep(1)  # 이 대기는 WebDriverWait 사용 시 필요 없을 수 있음

            
            if result_number > end_num:
                break

    # 브라우저 종료
    driver.quit()

def main():
    # 카테고리 url
    url = ['https://www.musinsa.com/categories/item/001010?device=mw', # 0 긴소매
           'https://www.musinsa.com/categories/item/001006?device=mw', # 1 니트,스웨터
           'https://www.musinsa.com/categories/item/001005?device=mw', # 2 맨투맨
           'https://www.musinsa.com/categories/item/001011?device=mw', # 3 민소매
           'https://www.musinsa.com/categories/item/001001?device=mw', # 4 반소매
           'https://www.musinsa.com/categories/item/001002?device=mw', # 5 셔츠,블라우스
           'https://www.musinsa.com/categories/item/001004?device=mw', # 6 후드티
           ]
    # 이미지 파일명 name.jpg
    name = ['긴소매',           # 0
            '니트,스웨터',      # 1
            '맨투맨',           # 2
            '민소매',           # 3
            '반소매',           # 4
            '셔츠,블라우스',    # 5
            '후드티',           # 6
            ]
    save_path = '../dataset/상의/' # 파일 저장 경로
    end_num = 300 # 크롤링할 데이터 개수

    #get_img_tag(url[6], name[6], save_path + name[6] + '/', end_num)
    for idx in [0, 1, 2]:
        get_img_tag(url[idx], name[idx], save_path + name[idx] + '/', end_num)

if __name__ == '__main__':
    main()