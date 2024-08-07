import os
import time
import requests
import multiprocessing
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def get_filtered_hrefs(url, save_path, max_count, cat_name):
    # 해쉬태그가 없는 상품도 있어서 max_count의 1.5배
    max_url_num = int(max_count * 1.5)

    # 저장할 파일 경로 설정
    url_file_path = os.path.join(save_path, '상의', cat_name, f'{cat_name}_url.txt')
    
    # 저장 폴더가 없으면 생성
    if not os.path.exists(os.path.dirname(url_file_path)):
        os.makedirs(os.path.dirname(url_file_path))
    
    # Chrome WebDriver 설정
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver = webdriver.Chrome(service=Service())
    
    # 웹사이트로 이동
    driver.get(url)
    #time.sleep(2)

    # WebDriverWait 객체 생성
    wait = WebDriverWait(driver, 3)

    # 항목의 href 목록 가져오기
    hrefs = []
    try:
        #while len(hrefs) < max_url_num:
        while (1):
            # 모든 a 태그의 href 속성 추출
            item_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="root"]/main/div/section[3]/div[1]//a')))
            new_hrefs = [item.get_attribute('href') for item in item_elements if item.get_attribute('href')]
            hrefs.extend(new_hrefs)
            hrefs = list(dict.fromkeys(hrefs))  # 중복 제거
            
            # 페이지 스크롤
            driver.execute_script("window.scrollBy(0, 10000);")
            #pyautogui.press('end')
            time.sleep(0.2)  # 페이지 로딩 대기

            # 'https://www.musinsa.com/app/goods'로 시작하는 href만 필터링
            filtered_hrefs = [url for url in hrefs if url.startswith('https://www.musinsa.com/app/goods')]

            print(f"Found {len(filtered_hrefs)} hrefs.")

            # max_url_num 초과 시 종료
            if len(filtered_hrefs) >= max_url_num:
                break

    except Exception as e:
        print(f"Error extracting hrefs: {e}")

    # 최대 max_count 개수만큼 필터링된 hrefs를 자르기
    if(len(filtered_hrefs) > max_url_num):
        filtered_hrefs = filtered_hrefs[:max_url_num]
    
    # 필터링된 url을 파일에 저장
    with open(url_file_path, 'w', encoding='utf-8') as f:
        for href in filtered_hrefs:
            f.write(f"{href}\n")
    
    # 브라우저 종료
    driver.quit()

def extract_text_and_images(url_file_path, index_list, text_file_path, image_path, category, count_start, count_end):  #경로
    # Chrome WebDriver 설정
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver = webdriver.Chrome(service=Service())

    # 이미지 저장 폴더 경로
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    #add_path = f'{index_list[0]}.txt'
    #t_path = 

    # 텍스트와 이미지 저장 파일 열기 (쓰기 모드, UTF-8 인코딩)
    with open(text_file_path, 'w', encoding='utf-8') as text_out_file:        
        # 필터링된 URL 읽기
        with open(url_file_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f]

        # WebDriverWait 객체 생성
        wait = WebDriverWait(driver, 5)  # 5초까지 대기
        
        valid_index = count_start  # 유효한 항목의 번호
        
        # product_count만큼 수집
        for index in index_list:
            url = urls[index]
            if valid_index > count_end:
                break 
            if not url:
                continue  # URL이 빈 문자열이면 건너뜀
            
            driver.get(url)
            #time.sleep(1)  # 필요에 따라 조정 가능
            #
            
            try:
                # 세부 페이지에서 텍스트 추출
                hashtag_xpath = '//*[@id="root"]/div[@class="sc-29qvgg-0 iXHguF"]'
                text_element = wait.until(EC.presence_of_element_located((By.XPATH, hashtag_xpath)))
                hashtag_contents = text_element.text.strip().split('\n')
                print('index is ', valid_index, '\nhashtag is \n', hashtag_contents)

                # 텍스트를 하나의 줄로 연결
                if hashtag_contents:
                    item_text = ' '.join(hashtag_contents)
                    text_out_file.write(f"{valid_index}. {item_text}\n")
                    #print(f"Text for URL '{url}' added to file.")
                    
                    # 이미지 추출 및 저장
                    image_xpath = '//div[contains(@class, "swiper-slide-active")]/div/img'
                    image_element = wait.until(EC.presence_of_element_located((By.XPATH, image_xpath)))
                    image_url = image_element.get_attribute('src')

                    # 이미지 다운로드 및 저장
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        image_filename = os.path.join(image_path, f"{category}_{valid_index}.jpg")
                        with open(image_filename, 'wb') as img_file:
                            img_file.write(image_response.content)
                        #print(f"Image for URL '{url}' saved as '{image_filename}'.")
                    
                    valid_index += 1  # 유효한 항목 번호 증가

                else:
                    print(f"No text found for URL '{url}'. Skipping image download.")
                    pass
                
            except Exception as e:
                valid_index = valid_index - 1
                print(f"Error processing URL '{url}': {e}")
                #print(f"Error processing URL : {url}")

            # 페이지 로딩 대기
            #time.sleep(2)  # 필요에 따라 조정 가능

    # 브라우저 종료
    driver.quit()

# 이미지 다운로드 및 저장 함수
def download_image(image_url, file_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Image saved successfully as {file_path}")
    else:
        print(f"Failed to download image from {image_url}")

# 스크롤 함수
def scroll_down(driver, scroll_step, scroll_pause_time):
    # 페이지의 현재 높이 가져오기
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # 페이지의 끝까지 스크롤
        driver.execute_script(f"window.scrollBy(0, {scroll_step});")
        
        # 스크롤 후 로딩 시간 대기
        time.sleep(scroll_pause_time)
        
        # 새로운 페이지 높이 계산
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # 만약 새로운 높이가 마지막 높이와 같다면 (더 이상 스크롤할 내용이 없음)
        if new_height == last_height:
            break
        
        last_height = new_height

def get_images_by_scrolling(url, max_num, save_path, cat_name, pause):
    """_summary_

    Args:
        url (_str_): 크롤링할 대상 URL
        max_num (_int_): 가져올 이미지의 개수
        save_path (_str_): 저장 경로(/로 끝나야함)
        cat_name (_str_): 카테고리 이름
        pause (_float_or_int_): 스크롤 후 정지할 시간
    """

    # 저장 경로 설정
    save_path = f'{save_path}{cat_name}/'
    #print(save_path)
    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))

    driver = webdriver.Chrome(service=Service())
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    define_list = []
    while True:
        # scroll
        driver.execute_script("window.scrollBy(0, 8000);")
        time.sleep(pause)

        # CLASS_NAME 조건으로 수집
        item_elements = driver.find_elements(By.CLASS_NAME, "category__sc-rb2kzk-9.eSSKjG")

        # 중복은 overlap_list로 빼냄
        src_list = []
        overlap_list = []

        for item in item_elements:
            src = item.get_attribute('src')
            if src not in define_list:
                define_list.append(src)
            else:
                overlap_list.append(src)

        # 개수 확인을 위한 print
        #print('num of src', len(define_list), ', num of overlap src', len(overlap_list), ', num of elements', len(item_elements))
        if(len(define_list) > max_num):
            print('final num of src is', len(define_list))
            break
    
    driver.quit()
    
    # 이미지를 저장
    index = 0
    for src in define_list[:max_num]:
        img = requests.get(src)
        filepath = f'{save_path}{cat_name}_{index}.jpg'
        with open(filepath, 'wb') as img_file:
            img_file.write(img.content)
            index += 1