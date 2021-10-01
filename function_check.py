def scan_by_exact_string (file_paths, str_to_scan):
    str_to_scan = str_to_scan.upper()
    l_prefix = [' ', '\t', '\n' , '&#XA', '.']
    l_suffix = [' ', '\t', '\n' , '&#XA', '<', ';']
    l_prefix_str = [prefix + str_to_scan for prefix in l_prefix]
    l_suffix_str = [str_to_scan + suffix for suffix in l_suffix]
    output_file_paths = []
    print(f"=========Scanning for string '{str_to_scan}'===========")
    for i, file_path in enumerate(file_paths):
        f = open(file_path, "r", encoding='utf-8', errors='ignore')
        encoded_f = f.read().upper()
        if any(str_to_scan in encoded_f for str_to_scan in l_prefix_str) and any(str_to_scan in encoded_f for str_to_scan in l_suffix_str):
    #     if str_to_scan in encoded_f:
            output_file_paths.append(file_path)
        if i % 200 == 0:
            print(f"Scanned {i}/{len(file_paths)} \n--'{str_to_scan}' founded in {len(output_file_paths)} files")
    print(f"=========Done scanning: string '{str_to_scan}' founded in {len(output_file_paths)} files===========")
    return output_file_paths
