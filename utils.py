from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

class KMeansPlot:

    def __init__(self, numClass=4, func_type='PCA'):
        if func_type == 'PCA':
            self.func_plot = PCA(n_components=2)
        elif func_type == 'TSNE':
            from sklearn.manifold import TSNE
            self.func_plot = TSNE(2, perplexity=50)
        self.numClass = numClass

    def plot_cluster(self, result, pos, cluster_centers=None):
        plt.figure(2)
        Lab = [[] for i in range(self.numClass)]
        index = 0
        for labi in result:
            Lab[labi].append(index)
            index += 1
        color = ['oy', 'ob', 'og', 'cs', 'ms', 'bs', 'ks', 'ys', 'yv', 'mv', 'bv', 'kv', 'gv', 'y^', 'm^', 'b^', 'k^',
                 'g^'] * 3

        for i in range(self.numClass):
            x1 = []
            y1 = []
            for ind1 in pos[Lab[i]]:
                # print ind1
                try:
                    y1.append(ind1[1])
                    x1.append(ind1[0])
                except:
                    pass
            plt.plot(x1, y1, color[i])

        if cluster_centers is not None:
            #绘制初始中心点
            x1 = []
            y1 = []

            for ind1 in cluster_centers:
                try:
                    y1.append(ind1[1])
                    x1.append(ind1[0])
                except:
                    pass

            plt.plot(x1, y1, "rv")  # 绘制中心

        plt.show()

    def plot(self, weight, label, cluster_centers=None):
        pos = self.func_plot.fit_transform(weight)
        # 高维的中心点坐标，也经过降维处理
        cluster_centers = self.func_plot.fit_transform(cluster_centers)
        self.plot_cluster(list(label), pos, cluster_centers)
