# -*- coding: utf-8 -*-
# author: Jclian91
# place: Pudong Shanghai
# time: 2020-02-29 11:19
import json

import pandas as pd
from py2neo import Graph, Node, Relationship, NodeMatcher
import config

# 读取Excel文件
df = pd.read_excel(config.excel_path)

# 连接Neo4j服务
server_url = "http://localhost:7474"
user_name = "neo4j" #默认用户名就是这个
password = "12345678"#密码是创建数据库时设置的,如果没设置,默认就是 neo4j
# 以下两种方法皆可,但要注意最后一定要再拼上 name = "neo4j",否则后续创建graph的时候就会报jsondecodererror的错误
# graph = Graph(server_url,username = user_name,password = password,name = "neo4j")
graph = Graph(server_url,auth= (user_name,password),name="neo4j")
matcher = NodeMatcher(graph)



for temp_list in df['spo_dic']:
    value_str = str(temp_list)
    value_str = value_str.replace("'",'"')
    spo_dic = json.loads(value_str)

    s_str = spo_dic[0]['S']
    print(s_str)

    nodes_data = graph.run("MATCH (n) where n.name contains'" + s_str + "' return n").data()

    # temp_node = matcher.match("Node", name=s_str).first()
    if len(nodes_data) >0:
        root_node = nodes_data[0]['n']
    else:
        root_node = Node(s_str, name=s_str)
        graph.create(root_node)

    for temp_dic in spo_dic:
        obj_str = temp_dic['O']
        child_nodes_data = graph.run("MATCH (n) where n.name contains'" + obj_str + "' return n").data()
        if len(child_nodes_data) > 0:
            child_node =                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           child_nodes_data[0]['n']
        else:
            child_node = Node(obj_str, name=obj_str)
            graph.create(child_node)

        relationship = Relationship(root_node, temp_dic['P'], child_node)
        graph.create(relationship)

print('create relationships successfully!')
print('You can check Neo4j now!')