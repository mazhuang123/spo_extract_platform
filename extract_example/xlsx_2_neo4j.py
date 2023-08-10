# -*- coding: utf-8 -*-
# author: Jclian91
# place: Pudong Shanghai
# time: 2020-02-29 11:19

import pandas as pd
from py2neo import Graph, Node, Relationship, NodeMatcher
import config
# 读取Excel文件
df = pd.read_excel(config.excel_path)

# 取前610行作为图谱数据
# df = df.iloc[:706, :]

# 连接Neo4j服务
server_url = "http://localhost:7474"
user_name = "neo4j" #默认用户名就是这个
password = "12345678"#密码是创建数据库时设置的,如果没设置,默认就是 neo4j
# 以下两种方法皆可,但要注意最后一定要再拼上 name = "neo4j",否则后续创建graph的时候就会报jsondecodererror的错误
# graph = Graph(server_url,username = user_name,password = password,name = "neo4j")
graph = Graph(server_url,auth= (user_name,password),name="neo4j")

# 创建节点
nodes = set(df['S'].tolist()+df['O'].tolist())
for node in nodes:
    node = Node("Node", name=node)
    graph.create(node)

print('create nodes successfully!')

# 创建关系
matcher = NodeMatcher(graph)
for i in range(df.shape[0]):
    S = df.iloc[i, :]['S']  # S节点
    O = df.iloc[i, :]['O']  # O节点
    s_node = matcher.match("Node", name=S).first()
    o_node = matcher.match("Node", name=O).first()

    # 创建关系
    P = df.iloc[i, :]['P']
    relationship = Relationship(s_node, P, o_node)
    graph.create(relationship)

print('create relationships successfully!')
print('You can check Neo4j now!')
