import pandas as pd
import re

def load_data(save_dir, cat_name):
    with open(f'{save_dir + cat_name}/{cat_name}.txt', 'r', encoding= 'UTF8') as f:
        raw_data = f.readlines()

    data = []
    for line in raw_data:
        data.append(line.strip().split(' ')[1:])

    return(data)

def get_counts(list):
    counts = {}
    for item in list:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1

    return counts

def make_labeldict(data):
    tag_list = [] # 태그 전체 리스트
    
    for row in data:
        for tag in row: # 숫자와 영어가 포함된 해시태그 제거
            if not re.search(r'\d', tag) and not re.search(r'[a-zA-Z]', tag):
                tag_list.append(tag)

    tag_dict = get_counts(tag_list)
    tag_dict = dict(sorted(tag_dict.items(), key= lambda item: item[1], reverse= True))

    # 등장 횟수가 2개 미만인 해시태그 제거 (임의로 2개로 지정)
    tag_dict = {tag: count for tag, count in tag_dict.items() if count > 1}

    print(tag_dict)
    return tag_dict

def make_df(dict, num, data):
    label_list = list(dict.keys())[:num]
    print(label_list)
    df = pd.DataFrame(columns=label_list) # 상위 num개의 해쉬태그를 열로 가진 dataframe 생성

    for line in data:
        # 해시태그 3개 이상인 경우만 처리
        if len(line) > 2:
            encoded_line = [] # 새로 추가될 행

            for item in label_list: # index열 무시
                if item in line:
                    encoded_line.append(1)
                else:
                    encoded_line.append(0)
            
            # 해시태그 개수 추가
            hashtag_count = sum(encoded_line)
            encoded_line.append(hashtag_count)

            new_row = pd.DataFrame([encoded_line], columns= label_list + ['hashtag_count'])
            df = pd.concat([df, new_row], ignore_index= True)

    return df

def make_csv(data_dir, save_dir, name_list, label_num):
    for cat_name in name_list:
        data = load_data(data_dir, cat_name)
        tag_dict = make_labeldict(data)
        df = make_df(tag_dict, label_num, data)
        df.to_csv(f'{save_dir}/{cat_name}.csv', index=False)