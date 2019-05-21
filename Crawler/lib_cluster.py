import os
import nltk

from file_util import read_json, write_json

new_data_dir = "E:/data/ASE2019/"

def parse():
    dir = new_data_dir + "category/origin"
    files = os.listdir(dir)
    count = 0
    for file in files:

        lib = read_json(os.path.join(dir, file))
        lib.pop('id')
        lib.pop('license')
        name = lib["name"]
        description = lib["description"]
        tags = lib["tags"]
        categories = lib["categories"]
        lib.pop('categories')

        if description is not None:
            description = description.replace("\n", "")
            if description == name:
                lib["description"] = None
        if categories is not None:
            categories = eval(categories)
            lib["category"] = list(categories.keys())[0]
        else:
            lib["category"] = None
        if tags is not None:
            tags = eval(tags)
            lib["tags"] = list(tags.keys())
            # if len(tags.keys()) < 1:
            #     print("++++++++++++++++++ " + file)
            #     print(list(tags.keys()))
        write_json(new_data_dir + "category/parsed/" + file, lib)

def have_category():
    dir = new_data_dir + "category/parsed"
    files = os.listdir(dir)
    count = 0
    for file in files:
        lib = read_json(os.path.join(dir, file))
        categories = lib["category"]
        tags = lib["tags"]
        description = lib["description"]
        if categories is not None or tags is not None:
            count += 1
        # else:
        #     pr
        # if categories is None and tags is None and description is None:
        #     count += 1
            # print(file)
    print(count)

# parse()
# have_category()
nltk.download()