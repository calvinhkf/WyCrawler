import file_util


def combine_lib():
    lib_array1 = file_util.read_json("lib_to_crawl1.txt")
    lib_array2 = file_util.read_json("lib_to_crawl2.txt")
    print(len(lib_array1))
    print(len(lib_array2))
    # lib_set1 = set(lib_array1)
    # lib_set2 = set(lib_array2)
    # print(len(lib_set1))
    # print(len(lib_set2))
    lib_array1.extend(lib_array2)
    print(len(lib_array1))
    lib_set = set(lib_array1)
    print(len(lib_set))
    result_lib = list(lib_set)
    file_util.write_json("jars.txt", result_lib)
    # for lib in lib_array2:
    #     if lib not in lib_array1:
    #         lib_array1.append(lib)
    # print(len(lib_array1))
    # file_util.write_json("jars1.txt", lib_array1)

# combine_lib()