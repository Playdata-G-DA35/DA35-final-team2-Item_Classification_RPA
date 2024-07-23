import pandas as pd
import numpy as np
import os
import shutil # 파일 복사
import data_prepro_method

from sklearn.cluster import KMeans

def clustering_and_classify(clusters_num, cat_name, image_dir):
        # csv 불러오기
        df = pd.read_csv(f'{csv_path + cat_name}.csv', index_col= 0)
        df_copy = df.copy()

        # 군집점 개수 = clusters_num으로 클러스터링
        clust_model = KMeans(n_clusters= clusters_num)
        clust_model.fit(df_copy)
        centers = clust_model.cluster_centers_

        # class열 추가한 데이터 프레임
        pred = clust_model.predict(df_copy)
        clusted_df = df.copy()
        clusted_df['class'] = pred
        
        # 결과 저장
        #clusted_df.to_csv(f'{csv_path}clusted_{cat_name}.csv')

        for label in range(clusters_num):
            # 클러스터링 된 이미지 저장 디렉터리를 생성
            os.makedirs(f'clustered_image/{cat_name}/c_num={clusters_num}/{label}', exist_ok= True)

            # csv에서 클래스 == label인 인덱스들 추출
            index_list = list(clusted_df[clusted_df['class'] == label].index)
            index_list = np.array(index_list) + 1
            index_list = list(index_list)
            print(np.shape(index_list))

            # index를 기준으로 파일 복사해오기
            for index in index_list:
                shutil.copy(f'{image_dir}/{cat_name}/' + f'{index}.jpg', f'clustered_image/{cat_name}/c_num={clusters_num}/{label}/' + f'{index}.jpg')

# 전역 변수
name_list = ['긴소매',           # 0
            '니트,스웨터',      # 1
            '맨투맨',           # 2
            '민소매',           # 3
            '반소매',           # 4
            '셔츠,블라우스',    # 5
            '후드티',           # 6
            ]

csv_path = 'csv/'

img_dir_list = ['../dataset/상의',
                  '../dataset/아우터',
                  '../dataset/하의',]

def main():
     # clusters_num 임의 설정
     clusters_num_list = [4, 13]
     
     for clsts_num in clusters_num_list:
          clustering_and_classify(clsts_num, name_list[0], img_dir_list[0])
    

if __name__ == '__main__':
    main()