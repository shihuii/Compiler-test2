import matplotlib.pyplot as plt
import graphviz
from PIL import Image
import io

def func1():
    # 定义节点列表
    nodes = [(0, '0', 'end'), (1, '1', ''), (2, '2', ''), (3, '3', ''),
    (4, '4', ''),(5, '5', ''), (6, '6', ''), (7, '7', ''),
    (8, '8', ''), (9, '9', ''), (10, '10', ''), (11, '11', ''), 
    (12, '12', 'end')]

    # 定义边列表
    edges = [(0, 1, 'a'), (1, 5, 'ε'), (2, 3, 'b'), (3, 5, 'ε'),
            (4, 2, 'ε'), (4, 0, 'ε'), (5, 4, 'ε'), (5, 7, 'ε'),
            (6, 4, 'ε'), (6, 7, 'ε'), (7, 8, 'ε'), (8, 9, 'a'),
            (9, 10, 'ε'), (10, 11, 'b'), (11, 12, 'ε')]

    # 创建有向图并设置布局方向为水平
    dot = graphviz.Digraph(graph_attr={'rankdir': 'LR'})

    # 添加节点
    for node in nodes:
        # 检查节点是否为"结束"节点，如果是，则添加两个环的标记
        if node[2] == 'end':
            dot.node(str(node[0]), node[1], shape='doublecircle')
        else:
            dot.node(str(node[0]), node[1])

    # 添加边
    for edge in edges:
        dot.edge(str(edge[0]), str(edge[1]), label=edge[2])

    # 渲染图形并获取图像数据
    dot.format = 'png'
    image_data = dot.pipe()

    # 将图像数据加载到PIL图像对象中
    image = Image.open(io.BytesIO(image_data))

    # 显示图像
    plt.imshow(image)
    plt.axis('off')
    plt.show()
