import os

def make_path_list(path):
    name_list = os.listdir(path)
    path_list = []
    for name in name_list:
        path_list.append(f'{path}/{name}')
    
    return path_list, name_list

def test_by_musinsa(source_path, weight_path, save_path, save_name, conf):
    """_summary_
    save_path에 save_name 폴더를 생성해 결과를 카테고리별로 나눠서 모두 저장
    
    Args:
        source_path (_type_): detection 실행 대상 이미지의 경로
        weight_path (_type_): 사용할 weight의 경로
        save_path (_type_): 결과를 저장할 경로
        save_name (_type_): 저장할 이름
    """
    # 저장 디렉토리 생성
    os.makedirs(f'{save_path}/{save_name}', exist_ok= True)

    large_category = source_path.split('/')[-2] # ex) top, ...
    cat_name = source_path.split('/')[-1] # ex) hood, ...
    save_dir = f'{save_path}/{save_name}/{large_category}/{cat_name}'
    
    # 착샷 detect
    os.system(f'python yolov5/detect.py --source {source_path}/person --weights {weight_path} --conf {conf} --save-txt --save-csv --save-crop --project {save_dir} --name person --data data.yaml')
    
    # 제품샷 detect
    os.system(f'python yolov5/detect.py --source {source_path}/product --weights {weight_path} --conf {conf} --save-txt --save-csv --save-crop --project {save_dir} --name product --data data.yaml')