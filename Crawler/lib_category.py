import os

from file_util import read_json, write_json, write_json_format

new_data_dir = "E:/data/ASE2019/"
category_dir = "E:/data/ASE2019/category/"

def get_top():
    categories = read_json(category_dir + "have_category.txt")
    # print(len(categories))
    categories1 = read_json(category_dir + "have_category_add.txt")
    # print(len(categories1))
    to_do = set()
    # file = "datas/s_1_b_top.txt"
    files = ["category_data/s_5_d_top.txt", "category_data/s_5_d_bottom.txt"]
    for file in files:
        data = read_json(os.path.join(new_data_dir, file))
        # print(len(data))
        for entry in data:
            to_do.add(entry)
    print(len(to_do))
    total = set()
    for lib in to_do:
        if lib not in categories and lib not in categories1:
            # print(lib)
            total.add(lib)
    print(len(total))
    write_json_format(category_dir + "to_do_list.txt", list(total))

def with_category():
    to_do = read_json(category_dir + "to_do_list.txt")
    print(len(to_do))
    # to_do["org.apache.hadoop__fdse__hadoop-hdds-server-framework"] = "HBase Clients"
    # to_do["org.springframework.cloud__fdse__spring-cloud-netflix-hystrix-contract"] = "Web Frameworks"
    # to_do["pentaho__fdse__pentaho-platform-core"] = "Enterprise Integration"
    # print(len(to_do))
    # write_json_format(category_dir + "have_category_add.txt", to_do)
    # categories = {}
    new_dict = {}
    j = read_json(category_dir + "CDTAll.json")
    print(len(j))
    # for item in j:
    #     groupId = item["groupId"]
    #     artifactId = item["artifactId"]
    #     new_dict[groupId + "__fdse__" + artifactId] = item
    # write_json_format(category_dir + "CDTAllWithKey.json", new_dict)
    # tree = {}
    # count = 0
    # for item in j:
    #     if item['category'] != None:
    #         count += 1
    #         if item['category'] not in tree:
    #             tree[item['category']] = []
    #             tree[item['category']].append(item)
    #         else:
    #             tree[item['category']].append(item)
    # print(count)
    # write_json_format(category_dir + "with_category_obj.json", tree)

    # tree = read_json(category_dir + "with_category_obj.json")
    # count = 0
    # for entry in tree.keys():
    #     count += len(tree[entry])
    # print(count)
    # descList = []
    # for item in j:
    #     if item['description'] == None:
    #         descList.append("")
    #     else:
    #
    #         # item['description'] = item['description'].replace('\n','')
    #         data = item['description'].split(' ')
    #         newWords = []
    #         for word in data:
    #             if not word in stopwords:
    #                 wnl = WordNetLemmatizer()
    #                 newW = wnl.lemmatize(word)
    #                 newWords.append(newW.lower())
    #         newDesc = ""
    #         for word in newWords:
    #             newDesc += word+" "
    #         descList.append(newDesc)
    # vectorizer=CountVectorizer()
    # array = vectorizer.fit_transform(descList).toarray()
    # cnt = 0
    # for item in j:
    #     item['array'] = array[cnt]
    #     cnt+=1
    # tree = {}
    # tree['No Category'] = []

    # categories = {}
    # for item in j:
    #     if item['category'] != None:
    #         groupId = item["groupId"]
    #         artifactId = item["artifactId"]
    #         categories[groupId + "__fdse__" + artifactId] = item['category']
    # write_json_format(category_dir + "have_category_add.txt", categories)

    # new_list = []
    # count = 0
    # for item in j:
    #     groupId = item["groupId"]
    #     artifactId = item["artifactId"]
    #     if groupId + "__fdse__" + artifactId in to_do:
    #         count += 1
    #         new_list.append(item)
    # print(count)
    # write_json_format(category_dir + "to_do_obj.txt", new_list)
    data = read_json(category_dir + "to_do_obj.txt")
    print(len(data))
    # for item in data:
    #     if item["tags"] is None:
    #         print(1)

def parse_top():
    # categories = read_json(category_dir + "have_category.txt")
    # print(len(categories))
    # categories1 = read_json(category_dir + "have_category_add.txt")
    # print(len(categories1))
    # # files = ["s_1_b_top.txt", "s_3_b_top.txt", "s_4_b_top.txt"]
    # # files = ["s_1_b_top.txt", "s_3_b_top.txt", "s_4_b_top.txt"]
    # files = ["s_5_b_bottom.txt"]
    # for file in files:
    #     print(new_data_dir, "category_data/" + file)
    #     total = {}
    #     data = read_json(os.path.join(new_data_dir, "category_data/" + file))
    #     for entry in data:
    #         # lib = entry[0]
    #         lib = entry
    #         # print(lib)
    #         if lib in categories:
    #             cate = categories[lib]
    #         elif lib in categories1:
    #             cate = categories1[lib]
    #         # if cate  == 'Dependency Injection':
    #         #     print(lib)
    #         if cate in total:
    #             total[cate] += 1
    #         else:
    #             total[cate] = 1
    #     write_json_format(category_dir + "result/" + file, total)
        # print(len(total))

    count = 0
    data = read_json(new_data_dir + "category/result/" + "s_5_b_bottom.txt")
    for entry in data:
        count += data[entry]
    print(count)

# get_top()
with_category()
# parse_top()