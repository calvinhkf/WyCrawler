import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def draw_bar(x,y,x_label,y_label):
    index = np.arange(len(y))
    plt.bar(index, y, width=0.4, color='lightblue')

    Times_New_Roman = matplotlib.font_manager.FontProperties(fname='C:\\Windows\\Fonts\\times.ttf')

    x_num = range(len(x))
    plt.xticks(x_num, x, rotation=75, fontproperties=Times_New_Roman, fontsize=20)
    # plt.xticks(x_num, x, fontproperties=Times_New_Roman, fontsize=11)
    plt.yticks(fontproperties=Times_New_Roman, fontsize=20)

    # plt.xlabel("Java项目数量")
    # plt.ylabel("第三方库数量（个）")

    plt.xlabel(x_label, fontproperties=Times_New_Roman, fontsize=20)
    plt.ylabel(y_label, fontproperties=Times_New_Roman, fontsize=20)

    # plt.legend()
    for a, b in zip(index, y):
        plt.text(a, b + 0.01, '%.0f' % b, ha='center', va='bottom', rotation=30, fontproperties=Times_New_Roman, fontsize=18)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.show()

def draw_barh(labels, value):
    index = np.arange(len(value))
    b=plt.barh(index, value, color='lightblue')

    Times_New_Roman = matplotlib.font_manager.FontProperties(fname='C:\\Windows\\Fonts\\times.ttf')

    y_ = range(len(labels))
    plt.yticks(y_, labels, fontproperties=Times_New_Roman, fontsize=17)
    plt.xticks(fontproperties=Times_New_Roman, fontsize=20)

    plt.xlabel("The Number of Projects (#)", fontproperties=Times_New_Roman, fontsize=20)

    for rect in b:
        w = rect.get_width()
        plt.text(w, rect.get_y()+rect.get_height()/2, '%d' % int(w), ha='left', va='center', fontproperties=Times_New_Roman, fontsize=18)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.show()

def draw_line(x1,y1,x2,y2,x_label,y_label):
    Times_New_Roman = matplotlib.font_manager.FontProperties(fname='C:\\Windows\\Fonts\\times.ttf')

    l1, = plt.plot(x1, y1, color='b', linestyle=':', marker='o', markerfacecolor='b', markersize=5)
    l2, = plt.plot(x2, y2, color='r', linestyle=':', marker='o', markerfacecolor='r', markersize=5)

    plt.legend([l1, l2], ['twelve months', 'nine months'], loc='upper right')
    # plt.legend()

    plt.xlabel(x_label, fontproperties=Times_New_Roman, fontsize=15)
    plt.ylabel(y_label, fontproperties=Times_New_Roman, fontsize=15)
    plt.xticks(rotation=60)

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.show()