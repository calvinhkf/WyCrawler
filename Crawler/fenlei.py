import os
import json
from sklearn.feature_extraction.text import CountVectorizer  
import time
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer

from file_util import read_json, write_json_format

stopwords = {'he', 'having', 'do', 'by', 'll', "should've", "mustn't", 'such', 'themselves', 't', 'aren', "isn't", 'over', 'wasn', 'don', 'they', 'your', 'these', 'on', 'were', 'further', 'down', 'isn', 'y', 'm', 'ourselves', 'ours', 'very', 'our', 'ma', 'out', 'their', 'yours', 'are', 'itself', 'himself', 'before', 'above', 'up', 'just', 'its', 'more', 'theirs', 'of', 'will', 'being', 'her', 'few', 'him', 'same', 'too', 'this', 'other', 'i', 'can', 're', 'again', "aren't", 'it', 'all', 'is', "you'll", 'my', 'd', 'won', 'than', 'then', 'she', 'doesn', "didn't", 'couldn', 'nor', 'during', "that'll", 'at', 'most', 'because', 'did', "don't", 'didn', 'wouldn', 'against', 'them', 'between', 'each', 'own', 'through', 'under', 'with', 'so', 'until', 'we', 'hers', 'or', 'myself', 'which', 's', 'there', 'once', "hadn't", 'here', 'ain', 'hasn', 'only', 'have', 'who', 'had', 'not', 'weren', 'you', 'shan', 'no', 'some', 'from', 'o', "won't", 'haven', "haven't", 'be', 'mustn', "you've", "weren't", 'but', 'below', 'shouldn', 'when', "needn't", 'how', 'has', "mightn't", 'about', 'where', 'yourself', 'now', "shouldn't", 'herself', "wouldn't", 'needn', "doesn't", 'does', 'in', "you're", 'into', 'whom', 'should', 'me', 'was', "wasn't", 'his', "couldn't", "she's", 'been', 'after', 'yourselves', 'the', 'am', 'if', 'an', 'that', 'and', 'both', "it's", 'mightn', 'while', 'why', "shan't", 'what', 'those', 'off', 'doing', 'as', "hasn't", 'to', 've', 'a', 'any', "you'd", 'for', 'hadn'}
data_dir = "E:/data/ASE2019/category/"

def addAll(item,tree):
    t1 = set(item['tags'])
    max_average = -1
    lis = []
    for cat in tree:
        total = 0
        count = 0
        li = tree[cat]
        for i in li:
            if i['tags']!= None:
                t2 = set(i['tags'])
                if len(t1 & t2) !=0:
                    total += len(t1 & t2)
                    count += 1
        if count > 0:
            # if len(t1) == 1:
            #     average = total
            # else:
            #     average = total/count
            average = total
            if average > max_average:
                max_average = average
                lis = []
                lis.append(li)
            elif average == max_average:
                lis.append(li)
    item['add_type'] = "tagnotnulldescnull"
    for li in lis:
        li.append(item)
    #                 item['add_type'] = "tagnotnulldescnull"
    #                 li.append(item)
    #                 break

def addItemTagNotNull(item,tree):
    t1 = set(item['tags'])
    max_count = -1
    lis = []
    for cat in tree:
        total = 0
        li = tree[cat]
        for i in li:
            if i['tags']!= None:
                t2 = set(i['tags'])
                if len(t1 & t2) !=0:
                    intersection = t1 & t2
                    for tag in intersection:
                        if tag in category_tags[cat]:
                            total += category_tags[cat][tag]
        if total > 0:
            if total > max_count:
                max_count = total
                lis = []
                lis.append(li)
            elif total == max_count:
                lis.append(li)
    item['add_type'] = "tagnotnulldescnull"
    for li in lis:
        li.append(item)
    #                 item['add_type'] = "tagnotnulldescnull"
    #                 li.append(item)
    #                 break

def gen_sim(A, B):
    num = float(np.dot(np.mat(A), np.mat(B).T))
    denum = np.linalg.norm(A) * np.linalg.norm(B)
    if denum == 0:
        denum = 1
    cosn = num / denum
    sim = 0.5 + 0.5 * cosn  # 余弦值为[-1,1],归一化为[0,1],值越大相似度越大
    sim = 1 - sim  # 将其转化为值越小距离越近
    return sim

def addItemTagNotNullDescNotNull(item,tree):
    t1 = set(item['tags'])
    val = 10
    m_li = None
    for cate in tree:
        li = tree[cate]
        for item2 in li:
            if item2['tags'] == None:
                continue
            t2 = set(item2['tags'])
            if len(t1 & t2)!=0:
                v = gen_sim(item['array'],item2['array'])
                if v > 0.4:
                    continue
                # if item["name"] == "RMock":
                #     print("RMock : " + item2["name"] + " " + str(v))
                # if item["name"] == "IText, A Free Java PDF Library (rtf Package)":
                #     print("IText, A Free Java PDF Library (rtf Package) : " + item2["name"] + " " + str(v))
                # if item["name"] == "Dubbo Filter Validation":
                #     print("Dubbo Filter Validation : " + item2["name"] + " " + str(v))
                if v<val:
                    val = v
                    m_li = li
    if m_li == None:
        m_li = tree['No Category']
    item['add_type'] = "tagnotnulldescnotnull"
    m_li.append(item)

def addItemTagNullDescNotNull(item,tree):
    val = 10
    m_li = None
    for cate in tree:
        li = tree[cate]
        for item2 in li:
            v = gen_sim(item['array'],item2['array'])
            if v > 0.4:
                continue
                # if item["name"] == "RMock":
                #     print("RMock : " + item2["name"] + " " + str(v))
                # if item["name"] == "IText, A Free Java PDF Library (rtf Package)":
                #     print("IText, A Free Java PDF Library (rtf Package) : " + item2["name"] + " " + str(v))
                # if item["name"] == "Dubbo Filter Validation":
                #     print("Dubbo Filter Validation : " + item2["name"] + " " + str(v))
            if v<val:
                val = v
                m_li = li
    if m_li == None:
        m_li = tree['No Category']
    item['add_type'] = "tagnulldescnotnull"
    m_li.append(item)


def main():
    with open(data_dir + "CDTAll.json",'r') as f:
        # json.dump(result,f,indent=4)
        j = json.load(f)
    descList = []
    for item in j:
        if item['description'] == None:
            descList.append("")
        else:

            # item['description'] = item['description'].replace('\n','')
            data = item['description'].split(' ')
            newWords = []
            for word in data:
                if not word in stopwords:
                    wnl = WordNetLemmatizer()
                    newW = wnl.lemmatize(word)
                    newWords.append(newW.lower())
            newDesc = ""
            for word in newWords:
                newDesc += word+" "
            descList.append(newDesc)
        # if item['tags'] != None:
        #     if 'apache' in item['tags']:
        #         item['tags'].remove('apache')
    vectorizer=CountVectorizer()
    array = vectorizer.fit_transform(descList).toarray()
    cnt = 0
    for item in j:
        item['array'] = array[cnt]
        cnt+=1
    tree = {}
    tree['No Category'] = []
    for item in j:
        if item['category'] != None:
            if item['category'] not in tree:
                tree[item['category']] = []
            tree[item['category']].append(item)
    cntt =0
    for item in j:
        if cntt>500:
            break
        if item['category'] == None:
            if item['tags'] !=None:
                # cntt += 1
                # addAll(item, tree)
                if item['description'] == None:
                    cntt+=1
                    addAll(item,tree)
                else:
                    cntt+=1
                    addItemTagNotNullDescNotNull(item,tree)
            else:
                if item['description'] !=None:
                    cntt+=1
                    addItemTagNullDescNotNull(item,tree)
    for key in tree:
        en = tree[key]
        for item in en:
            item['array'] = None
    with open(data_dir + 'CDTClustered.json','w') as f:
        json.dump(tree,f,indent=4)

def data_prepare():
    files = os.listdir(data_dir + "parsed")
    all = []
    for file in files:
        obj = read_json(os.path.join(data_dir + "parsed", file))
        description = obj["description"]
        if description is not None:
            description = description.replace("\n", "")
        obj["description"] = description
        tags = obj["tags"]
        if tags is not None and "apache" in tags:
            tags.remove("apache")
            if len(tags) == 0:
                obj["tags"] = None
            else:
                obj["tags"] = tags
        all.append(obj)
    write_json_format(data_dir + "CDTAll.json", all)

def tag_importance():
    # with open(data_dir + "CDTAll.json",'r') as f:
    #     # json.dump(result,f,indent=4)
    #     j = json.load(f)
    # descList = []
    # tree = {}
    # for item in j:
    #     if item['category'] != None:
    #         if item['category'] not in tree:
    #             tree[item['category']] = []
    #         tree[item['category']].append(item)
    # write_json_format(data_dir + "with_category.json", tree)

    # tree = read_json(data_dir + "with_category.json")
    # result = {}
    # for cate in tree:
    #     li = tree[cate]
    #     tags_dict = {}
    #     for item in li:
    #         if item["tags"] is not None:
    #             for t in item["tags"]:
    #                 if t in tags_dict:
    #                     tags_dict[t] += 1
    #                 else:
    #                     tags_dict[t] = 1
    #     result[cate] = tags_dict
    # write_json_format(data_dir + "category_tags.json", result)

    tree = read_json(data_dir + "category_tags.json")
    for cate in tree:
        tag_num = tree[cate]
        total = 0
        for tag in tag_num:
            total += tag_num[tag]
        for tag in tag_num:
            tag_num[tag] = tag_num[tag]/total
    write_json_format(data_dir + "category_tag_percent.json", tree)

def main1():
    with open(data_dir + "CDTAll.json",'r') as f:
        # json.dump(result,f,indent=4)
        j = json.load(f)
    descList = []
    for item in j:
        if item['description'] == None:
            descList.append("")
        else:

            # item['description'] = item['description'].replace('\n','')
            data = item['description'].split(' ')
            newWords = []
            for word in data:
                if not word in stopwords:
                    wnl = WordNetLemmatizer()
                    newW = wnl.lemmatize(word)
                    newWords.append(newW.lower())
            newDesc = ""
            for word in newWords:
                newDesc += word+" "
            descList.append(newDesc)
    vectorizer=CountVectorizer()
    array = vectorizer.fit_transform(descList).toarray()
    cnt = 0
    for item in j:
        item['array'] = array[cnt]
        cnt+=1
    tree = {}
    tree['No Category'] = []
    for item in j:
        if item['category'] != None:
            if item['category'] not in tree:
                tree[item['category']] = []
            tree[item['category']].append(item)
    cntt =0
    for item in j:
        if cntt>500:
            break
        if item['category'] == None:
            if item['tags'] !=None:
                cntt += 1
                addItemTagNotNull(item, tree)
            # else:
            #     if item['description'] !=None:
            #         cntt+=1
            #         addItemTagNullDescNotNull(item,tree)
    for key in tree:
        en = tree[key]
        for item in en:
            item['array'] = None
    with open(data_dir + 'CDTClustered.json','w') as f:
        json.dump(tree,f,indent=4)


# print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
category_tags = read_json(data_dir + "category_tag_percent.json")
main1()
# print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
# data_prepare()
# tag_importance()
