import database
from file_util import write_json, read_json

projs_3_month = [2, 4, 5, 6, 7, 8, 9, 10, 11, 15, 18, 20, 21, 23, 30, 32, 34, 37, 38, 40, 41, 42, 49, 50, 52, 56, 60, 63, 68, 69, 70, 73, 78, 79, 80, 83, 84, 85, 93, 95, 108, 115, 116, 118, 123, 127, 128, 130, 131, 138, 141, 143, 145, 147, 148, 152, 155, 160, 163, 164, 165, 166, 169, 171, 172, 173, 174, 175, 177, 178, 180, 184, 186, 188, 189, 190, 192, 193, 195, 197, 198, 200, 205, 207, 208, 209, 213, 216, 217, 218, 220, 221, 223, 225, 240, 241, 242, 245, 258, 259, 260, 261, 262, 264, 268, 270, 271, 275, 277, 279, 282, 288, 294, 302, 311, 318, 319, 322, 328, 332, 338, 346, 347, 349, 351, 352, 357, 359, 361, 363, 365, 368, 370, 371, 372, 376, 381, 383, 384, 388, 400, 404, 407, 410, 412, 413, 414, 430, 432, 438, 439, 443, 446, 447, 448, 449, 450, 451, 464, 465, 477, 478, 481, 482, 486, 487, 490, 492, 493, 499, 501, 502, 504, 505, 508, 509, 525, 532, 536, 541, 542, 543, 547, 552, 556, 562, 565, 567, 584, 588, 591, 596, 599, 602, 610, 612, 613, 633, 638, 649, 650, 654, 660, 663, 668, 672, 678, 686, 692, 696, 697, 699, 700, 707, 709, 711, 716, 734, 736, 741, 746, 759, 765, 784, 797, 800, 802, 803, 815, 816, 818, 834, 838, 840, 850, 851, 853, 859, 865, 921, 927, 941, 945, 953, 957, 966, 970, 1006, 1015, 1023, 1026, 1040, 1056, 1071, 1098, 1103, 1105, 1107, 1109, 1114, 1116, 1136, 1137, 1154, 1156, 1157, 1166, 1170, 1179, 1201, 1202, 1207, 1213, 1236, 1237, 1238, 1239, 1240, 1261, 1265, 1269, 1286, 1304, 1306, 1325, 1342, 1344, 1356, 1358, 1362, 1367, 1370, 1374, 1383, 1389, 1390, 1391, 1399, 1400, 1403, 1407, 1409, 1416, 1417, 1418, 1423, 1424, 1428, 1429, 1434, 1439, 1445, 1447, 1450, 1452, 1464, 1468, 1469, 1470, 1471, 1474, 1481, 1492, 1493, 1494, 1498, 1501, 1502, 1504, 1505, 1526, 1532, 1534, 1540, 1541, 1542, 1544, 1547, 1552, 1554, 1556, 1558, 1564, 1565, 1570, 1573, 1574, 1575, 1578, 1585, 1590, 1593, 1594, 1596, 1602, 1608, 1612, 1630, 1631, 1648, 1655, 1658, 1659, 1663, 1665, 1669, 1670, 1674, 1676, 1677, 1678, 1682, 1686, 1689, 1691, 1692, 1698, 1700, 1702, 1703, 1704, 1705, 1707, 1708, 1713, 1716, 1718, 1723, 1733, 1738, 1745, 1749, 1752, 1753, 1754, 1755, 1758, 1765, 1767, 1768, 1770, 1772, 1776, 1778, 1782, 1784, 1792, 1793, 1798, 1806, 1808, 1809, 1815, 1819, 1834, 1835, 1837, 1839, 1840, 1848, 1852, 1856, 1865, 1868, 1873, 1874, 1877, 1878, 1886, 1888, 1895, 1901, 1906, 1907, 1909, 1910, 1914, 1919, 1920, 1925, 1926, 1927, 1928, 1929, 1942, 1944, 1948, 1951, 1954, 1963, 1964, 1971, 1980, 1993, 1996, 2004, 2009, 2016, 2025, 2048, 2055, 2056, 2059, 2065, 2066, 2067, 2075, 2081, 2086, 2087, 2089, 2092, 2110, 2111, 2112, 2123, 2128, 2130, 2178, 2183, 2204, 2208, 2230, 2272, 2307, 2318, 2325, 2336, 2386, 2391, 2395, 2396, 2398, 2400, 2404, 2405, 2408, 2410, 2413, 2423, 2430, 2450, 2453, 2493, 2512, 2520, 2528, 2550, 2566, 2574, 2590, 2594, 2598, 2609, 2611, 2628, 2635, 2638, 2639, 2659, 2660, 2661, 2663, 2665, 2667, 2669, 2673, 2678, 2679, 2682, 2690, 2695, 2696, 2703, 2712, 2714, 2784, 2836, 2890, 2902, 2920, 2926, 2979, 2983, 3020, 3046, 3059, 3075, 3106, 3120, 3149, 3220, 3226, 3336, 3411, 3436, 3498, 3554, 3600, 3660, 3664, 3837, 3922, 4014, 4025, 4041, 4049, 4233, 4235, 4274, 4408, 4493, 4516, 4600, 4811, 4826, 4859, 5172, 5214, 5234, 5253, 5260, 5261, 5293, 5333, 5405, 5461, 5501, 5507, 5535, 2704, 2713, 2716, 2733, 2737, 2749, 2757, 2781, 2792, 2800, 2808, 2816, 2826, 2834, 2845, 2854, 2857, 2861, 2880, 2886, 2909, 2913, 2937, 2939, 2944, 2955, 2957, 2965, 2967, 2971, 2973, 2975, 2980, 2985, 2999, 3016, 3028, 3030, 3036, 3042, 3051, 3053, 3055, 3060, 3062, 3066, 3079, 3088, 3105, 3115, 3129, 3160, 3166, 3186, 3204, 3214, 3228, 3230, 3244, 3258, 3266, 3277, 3293, 3299, 3315, 3327, 3333, 3340, 3350, 3352, 3355, 3359, 3361, 3372, 3374, 3398, 3417, 3424, 3434, 3437, 3441, 3449, 3467, 3469, 3475, 3486, 3488, 3490, 3499, 3501, 3505, 3516, 3518, 3526, 3528, 3538, 3540, 3544, 3555, 3586, 3588, 3597, 3606, 3609, 3615, 3625, 3631, 3640, 3648, 3673, 3683, 3697, 3717, 3729, 3741, 3743, 3747, 3749, 3757, 3778, 3798, 3824, 3828, 3834, 3847, 3852, 3879, 3885, 3887, 3893, 3928, 3964, 3970, 3974, 4002, 4006, 4008, 4012, 4034, 4038, 4043, 4059, 4069, 4087, 4114, 4124, 4132, 4153, 4161, 4178, 4210, 4234, 4237, 4239, 4241, 4257, 4284, 4288, 4294, 4315, 4321, 4330, 4343, 4447, 4461, 4475, 4485, 4487, 4491, 4535, 4564, 4574, 4605, 4662, 4672, 4674, 4676, 4725, 4744, 4760, 4774, 4803, 4848, 4865, 4941, 4949, 4951, 5005, 5042, 5049, 5075, 5089, 5128, 5145, 5156, 5205, 5270, 5302, 5320, 5348, 5368, 5379, 5412, 5414, 5422, 5432, 5460, 5463, 5473, 5480, 5486, 5488, 5496, 5502, 5529, 5533]
new_data_dir = "E:/data/ASE2019/"
db = database.connectdb()

def proj_lib_usage():


    # versions = set()
    # for id in projs_3_month:
    #     sql = "SELECT distinct group_str,name_str,version FROM `usage` WHERE project_id = " + str(id)
    #     query_result = database.querydb(db, sql)
    #     versions = versions.union(set(query_result))
    # print(len(versions)) #24205
    # write_json(new_data_dir + "all_versions.txt", list(versions))

    # json_data = read_json(new_data_dir + "all_versions.txt")
    # print(len(json_data))
    # solved = []
    # unsolved = []
    # count = 0
    # for entry in json_data:
    #     print(entry)
    #     sql = "SELECT * FROM library_versions WHERE group_str = '" + entry[0] + "' and name_str = '" + entry[1] + "' and version = '" + entry[2] + "'"
    #     query_result = database.querydb(db, sql)
    #     if len(query_result) > 0:
    #         count += 1
    #         solved.append(entry)
    #     else:
    #         unsolved.append(entry)
    # print(count) #16384
    # print(len(unsolved)) # 7821
    # write_json(new_data_dir + "solved_versions.txt", solved)
    # write_json(new_data_dir + "unsolved_versions.txt", unsolved)

    unsolved = read_json(new_data_dir + "unsolved_versions.txt")
    print(len(unsolved))
    count = 0
    for entry in unsolved:
        version = entry[2]
        if version.endswith("SNAPSHOT"):
            count += 1
    print(count)

def get_libraries():
    # result = set()
    # solved = read_json(new_data_dir + "solved_versions.txt")
    # unsolved = read_json(new_data_dir + "unsolved_versions.txt")
    # for entry in solved:
    #     temp = (entry[0],entry[1])
    #     result.add(temp)
    # # for entry in unsolved:
    # #     temp = (entry[0],entry[1])
    # #     result.add(temp)
    # print(len(result)) #7364
    # write_json(new_data_dir + "libraries.txt", list(result))

    ids = set()
    for id in projs_3_month:
        sql = "SELECT distinct library_id FROM project_lib_usage WHERE project_id = " + str(id)
        query_result = database.querydb(db, sql)
        for entry in query_result:
            ids.add(entry[0])
    print(len(ids))
    write_json(new_data_dir + "library_ids.txt", list(ids)) # 7229

def get_releases():
    # data = read_json(new_data_dir + "libraries.txt")
    # print(len(data))
    # total = 0
    # for entry in data:
    #     sql = "SELECT * FROM library_versions WHERE group_str = '" + entry[0] + "' and name_str = '" + entry[1] + "'"
    #     query_result = database.querydb(db, sql)
    #     total += len(query_result)
    # print(total)

    # versions = []
    # for id in projs_3_month:
    #     sql = "SELECT distinct version_id FROM project_lib_usage WHERE project_id = " + str(id)
    #     query_result = database.querydb(db, sql)
    #     for entry in query_result:
    #         versions.append(entry[0])
    # print(len(versions))
    # lib_repo = set()
    # for version_id in versions:
    #     sql = "SELECT library_id,repository FROM library_versions WHERE id = " + str(version_id)
    #     lib_result = database.querydb(db, sql)
    #     lib_repo.add((lib_result[0][0], lib_result[0][1]))
    # print(len(lib_repo))
    # write_json(new_data_dir + "lib_repo.txt", list(lib_repo))

    data = read_json(new_data_dir + "lib_repo.txt")
    count = 0
    for entry in data:
        print(entry)
        sql = "SELECT count(*) FROM library_versions WHERE repository = '" + entry[1] + "' and library_id = " + str(entry[0])
        release_result = database.querydb(db, sql)
        count += release_result[0][0]
    print(count) # 288312

proj_lib_usage()
# get_libraries()
# get_releases()