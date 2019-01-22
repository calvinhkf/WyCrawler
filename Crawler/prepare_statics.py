import os

from file_util import read_json, read_file


def android_proj():
    android_count = 0
    no_count = 0
    m_g_count = 0
    lines = read_file("C:/Users/yw/Desktop/I-result-7-25_500.txt")
    for line in lines:
        if line == "proj-type: android":
            android_count += 1
        elif line == "proj-type: no":
            no_count += 1
        elif line == "proj-type: maven" or line == "proj-type: gradle" or line == "proj-type: maven-gradle":
            m_g_count += 1
        elif line.startswith("proj-type:"):
            print(line)

    lines = read_file("C:/Users/yw/Desktop/I-result-7-25.txt")
    for line in lines:
        if line == "proj-type: android":
            android_count += 1
        elif line == "proj-type: no":
            no_count += 1
        elif line == "proj-type: maven" or line == "proj-type: gradle" or line == "proj-type: maven-gradle":
            m_g_count += 1
        elif line.startswith("proj-type:"):
            print(line)
    #
    print(android_count)
    print(no_count)
    print(m_g_count)

# android_proj()
json_data = read_json("E:/data/projs.json");
print(len(json_data))