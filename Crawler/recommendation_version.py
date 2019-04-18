import os
import database
from file_util import read_json, write_json


def get_project_commit_pair():
    json_data = read_json("E:/data/recommendation/Diff API calls/cg_result-Feb2.json")
    libs = set()
    for key in json_data.keys():
        value = json_data[key]
        for jar_name in value.keys():
            if jar_name != "url":
                libs.add(jar_name)
    print(libs)

    db = database.connectdb()
    result = {}
    for lib in libs:
        print(lib)
        sql = "SELECT version_id FROM version_types WHERE jar_package_url = '" + lib + "'"
        type_info = database.querydb(db, sql)
        version_id = type_info[0][0]
        sql = "SELECT group_str,name_str,version FROM library_versions WHERE id = " + str(version_id)
        version_info = database.querydb(db, sql)
        groupId = version_info[0][0]
        artifactId = version_info[0][1]
        version = version_info[0][2]
        sql = "SELECT id,project_id, curr_version,prev_commit,curr_commit,type,classifier FROM lib_update WHERE group_str = '" + groupId + "' and name_str = '" + artifactId + "' and prev_version = '" + version + "'"
        update_info = database.querydb(db, sql)
        update_list = []
        for entry in update_info:
            data = list(entry)
            data.append(groupId)
            data.append(artifactId)
            data.append(version)
            update_list.append(data)
        result[lib] = update_list
    write_json("E:/data/recommendation/update_commits.txt", result)

def filter_diff():
    json_data = read_json("E:/data/recommendation/update_commits.txt")
    prefixs = read_json("E:/data/recommendation/100libPackgePrefix.json")
    thirty_diff = read_json("E:/data/recommendation/Diff API calls/30diff.json")
    sixty_diff = read_json("E:/data/recommendation/Diff API calls/60diff.json")
    ninety_diff = read_json("E:/data/recommendation/Diff API calls/90diff.json")
    result = {}
    for lib in json_data:
        update_list = json_data[lib]
        groupId = update_list[0][7]
        artifactId = update_list[0][8]
        prefix = prefixs[groupId + "__fdse__" + artifactId]
        for entry in update_list:
            project_id = entry[1]
            prev_commit = entry[3]
            curr_commit = entry[4]
            key = str(project_id) + "__fdse__" + prev_commit + "__fdse__" + curr_commit
            print(key)
            change_content = None
            if key in thirty_diff:
                change_content = thirty_diff[key]
            elif key in sixty_diff:
                change_content = sixty_diff[key]
            elif key in ninety_diff:
                change_content = ninety_diff[key]
            if change_content is not None:
                new_content = {}
                for operation in change_content:
                    api_list = change_content[operation]
                    new_list = []
                    for api in api_list:
                        if api.startswith(prefix):
                            new_list.append(api)
                    new_content[operation] = new_list
                result[key] = new_content
    write_json("E:/data/recommendation/filtered_diff.txt", result)

projects = [2, 4, 5, 6, 7, 8, 9, 10, 15, 16, 17, 18, 20, 21, 22, 23, 24, 28, 30, 31, 32, 34, 35, 37, 38, 39, 40, 41, 42, 43, 49, 50, 52, 53, 56, 60, 62, 63, 66, 68, 69, 70, 73, 78, 79, 80, 83, 84, 85, 86, 87, 93, 95, 96, 99, 102, 108, 111, 113, 115, 116, 118, 119, 123, 125, 127, 128, 130, 131, 132, 133, 135, 136, 138, 142, 143, 145, 147, 148, 149, 151, 152, 155, 157, 160, 163, 164, 165, 166, 169, 171, 172, 173, 174, 175, 176, 177, 178, 180, 184, 186, 188, 189, 190, 192, 193, 195, 197, 198, 200, 205, 207, 208, 209, 213, 216, 217, 218, 220, 221, 223, 225, 234, 235, 236, 240, 242, 245, 258, 259, 260, 261, 262, 264, 268, 269, 270, 271, 275, 277, 279, 282, 284, 288, 293, 294, 295, 297, 302, 305, 308, 310, 311, 318, 319, 322, 323, 328, 332, 338, 341, 342, 343, 346, 347, 349, 350, 351, 352, 357, 358, 359, 360, 361, 363, 365, 368, 369, 370, 371, 372, 376, 380, 381, 383, 384, 386, 388, 389, 395, 400, 404, 407, 410, 412, 413, 414, 421, 430, 432, 434, 438, 439, 443, 446, 447, 448, 449, 450, 451, 452, 454, 460, 464, 465, 468, 477, 478, 481, 482, 486, 487, 490, 492, 493, 499, 501, 502, 504, 505, 506, 508, 521, 525, 526, 532, 534, 536, 538, 541, 542, 543, 547, 552, 556, 562, 565, 566, 567, 572, 584, 588, 591, 596, 598, 599, 602, 610, 612, 613, 623, 633, 638, 649, 650, 654, 660, 663, 666, 668, 672, 678, 681, 686, 692, 696, 698, 699, 700, 707, 709, 711, 716, 734, 736, 741, 746, 751, 759, 765, 771, 784, 797, 800, 802, 803, 810, 815, 816, 818, 834, 836, 838, 840, 850, 851, 853, 860, 865, 920, 921, 927, 937, 941, 953, 956, 957, 964, 966, 970, 988, 1006, 1011, 1015, 1022, 1023, 1026, 1028, 1040, 1047, 1056, 1071, 1098, 1103, 1105, 1107, 1109, 1114, 1116, 1120, 1136, 1137, 1139, 1147, 1148, 1154, 1156, 1157, 1170, 1179, 1198, 1201, 1202, 1207, 1213, 1226, 1236, 1237, 1238, 1239, 1240, 1261, 1265, 1269, 1286, 1304, 1306, 1317, 1325, 1342, 1344, 1356, 1358, 1362, 1367, 1370, 1374, 1383, 1385, 1386, 1387, 1388, 1389, 1390, 1391, 1392, 1396, 1399, 1400, 1401, 1403, 1404, 1406, 1407, 1409, 1412, 1414, 1416, 1417, 1418, 1419, 1421, 1423, 1427, 1428, 1430, 1434, 1435, 1439, 1441, 1442, 1444, 1447, 1450, 1452, 1458, 1460, 1461, 1462, 1464, 1466, 1467, 1468, 1469, 1470, 1471, 1472, 1474, 1476, 1481, 1484, 1489, 1490, 1491, 1492, 1493, 1494, 1498, 1501, 1502, 1504, 1505, 1506, 1508, 1510, 1511, 1513, 1515, 1516, 1517, 1520, 1521, 1522, 1526, 1527, 1528, 1529, 1530, 1532, 1534, 1538, 1540, 1541, 1542, 1544, 1546, 1547, 1548, 1552, 1554, 1555, 1556, 1557, 1558, 1565, 1570, 1571, 1573, 1574, 1575, 1578, 1579, 1581, 1582, 1585, 1588, 1590, 1592, 1593, 1594, 1596, 1598, 1599, 1602, 1604, 1608, 1610, 1612, 1618, 1619, 1623, 1627, 1630, 1631, 1633, 1634, 1635, 1639, 1640, 1641, 1653, 1655, 1658, 1659, 1663, 1665, 1669, 1670, 1673, 1674, 1676, 1677, 1678, 1679, 1682, 1686, 1689, 1691, 1692, 1693, 1697, 1698, 1700, 1701, 1702, 1703, 1704, 1705, 1706, 1707, 1708, 1710, 1711, 1713, 1716, 1718, 1722, 1723, 1727, 1730, 1733, 1738, 1749, 1752, 1753, 1754, 1755, 1757, 1758, 1764, 1765, 1767, 1768, 1770, 1772, 1773, 1776, 1778, 1779, 1780, 1784, 1786, 1787, 1792, 1793, 1798, 1799, 1800, 1801, 1806, 1807, 1808, 1809, 1814, 1815, 1819, 1825, 1826, 1834, 1835, 1837, 1839, 1840, 1843, 1852, 1856, 1858, 1860, 1865, 1866, 1867, 1868, 1873, 1874, 1877, 1878, 1879, 1886, 1888, 1893, 1895, 1901, 1903, 1906, 1907, 1909, 1910, 1914, 1919, 1920, 1923, 1925, 1926, 1928, 1929, 1931, 1934, 1939, 1942, 1944, 1948, 1951, 1953, 1954, 1959, 1963, 1964, 1965, 1971, 1980, 1981, 1982, 1992, 1993, 1996, 2004, 2009, 2014, 2016, 2018, 2025, 2028, 2030, 2041, 2048, 2055, 2056, 2057, 2059, 2061, 2064, 2065, 2066, 2067, 2075, 2077, 2081, 2086, 2087, 2089, 2092, 2100, 2110, 2111, 2112, 2116, 2123, 2128, 2130, 2136, 2137, 2172, 2178, 2183, 2200, 2201, 2204, 2208, 2209, 2228, 2230, 2247, 2272, 2274, 2304, 2307, 2318, 2324, 2325, 2336, 2345, 2353, 2366, 2386, 2387, 2391, 2395, 2396, 2398, 2400, 2404, 2405, 2408, 2410, 2413, 2423, 2430, 2433, 2434, 2448, 2450, 2453, 2470, 2471, 2489, 2493, 2512, 2520, 2528, 2544, 2550, 2558, 2566, 2574, 2576, 2580, 2590, 2594, 2598, 2606, 2607, 2608, 2609, 2611, 2628, 2633, 2635, 2638, 2639, 2659, 2660, 2661, 2663, 2665, 2667, 2669, 2673, 2678, 2679, 2682, 2690, 2695, 2696, 2703, 2712, 2713, 2714, 2716, 2721, 2723, 2725, 2731, 2733, 2735, 2737, 2747, 2749, 2757, 2761, 2763, 2769, 2781, 2784, 2785, 2792, 2794, 2796, 2798, 2800, 2802, 2808, 2814, 2816, 2822, 2826, 2834, 2836, 2841, 2843, 2845, 2847, 2852, 2854, 2855, 2857, 2861, 2867, 2871, 2880, 2881, 2883, 2884, 2886, 2890, 2893, 2895, 2896, 2900, 2902, 2909, 2913, 2917, 2918, 2920, 2921, 2923, 2926, 2928, 2929, 2933, 2937, 2939, 2942, 2944, 2946, 2951, 2953, 2955, 2957, 2959, 2965, 2967, 2969, 2971, 2973, 2975, 2979, 2980, 2982, 2983, 2985, 2987, 2989, 2993, 2995, 2997, 2999, 3005, 3007, 3016, 3020, 3024, 3028, 3030, 3036, 3038, 3042, 3044, 3046, 3051, 3053, 3059, 3060, 3062, 3066, 3068, 3070, 3075, 3079, 3081, 3082, 3086, 3088, 3103, 3105, 3106, 3108, 3110, 3115, 3119, 3120, 3124, 3126, 3128, 3129, 3131, 3133, 3146, 3149, 3155, 3158, 3160, 3162, 3168, 3176, 3182, 3186, 3193, 3197, 3202, 3204, 3212, 3214, 3220, 3221, 3225, 3226, 3228, 3230, 3232, 3234, 3236, 3238, 3242, 3244, 3248, 3258, 3266, 3272, 3277, 3281, 3283, 3291, 3293, 3299, 3301, 3303, 3305, 3307, 3315, 3321, 3323, 3325, 3327, 3329, 3333, 3336, 3340, 3344, 3350, 3352, 3355, 3359, 3361, 3363, 3365, 3367, 3369, 3370, 3372, 3374, 3380, 3388, 3398, 3404, 3406, 3411, 3417, 3422, 3424, 3434, 3436, 3437, 3439, 3441, 3445, 3449, 3461, 3465, 3467, 3469, 3475, 3483, 3486, 3488, 3490, 3496, 3498, 3499, 3501, 3505, 3507, 3512, 3516, 3518, 3522, 3524, 3526, 3528, 3533, 3537, 3538, 3544, 3550, 3554, 3555, 3568, 3574, 3576, 3584, 3586, 3588, 3590, 3594, 3597, 3599, 3600, 3606, 3607, 3609, 3615, 3625, 3627, 3629, 3631, 3637, 3640, 3642, 3648, 3657, 3660, 3664, 3671, 3673, 3683, 3687, 3693, 3697, 3709, 3717, 3721, 3729, 3731, 3733, 3737, 3739, 3741, 3743, 3747, 3755, 3757, 3778, 3782, 3784, 3788, 3796, 3798, 3814, 3822, 3828, 3834, 3837, 3847, 3852, 3879, 3887, 3889, 3893, 3903, 3909, 3915, 3922, 3924, 3928, 3932, 3934, 3936, 3941, 3945, 3955, 3964, 3966, 3970, 3974, 4002, 4006, 4008, 4012, 4014, 4015, 4021, 4025, 4030, 4034, 4038, 4041, 4043, 4049, 4054, 4069, 4075, 4087, 4104, 4114, 4124, 4126, 4132, 4140, 4151, 4153, 4161, 4165, 4174, 4178, 4191, 4202, 4210, 4212, 4216, 4227, 4231, 4233, 4234, 4235, 4237, 4239, 4241, 4247, 4255, 4257, 4261, 4267, 4274, 4278, 4284, 4288, 4294, 4306, 4315, 4321, 4323, 4330, 4334, 4343, 4352, 4380, 4388, 4408, 4410, 4414, 4416, 4423, 4447, 4461, 4469, 4473, 4475, 4481, 4485, 4487, 4491, 4493, 4500, 4512, 4514, 4516, 4518, 4524, 4535, 4564, 4574, 4594, 4598, 4600, 4605, 4618, 4638, 4662, 4672, 4674, 4676, 4678, 4695, 4725, 4742, 4744, 4746, 4748, 4754, 4760, 4770, 4774, 4795, 4803, 4811, 4826, 4832, 4846, 4848, 4859, 4865, 4873, 4879, 4883, 4933, 4939, 4941, 4949, 4951, 4957, 4973, 4983, 5005, 5017, 5027, 5033, 5042, 5075, 5079, 5087, 5089, 5096, 5128, 5145, 5153, 5156, 5163, 5165, 5172, 5185, 5214, 5233, 5234, 5236, 5245, 5253, 5260, 5261, 5270, 5273, 5293, 5295, 5302, 5320, 5328, 5330, 5333, 5338, 5348, 5368, 5379, 5399, 5401, 5405, 5408, 5412, 5414, 5432, 5434, 5447, 5454, 5456, 5460, 5461, 5463, 5473, 5475, 5479, 5480, 5486, 5488, 5496, 5501, 5502, 5504, 5507, 5525, 5529, 5533, 5535, 5538]
def get_multiversion_libs():
    db = database.connectdb()
    libs = set()
    projs = set()
    count = 0
    for id in projects:
        print(id)
        sql = "SELECT DISTINCT group_str,name_str FROM `usage` WHERE project_id = " + str(id)
        usage_info = database.querydb(db, sql)
        num = 0
        have = False
        for entry in usage_info:
            groupId = entry[0]
            artifactId = entry[1]
            sql = "SELECT COUNT(DISTINCT(version)) FROM `usage` WHERE project_id = " + str(id) + " and group_str = '"+groupId+"' and name_str = '"+artifactId+"'"
            result = database.querydb(db, sql)
            if result[0][0] > 1:
                have = True
                break
        if have:
            projs.add(id)
            count += 1
    print(count)
    write_json("E:/data/mv_libs_total.txt", list(projs))
    #             libs.add(groupId + "__fdse__" + artifactId)
    # write_json("E:/data/mv_libs.txt", list(libs))

def get_multiversion_libs_exclude_top100():
    top100 = read_json("E:/data/top100.txt")
    print(len(top100))
    top_set = set()
    for entry in top100:
        # print(entry[0])
        top_set.add(entry[0])
    print(top_set)
    data = read_json("E:/data/mv_libs.txt")
    new_data = set()
    count = 0
    for entry in data:
        if entry not in top_set:
            new_data.add(entry)
        else:
            count += 1
    print(count)
    write_json("E:/data/mv_libs_exclude_top100.txt", list(new_data))

def get_build_success_proj():
    total = set()
    dir = "E:/data/dependency_tree/parsed"
    files = os.listdir(dir)
    for file in files:
        content = read_json(os.path.join(dir, file))
        length1 = len(content["unparsed"])
        length2 = len(content["parsed"])
        if length1 + length2 > 0:
            project_id = int(file.split("-")[0])
            total.add(project_id)
    print(len(total))
    write_json("E:/data/multiversion/build_success.txt", list(total))


def get_all_verisons_for_mv():
    db = database.connectdb()
    data = read_json("E:/data/multiversion/mv_libs_exclude_top100.txt")
    result = {}
    for entry in data:
        print("+++++++++++++++++++++ " + entry)
        groupId = entry.split("__fdse__")[0]
        artifactId = entry.split("__fdse__")[1]
        versions = set()
        sql = "SELECT id FROM library WHERE group_str = '"+groupId+"' and name_str = '"+artifactId+"'"
        libray_id_info = database.querydb(db, sql)
        if len(libray_id_info) <= 0:
            print("no library id : " + entry)
            result[entry] = list(versions)
            continue
        library_id = libray_id_info[0][0]
        sql = "SELECT DISTINCT version_id FROM `project_lib_usage` WHERE library_id = " + str(library_id)
        version_info = database.querydb(db, sql)
        for info in version_info:
            version_id = info[0]
            sql = "SELECT version FROM library_versions WHERE id = " + str(version_id)
            query_result = database.querydb(db, sql)
            version = query_result[0][0]
            versions.add(version)
        result[entry] = list(versions)
        print(versions)
    write_json("E:/data/multiversion/mv_libs_to_crawl.txt", result)

def snapshot_filter():
    json_data = read_json("E:/data/multiversion/mv_libs_to_crawl.txt")
    for key in json_data.keys():
        old_list = json_data[key]
        if len(old_list) == 0:
            print("++++++++++++++++++" + key)
    #     for version in old_list:
    #         if version.endswith("-SNAPSHOT"):
    #             old_list.remove(version)
    # write_json("E:/data/multiversion/mv_libs_exclude_snapshot.txt", json_data)

def add_proj_type():
    db = database.connectdb()
    json_data = read_json("E:/data/200_plus.txt")
    for entry in json_data:
        project_id = entry["id"]
        sql = "SELECT type FROM project WHERE id = " + str(project_id)
        query_result = database.querydb(db, sql)
        _type = query_result[0][0]
        entry["type"] = _type
    write_json("E:/data/200_plus_with_type.txt", json_data)


def get_multiversion_info():
    db = database.connectdb()
    final = {}
    for id in projects:
        print(id)
        proj_obj = {}
        sql = "SELECT DISTINCT group_str,name_str FROM `usage` WHERE project_id = " + str(id)
        usage_info = database.querydb(db, sql)
        for entry in usage_info:
            groupId = entry[0]
            artifactId = entry[1]
            sql = "SELECT DISTINCT version,module FROM `usage` WHERE project_id = " + str(id) + " and group_str = '"+groupId+"' and name_str = '"+artifactId+"'"
            result = database.querydb(db, sql)
            if len(result) > 1:
                version_list = []
                for entry in result:
                    version = entry[0]
                    _module = entry[1]
                    version_list.append(_module + "__fdse__" + version)
                proj_obj[groupId + "__fdse__" + artifactId] = version_list
        if len(proj_obj) > 0:
            final[str(id)] = proj_obj
            # break
    write_json("E:/data/multiversion/multiversion_info.txt", final)

def mv_dict_to_list():
    json_data = read_json("mv_libs_exclude_snapshot.txt")
    new_list = []
    for key in json_data.keys():
        versions = json_data[key]
        obj = {}
        obj["lib"] = key
        obj["versions"] = versions
        new_list.append(obj)
    write_json("mv_libs.txt", new_list)

def get_multiversion_projs():
    print(len(projects))
    db = database.connectdb()
    projs = set()
    count = 0
    for id in projects:
        print(id)
        sql = "SELECT DISTINCT library_id FROM `project_lib_usage` WHERE project_id = " + str(id)
        usage_info = database.querydb(db, sql)
        num = 0
        have = False
        for entry in usage_info:
            library_id = entry[0]
            sql = "SELECT COUNT(DISTINCT(version_id)) FROM `project_lib_usage` WHERE project_id = " + str(id) + " and library_id = " + str(library_id)
            result = database.querydb(db, sql)
            if result[0][0] > 1:
                have = True
                projs.add(id)
                print(id)
                break
        if have:
            count += 1
    print(count)
    #             libs.add(groupId + "__fdse__" + artifactId)
    write_json("E:/data/mv_projs.txt", list(projs))

def compare():
    json_data = read_json("E:/data/multiversion/multiversion_info.txt")
    longer = list(json_data.keys())
    shorter = read_json("E:/data/multiversion/mv_libs_total.txt")
    # print(shorter)
    final = []
    for id_str in longer:
        id = int(id_str)
        # print(id_str)
        if not id in shorter:
            final.append(id)
    print(final)
    print(len(final))

def get_multiversion_info_in_usage():
    # db = database.connectdb()
    # final = {}
    # for id in projects:
    #     print(id)
    #     proj_obj = {}
    #     sql = "SELECT DISTINCT library_id FROM `project_lib_usage` WHERE project_id = " + str(id)
    #     usage_info = database.querydb(db, sql)
    #     for entry in usage_info:
    #         library_id = entry[0]
    #         sql = "SELECT * FROM library WHERE id = " + str(library_id)
    #         library_info = database.querydb(db, sql)
    #         groupId = library_info[0][1]
    #         artifactId = library_info[0][2]
    #         sql = "SELECT DISTINCT version FROM `project_lib_usage` WHERE project_id = " + str(id) + " and library_id = " + str(library_id)
    #         result = database.querydb(db, sql)
    #         if len(result) > 1:
    #             version_list = []
    #             for entry in result:
    #                 version = entry[0]
    #                 sql = "SELECT DISTINCT module FROM `project_lib_usage` WHERE project_id = " + str(id) + " and library_id = " + str(library_id) + " and version = '" + version + "'"
    #                 module_info = database.querydb(db, sql)
    #                 for m in module_info:
    #                     _module = m[0]
    #                     version_list.append(_module + "__fdse__" + version)
    #             proj_obj[groupId + "__fdse__" + artifactId] = version_list
    #     if len(proj_obj) > 0:
    #         final[str(id)] = proj_obj
    #         # break
    # write_json("E:/data/multiversion/multiversion_info.txt", final)

    db = database.connectdb()
    final = {}
    for id in projects:
        print(id)
        proj_obj = {}
        sql = "SELECT DISTINCT library_id FROM `project_lib_usage` WHERE project_id = " + str(id)
        usage_info = database.querydb(db, sql)
        for entry in usage_info:
            library_id = entry[0]
            sql = "SELECT DISTINCT version_id FROM `project_lib_usage` WHERE project_id = " + str(
                id) + " and library_id = " + str(library_id)
            result = database.querydb(db, sql)
            version_list = []
            if len(result) > 1:
                sql = "SELECT * FROM library WHERE id = " + str(library_id)
                library_info = database.querydb(db, sql)
                groupId = library_info[0][1]
                artifactId = library_info[0][2]
                lib_obj = {}
                for entry in result:
                    version_id = entry[0]
                    sql = "SELECT version FROM `library_versions` WHERE id = " + str(version_id)
                    version_info = database.querydb(db, sql)
                    version = version_info[0][0]
                    sql = "SELECT version_type_id, module FROM `project_lib_usage` WHERE project_id = " + str(
                        id) + " and version_id = " + str(version_id)
                    module_info = database.querydb(db, sql)
                    for m in module_info:
                        version_type_id = m[0]
                        _module = m[1]
                        sql = "SELECT type, classifier FROM `version_types` WHERE type_id = " + str(version_type_id)
                        type_info = database.querydb(db, sql)
                        type_ = type_info[0][0]
                        classifier = type_info[0][1]
                        key = groupId + "__fdse__" + artifactId + "__fdse__" + type_
                        if classifier is not None:
                            key += "__fdse__" + classifier
                        if key in lib_obj:
                            lib_obj[key].add(_module + "__fdse__" + version)
                        else:
                            lib_obj[key] = set()
                            lib_obj[key].add(_module + "__fdse__" + version)
                for lib_key in lib_obj:
                    if len(lib_obj[lib_key]) > 1:
                        proj_obj[lib_key] = list(lib_obj[lib_key])
                    else:
                        print(lib_key + " : " + str(lib_obj[lib_key]))
            # proj_obj[groupId + "__fdse__" + artifactId] = version_list
        if len(proj_obj) > 0:
            final[str(id)] = proj_obj
            # break
    write_json("E:/data/multiversion/multiversion_info.txt", final)

def parse_mv_info():
    db = database.connectdb()
    json_data = read_json("E:/data/multiversion/multiversion_info.txt")
    final = {}
    for project_id in json_data.keys():
        sql = "SELECT url FROM project WHERE id = " + project_id
        query_result = database.querydb(db, sql)
        url = query_result[0][0]
        name = url.replace("https://github.com/", "").replace("/", "__fdse__")
        proj_data = json_data[project_id]
        proj_ = {}
        for lib in proj_data.keys():
            version_list = proj_data[lib]
            for entry in version_list:
                _module = entry.split("__fdse__")[0]
                version = entry.split("__fdse__")[1]
                if _module in proj_:
                    proj_[_module].append(lib + "__fdse__" + version)
                else:
                    new_list = [lib + "__fdse__" + version]
                    proj_[_module] = new_list
        final[project_id] = proj_
    write_json("E:/data/multiversion/mv_info_parsed.txt", final)

def remove_gradle_proj():
    # proj_data = read_json("E:/data/200_plus_with_type.txt")
    # proj_dict = {}
    # for entry in proj_data:
    #     id = entry["id"]
    #     _type = entry["type"]
    #     proj_dict[str(id)] = _type
    #
    # json_data = read_json("E:/data/multiversion/mv_info_parsed.txt")
    # print(len(json_data))
    # new_data = {}
    # for id in json_data:
    #     _type = proj_dict[id]
    #     if _type == "maven":
    #         new_data[id] = json_data[id]
    # print(len(new_data))
    # write_json("E:/data/multiversion/mv_info_maven.txt", new_data)
    data = read_json("E:/data/multiversion/mv_info_maven.txt")
    print(len(data))


# get_project_commit_pair()
# filter_diff()
# get_multiversion_libs()
# data = read_json("E:/data/mv_libs_exclude_top100.txt")
# print(len(data))
# get_multiversion_libs_exclude_top100()
# get_build_success_proj()
# get_all_verisons_for_mv()
# get_multiversion_info()
# get_build_success_proj()
# snapshot_filter()
# mv_dict_to_list()
# get_multiversion_projs()
# data = read_json("E:/data/multiversion/mv_projs.txt")
# print(len(data))
# add_proj_type()
# get_multiversion_libs()
# compare()
# get_multiversion_info_in_usage()
# data = read_json("E:/data/multiversion/multiversion_info_4.9.txt")
# print(len(data))
# parse_mv_info()
remove_gradle_proj()