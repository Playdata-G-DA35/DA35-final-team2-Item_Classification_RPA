import data_prepro_method

def main():
    name_list = ['긴소매',          # 0
                '니트_스웨터',      # 1
                '맨투맨',           # 2
                '민소매',           # 3
                '반소매',           # 4
                '셔츠_블라우스',    # 5
                '후드티',           # 6
                ]

    data_dir1 = '../dataset/상의/'
    data_dir2 = '../dataset/아우터/'
    data_dir3 = '../dataset/하의/'
    save_dir = 'csv/'
    label_num = 1000

    data_prepro_method.make_csv(data_dir1, save_dir, name_list, label_num)

if __name__ == '__main__':
    main()