import os
import database
from draw import draw_bar, draw_barh, draw_line
from file_util import read_json, write_json
from statics_3_new import data_group

db = database.connectdb()

def s_5_1_1():
    # usage_count.sort()
    # write_json("D:/data/data_copy/figure/datas/s_3_1_1.txt", usage_count)
    # keys = ['']*25
    # values = [0]*25
    # keys[0] = '0'
    # values[0] = 1329 - 1281
    # for i in range(0,20):
    #     start = i*5
    #     end = i*5 + 5
    #     keys[i+1] = str(start) + "-" + str(end)
    # keys[21] = '100-150'
    # keys[22] = '150-200'
    # keys[23] = '200-250'
    # keys[24] = '>250'
    # usage_count = read_json("D:/data/data_copy/figure/datas/s_3_1_1.txt")
    # print(len(usage_count))
    # count = 0
    # for num in usage_count:
    #     if num > 250:
    #         values[24] += 1
    #     elif num > 200 and num <= 250:
    #         values[23] += 1
    #     elif num > 150 and num <= 200:
    #         values[22] += 1
    #     elif num > 100 and num <= 150:
    #         values[21] += 1
    #     else:
    #         index = num // 5 + 1
    #         if num % 5 == 0:
    #             index -= 1
    #         values[index] += 1
    #
    # draw_bar(keys, values, "The Number of Library Versions Used in a Project (#)", "The Number of Projects (#)")

    usage_count = read_json("D:/data/data_copy/figure/datas/Fig5-A-Data.json")
    usage_count = list(usage_count.values())
    print(usage_count)
    print(len(usage_count))
    data_group(usage_count, 2, "The Number of Severe Bugs in a Library Version (#)", "The Number of Library Versions (#)", False)

def s_5_1_2():
    # usage_count = read_json("D:/data/data_copy/figure/datas/Fig5-B-Data2.json")
    # usage_count = list(usage_count.values())
    # print(usage_count)
    # print(len(usage_count))
    # data_group(usage_count, 2, "The Number of Projects Using a Library Version (#)", "The Number of Library Versions (#)", False)
    keys = [''] * 19
    values = [0] * 19
    for i in range(0, 10):
        start = i * 2
        end = i * 2 + 2
        keys[i] = str(start) + "-" + str(end)
    keys[10] = '20-30'
    keys[11] = '30-40'
    keys[12] = '40-50'
    keys[13] = '50-60'
    keys[14] = '60-70'
    keys[15] = '70-80'
    keys[16] = '80-90'
    keys[17] = '90-100'
    keys[18] = '>100'
    usage_count = read_json("D:/data/data_copy/figure/datas/Fig5-B-Data2.json")
    usage_count = list(usage_count.values())
    print(len(usage_count))
    count = 0
    for num in usage_count:
        if num > 100:
            values[18] += 1
        elif num > 90 and num <= 100:
            values[17] += 1
        elif num > 80 and num <= 90:
            values[16] += 1
        elif num > 70 and num <= 80:
            values[15] += 1
        elif num > 60 and num <= 70:
            values[14] += 1
        elif num > 50 and num <= 60:
            values[13] += 1
        elif num > 40 and num <= 50:
            values[12] += 1
        elif num > 30 and num <= 40:
            values[11] += 1
        elif num > 20 and num <= 30:
            values[10] += 1
        else:
            index = num // 2
            if num % 2 == 0:
                index -= 1
            if index < 0:
                index = 0
            values[index] += 1
    draw_bar(keys, values, "The Number of Projects Affected by a Library Version (#)", "The Number of Library Versions (#)")

# s_5_1_1()
s_5_1_2()