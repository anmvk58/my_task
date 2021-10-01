import helpers as utils

base_path = "D:\\Source\\SSIS\\SSIS_srv20\\ETL_G01_TRACKING\\ETL_G01_TRACKING\\VPB_ETL_TRACKING"

if __name__ == '__main__':
    # Get list key word to find
    key_word = utils.get_data('C:\\Users\\anmv1\\Desktop\\New folder\\LIST_TABLE_TMP.xlsx')

    # Get list file need to check
    list_file = utils.get_list_file(base_path)

    data = []

    # Make data when search
    for file in list_file:
        for key in key_word:
            file_path = (''.join([base_path,"\\" ,file]))
            content = open(file_path, "r", encoding="utf8").read()
            if key in content:
                data.append((file_path, key))
                print(file_path, key)


    # Write result
    utils.write_result_to_xlsx("C:\\Users\\anmv1\\Desktop\\", data)
