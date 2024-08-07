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
    # 사용 안함
    url_category_list = [['https://www.musinsa.com/categories/item/001010?device=mw&sortCode=3m', 'longsleeve'],
                ['https://www.musinsa.com/categories/item/001004?device=mw&sortCode=3m', 'hood'],
                ['https://www.musinsa.com/categories/item/001005?device=mw&sortCode=3m', 'sweatshirts'],
                ['https://www.musinsa.com/categories/item/001002?device=mw&sortCode=3m', 'shirts_blouse'],
                ['https://www.musinsa.com/categories/item/001001?device=mw&sortCode=3m', 'half_sleeve'],
                ['https://www.musinsa.com/categories/item/001011?device=mw&sortCode=3m', 'sleeveless'],
                ['https://www.musinsa.com/categories/item/001006?device=mw&sortCode=3m', 'knit_sweater'],
                []
    ]

    url_list = [
                'https://www.musinsa.com/categories/item/001010?device=mw&sortCode=3m', # 'longsleeve'
                'https://www.musinsa.com/categories/item/001004?device=mw&sortCode=3m', # 'hood'
                'https://www.musinsa.com/categories/item/001005?device=mw&sortCode=3m', # 'sweatshirts'
                'https://www.musinsa.com/categories/item/001002?device=mw&sortCode=3m', # 'shirts_blouse'
                'https://www.musinsa.com/categories/item/001001?device=mw&sortCode=3m', # 'half_sleeve'
                'https://www.musinsa.com/categories/item/001011?device=mw&sortCode=3m', # 'sleeveless'
                'https://www.musinsa.com/categories/item/001006?device=mw&sortCode=3m', # 'knit_sweater'
                'https://www.musinsa.com/categories/item/003002?device=mw&goodsAttributes=34%5E375&sortCode=3m', # 'long_denim'
                'https://www.musinsa.com/categories/item/003007?device=mw&goodsAttributes=34%5E375&sortCode=3m', # 'long_cotton'
                'https://www.musinsa.com/categories/item/003008?device=mw&goodsAttributes=34%5E375&sortCode=3m', # 'long_slacks'
                'https://www.musinsa.com/categories/item/003009?device=mw&sortCode=3m', # 'shorts'
                'https://www.musinsa.com/categories/item/100004?device=mw&sortCode=3m', # 'mini_skirt'
                'https://www.musinsa.com/categories/item/100005?device=mw&sortCode=3m', # 'midi_skirt'
                'https://www.musinsa.com/categories/item/100006?device=mw&sortCode=3m', # 'long_skirt'
                'https://www.musinsa.com/categories/item/100001?device=mw&sortCode=3m', # 'mini_onepiece'
                'https://www.musinsa.com/categories/item/100002?device=mw&sortCode=3m', # 'midi_onepiece'
                'https://www.musinsa.com/categories/item/100003?device=mw&sortCode=3m', # 'maxi_onepiece'
                'https://www.musinsa.com/categories/item/003010?device=mw&sortCode=1y', # 'jump_suite'
                ]
    
    category_list = [
                    'longsleeve',       # 0
                    'hood',             # 1
                    'sweatshirts',      # 2
                    'shirts_blouse',    # 3
                    'half_sleeve',      # 4
                    'sleeveless',       # 5
                    'knit_sweater',     # 6
                    'long_denim',       # 7
                    'long_cotton',      # 8
                    'long_slacks',      # 9
                    'shorts',           # 10
                    'mini_skirt',       # 11
                    'midi_skirt',       # 12
                    'long_skirt',       # 13
                    'mini_onepiece',    # 14
                    'midi_onepiece',    # 15
                    'maxi_onepiece',    # 16
                    'jump_suite'        # 17
                    ]


    path_list = ['../dataset/top/', '../dataset/bottom/', '../dataset/onepiece/']  # 파일 저장 경로
    num_of_process = 2 # 프로세스 개수

    args_list = [   
                [url_list[0], 3000, path_list[0], category_list[0], 2],
                [url_list[1], 3000, path_list[0], category_list[1], 2],
                [url_list[2], 3000, path_list[0], category_list[2], 2],
                [url_list[3], 4000, path_list[0], category_list[3], 2],
                [url_list[4], 4000, path_list[0], category_list[4], 2],
                [url_list[5], 4000, path_list[0], category_list[5], 2],
                [url_list[6], 4000, path_list[0], category_list[6], 2],
                [url_list[7], 3000, path_list[1], category_list[7], 2],
                [url_list[8], 3000, path_list[1], category_list[8], 2],
                [url_list[9], 3000, path_list[1], category_list[9], 1],
                [url_list[10], 5000, path_list[1], category_list[10], 1],
                [url_list[11], 2000, path_list[1], category_list[11], 1],
                [url_list[12], 2000, path_list[1], category_list[12], 1],
                [url_list[13], 2000, path_list[1], category_list[13], 1],
                [url_list[14], 2000, path_list[2], category_list[14], 1],
                [url_list[15], 2000, path_list[2], category_list[15], 1],
                [url_list[16], 2000, path_list[2], category_list[16], 1],
                [url_list[17], 1000, path_list[2], category_list[17], 1],
                 ]

    # 멀티프로세싱
    #pool = Pool(processes= num_of_process)
    
    #pool.starmap(method.get_images_by_scrolling, args_list[:3])
    #pool.starmap(method.get_images_by_scrolling, args_list[3:6])
    #pool.starmap(method.get_images_by_scrolling, args_list[6:9])
    #pool.starmap(method.get_images_by_scrolling, args_list[9:12])
    #pool.starmap(method.get_images_by_scrolling, args_list[12:15])
    #pool.starmap(method.get_images_by_scrolling, args_list[15:])

    # 그냥 실행
    #for args in args_list[9:]:
    #   method.get_images_by_scrolling(*args)

if __name__ == '__main__':
    main()