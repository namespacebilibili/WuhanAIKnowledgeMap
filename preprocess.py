import pandas as pd

# 定义与人工智能相关的关键词列表
ai_keywords = ['人工智能', 'AI', '智能算法', '机器学习', '深度学习', '神经网络', '计算机视觉',
               '自然语言处理', '知识图谱', '大数据', '数据挖掘', '数据分析', '机器人']

def preprocess():
    data = pd.read_csv('data/武汉市企业工商信息.csv', encoding='utf-8')

    # 创建一个空列表,用于存储与人工智能相关的条目
    ai_entries = []

    # 遍历每一行数据
    for index, row in data.iterrows():
        # 获取经营范围
        business_scope = row['经营范围']

        # 检查经营范围中是否包含任何关键词
        for keyword in ai_keywords:
            if keyword in business_scope:
                ai_entries.append(row)
                break

    # 将与人工智能相关的条目存储为新的CSV文件
    ai_data = pd.DataFrame(ai_entries)
    ai_data.to_csv('data/武汉市AI相关企业.csv', index=False)

    print(f'一共找到 {len(ai_entries)} 条与人工智能相关的条目。')

def cluster_product():
    import torch
    import numpy as np
    from text2vec import SentenceModel
    from fast_pytorch_kmeans import KMeans
    from utils import KMeansPlot
    import pickle

    data = pd.read_csv('data/武汉市AI相关企业.csv', encoding='utf-8')
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    ai_products = set()
    for index, row in data.iterrows():
        bussiness_scope = row['经营范围'][5:]
        # 替换标点符号为空格
        puncs = ',，。、；（）;：'
        for punc in puncs:
            bussiness_scope = bussiness_scope.replace(punc, ' ')
        for product in bussiness_scope.split(' '):
            for keyword in ai_keywords:
                if keyword in product:
                    ai_products.add(product)
                    break

    ai_products = list(ai_products)
    with open('data/武汉市AI相关企业产品.txt', 'w') as f:  # Open the file in text mode
        for product in ai_products:
            f.write(product + '\n')
    embedding_model = SentenceModel()     
    embeddings = embedding_model.encode(ai_products)
    embeddings = torch.from_numpy(embeddings)

    num_classes = 5
    kmeans = KMeans(n_clusters=num_classes, mode='euclidean', verbose=1)
    labels = kmeans.fit_predict(embeddings)
    centroids = kmeans.centroids
    class_data = {
        i: [] for i in range(num_classes)
    }
    for product, label in zip(ai_products, labels):
        class_data[label.item()].append(product)

    with open('data/武汉市AI相关企业产品分类.pkl', 'wb') as f:
        pickle.dump(class_data, f)

    k_plot = KMeansPlot(numClass=num_classes, func_type='PCA')
    k_plot.plot(embeddings.to('cpu'), labels.to('cpu'), kmeans.centroids.to('cpu'))

def match_product_to_standard_product():
    import pickle

    class_data = {}
    with open('data/武汉市AI相关产品分类.txt', 'r') as f:
        matches = f.readlines()

    for match in matches:
        try:
            product, standard_products = tuple(match.split(':'))
        except:
            print(match)
            exit()
        standard_products = standard_products.split('、')
        for standard_product in standard_products:
            # delete space and \n in the end
            standard_product = standard_product.strip()
            if standard_product not in class_data.keys():
                class_data[standard_product] = set()
            class_data[standard_product].add(product)
    print(class_data.keys())
    for key in class_data.keys():
        class_data[key] = list(class_data[key])
    with open('data/武汉市AI相关企业产品分类.pkl', 'wb') as f:
        pickle.dump(class_data, f)

def add_standard_product():
    import pickle
    import pandas as pd
    with open('data/武汉市AI相关企业产品分类.pkl', 'rb') as f:
        class_data = pickle.load(f)
    company_data = pd.read_csv('data/武汉市AI相关企业.csv', encoding='utf-8') 
    inverse_class_data = {v: k for k, vs in class_data.items() for v in vs}

    # 产业链划分
    chain_info = {
        '人工智能技术研发': ['人工智能通用技术研发'],
        '人工智能产品研发': ['人工智能软硬件产品研发'],
        '人工智能产品制造': ['人工智能产品生产'],
        '销售与服务': ['人工智能数据服务', '人工智能教育服务', '人工智能系统集成服务', '人工智能产品销售', '人工智能产品租赁服务', '人工智能其他服务', '人工智能产业投资服务', '人工智能技术培训服务', '人工智能技术服务']
    }
    inverse_chain_info = {v: k for k, vs in chain_info.items() for v in vs}
    # print(f"{set(class_data.keys()) - set(inverse_chain_info.keys())}")
    assert inverse_chain_info.keys() == class_data.keys()

    # 将 “标准产品{1-6}”, “产业链{1-4}”  加入csv数据的列名
    for i in range(1, 6):
        company_data[f'标准产品{i}'] = ''
    for i in range(1, 5):
        company_data[f'产业链{i}'] = ''

    for index, row in company_data.iterrows():
        bussiness_scope = row['经营范围'][5:]
        # 替换标点符号为空格
        puncs = ',，。、；（）;：'
        for punc in puncs:
            bussiness_scope = bussiness_scope.replace(punc, ' ')
        for product in bussiness_scope.split(' '):
            standard_products = set()
            chain_classes = set()
            for key_word in ai_keywords:
                if key_word in product:
                    try:
                        standard_product = inverse_class_data[product]
                        chain_class = inverse_chain_info[standard_product]
                        standard_products.add(standard_product)
                        chain_classes.add(chain_class)
                    except:
                        print(f'产品 {product} 未找到对应的标准产品')
                        continue
            for i, standard_product in enumerate(standard_products):
                company_data.at[index, f'标准产品{i+1}'] = standard_product
            for i, chain_class in enumerate(chain_classes):
                company_data.at[index, f'产业链{i+1}'] = chain_class

    company_data.to_csv('data/武汉市AI相关企业(新).csv', index=False)


if __name__ == '__main__':
    # preprocess()
    # cluster_product()
    match_product_to_standard_product()
    add_standard_product()
