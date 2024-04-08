import os
import json

import numpy as np
from py2neo import Node, Graph
from tqdm import tqdm
import pickle
import pandas as pd


# 定义中心节点性质和读取节点

product_node_attr = ['name', '所属产业','node_type']
industry_node_attr = ['name','下游总产业','node_type']
domain_industry_node_attr = ['name','所属总产业','node_type']
with open('./data/company_node_attr.json','r', encoding='utf-8') as f:
    company_node_attr = json.load(f)


with open('./data/industry_nodes.json', 'r', encoding='utf-8') as f:
    industry_nodes = json.load(f)

with open('./data/domain_industry_nodes.json', 'r', encoding='utf-8') as f:
    domain_industry_nodes = json.load(f)

with open('./data/company_nodes.json','r', encoding='utf-8') as f:
    company_nodes = json.load(f)


with open('./data/product_nodes.json','r', encoding='utf-8') as f:
    product_nodes = json.load(f)


# 定义关系集
edges_set = {
    'domain_industry_belongs_to' : set(),
    'product_belongs_to': set(),
    # 'produce': set(),
    'company_belongs_to': set(),
    'downstream_industry': set(),
}

# 定义关系三元组

edges_set_tuple = {
    'domain_industry_belongs_to' : ['domain_industry','industry','属于'],
    'product_belongs_to': ['product','domain_industry','属于'],
    # 'produce': ['company','product','生产'],
    'company_belongs_to': ['company','domain_industry','生产'],
    'downstream_industry': ['industry', 'industry','下游'],
}


# 在预定义集合中搜索并构建边关系

for k in edges_set.keys():
    key_tuple = edges_set_tuple[k]
    type1 = key_tuple[0]
    type2 = key_tuple[1]
    if type1 == 'domain_industry' and type2 == 'industry':
        for node1 in domain_industry_nodes:
            ind_name = node1['所属总产业']
            for node2 in industry_nodes:
                if node2['name'] == ind_name:
                    edges_set[k].add((node1['name'], node2['name']))
                    break
    elif type1 == 'product' and type2 == 'domain_industry':
        for node1 in product_nodes:
            domain_name = node1['所属产业']
            for node2 in domain_industry_nodes:
                if node2['name'] == domain_name:
                    edges_set[k].add((node1['name'], node2['name']))
                    break
    elif type1 == 'company' and type2 == 'domain_industry':
        for node1 in company_nodes:
            for t in range(5):
                product_name = node1[f'标准产品{t+1}']
                # print(f'product_name = {product_name}')
                for node2 in domain_industry_nodes:
                    if node2['name'] == product_name:
                        edges_set[k].add((node1['name'], node2['name']))
                        break
    elif type1 == 'industry' and type2 == 'industry':
        for node1 in industry_nodes:
            ind_name = node1['下游总产业']
            for node2 in industry_nodes:
                if node2['name'] == ind_name:
                    edges_set[k].add((node1['name'], node2['name']))
                    break


graph = Graph('http://localhost:7474', user='neo4j', password='neo4j')

for n in industry_nodes:
    node = Node('industry', **n)
    graph.create(node)

for n in domain_industry_nodes:
    node = Node('domain_industry', **n)
    graph.create(node)

for n in company_nodes[:500]:
    node = Node('company', **n)
    graph.create(node)

for n in product_nodes:
    node = Node('product', **n)
    graph.create(node)

for rel_type, edges in edges_set.items():
    start_node, end_node, rel_name = edges_set_tuple[rel_type]
    print(start_node, end_node, rel_name)

    for edge in edges:
        p, q = edge
        # print(f"p = {p}, q={q}")
        query = f"""
        match(p:{start_node}),(q:{end_node})
        where p.name='{p}' and q.name='{q}'
        merge (p)-[rel:{rel_name}{{name:'{rel_name}'}}]->(q)
        """
        try:
            graph.run(query)
        except Exception as e:
            print(e)
