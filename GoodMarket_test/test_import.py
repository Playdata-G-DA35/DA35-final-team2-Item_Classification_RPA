import os

# 상대 경로를 지정합니다.
relative_path = "/media/test/crops/Bottom/1622808.jpg"

# 현재 작업 디렉터리를 가져옵니다.
current_dir = os.getcwd()

# 절대 경로를 생성합니다.
absolute_path = os.path.join(current_dir, relative_path.lstrip('/'))

print(absolute_path)  # 절대 경로 출력
