import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_filtered_hrefs(url, save_path, max_count, item_path):
    # 저장할 파일 경로 설정
    hrefs_filename = os.path.join(save_path, item_path, 'url.txt')
    
    # 저장 폴더가 없으면 생성
    if not os.path.exists(os.path.dirname(hrefs_filename)):
        os.makedirs(os.path.dirname(hrefs_filename))
    
    # Chrome WebDriver 설정
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    # 웹사이트로 이동
    driver.get(url)

    # WebDriverWait 객체 생성
    wait = WebDriverWait(driver, 1)  

    # 항목의 href 목록 가져오기
    hrefs = []
    try:
        while len(hrefs) < max_count:
            # 모든 a 태그의 href 속성 추출
            item_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="root"]/main/div/section[3]/div[1]//a')))
            new_hrefs = [item.get_attribute('href') for item in item_elements if item.get_attribute('href')]
            hrefs.extend(new_hrefs)
            hrefs = list(dict.fromkeys(hrefs))  # 중복 제거
            print(f"Found {len(hrefs)} hrefs.")
            
            # 페이지 스크롤
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(0.1)  # 페이지 로딩 대기

            # 최대 개수 초과 시 종료
            if len(hrefs) >= max_count:
                break
    except Exception as e:
        print(f"Error extracting hrefs: {e}")

    # 'https://www.musinsa.com/app/goods'로 시작하는 href만 필터링
    filtered_hrefs = [href for href in hrefs if href.startswith('https://www.musinsa.com/app/goods')]
    
    # 최대 max_count 개수만큼 필터링된 hrefs를 자르기
    filtered_hrefs = filtered_hrefs[:max_count]
    
    # 필터링된 hrefs를 파일에 저장
    with open(hrefs_filename, 'w', encoding='utf-8') as f:
        for href in filtered_hrefs:
            f.write(f"{href}\n")
    
    # 브라우저 종료
    driver.quit()

def extract_text_and_images(filtered_file, text_file, image_folder, product_num):
    # Chrome WebDriver 설정
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # 텍스트 저장 파일 경로
    text_filename = text_file

    # 이미지 저장 폴더 경로
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # 텍스트와 이미지 저장 파일 열기 (쓰기 모드, UTF-8 인코딩)
    with open(text_filename, 'w', encoding='utf-8') as text_out_file:
        
        # 필터링된 URL 읽기
        with open(filtered_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f]

        # WebDriverWait 객체 생성
        wait = WebDriverWait(driver, 1)  # 10초까지 대기

        # URL 처리
        
        valid_index = 0  # 유효한 항목의 번호
        for url in urls:
            if valid_index >= product_num:
                break  # valid_index가 200을 초과하면 종료
            if not url:
                continue  # URL이 빈 문자열이면 건너뜀
            driver.get(url)
            try:
                # 세부 페이지에서 텍스트 추출
                text_xpath = '//*[@id="root"]/div[@class="sc-29qvgg-0 iXHguF"]'
                text_element = wait.until(EC.presence_of_element_located((By.XPATH, text_xpath)))
                item_texts = text_element.text.strip().split('\n')

                # 텍스트를 하나의 줄로 연결
                if item_texts:
                    item_text = ' '.join(item_texts)
                    text_out_file.write(f"{valid_index}. {item_text}\n")
                    print(f"Text for URL '{url}' added to file.")
                    
                    # 이미지 추출 및 저장
                    image_xpath = '//div[contains(@class, "swiper-slide-active")]/div/img'
                    image_element = wait.until(EC.presence_of_element_located((By.XPATH, image_xpath)))
                    image_url = image_element.get_attribute('src')

                    # 이미지 다운로드 및 저장
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        image_filename = os.path.join(image_folder, f"{valid_index}.jpg")
                        with open(image_filename, 'wb') as img_file:
                            img_file.write(image_response.content)
                        print(f"Image for URL '{url}' saved as '{image_filename}'.")

                    valid_index += 1  # 유효한 항목 번호 증가

                else:
                    print(f"No text found for URL '{url}'. Skipping image download.")
                
            except Exception as e:
                print(f"Error processing URL '{url}': {e}")

            # 페이지 로딩 대기
            time.sleep(0.1)  # 필요에 따라 조정 가능

    # 브라우저 종료
    driver.quit()

def main():
    url = 'https://www.musinsa.com/categories/item/001010?device=mw'  #  URL
    save_path = './'  # 파일 저장 경로
    max_count = 500  # 가져올 필터링된 href 개수
    item_path = '상의/긴소매'  # 경로 설정
    
    get_filtered_hrefs(url, save_path, max_count*2, item_path)

    filtered_file = os.path.join(save_path, item_path, 'url.txt')  # 필터링된 URL 파일
    text_file = os.path.join(save_path, item_path, 'text.txt')  # 텍스트 저장 파일
    image_folder = os.path.join(save_path, item_path)  # 이미지 저장 폴더

    extract_text_and_images(filtered_file, text_file, image_folder, max_count)

if __name__ == '__main__':
    main()