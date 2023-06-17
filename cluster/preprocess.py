
em_beds_dim = 3

from multiprocessing import reduction
import numpy as np  
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

def dim_reduction(em_beds_dim):

    #导入npy文件路径位置
    test = np.load('C:\\Users\\15957\\Desktop\\2023\\data mining\\project\\npy_embs\\ift_cluster_given_fudandm2023-input-bert-base-chinese.npy')
    print(test.shape)
    print(f">>> t-SNE fitting")
    tsne = TSNE(n_components=em_beds_dim, init='pca', perplexity=30)
    Y = tsne.fit_transform(test)
    print(f"<<< fitting over")
    print(Y.shape)
    path = str(em_beds_dim) +"d_emb"
    np.save(path, Y)
    return Y


def add_label(file_name, last_label):
    import langid
    import jsonlines
    from tqdm import tqdm
    file_name = './datasets/' + file_name
    with jsonlines.open(file_name, 'w') as cf:
        with jsonlines.open('./datasets/ift_cluster_given_fudandm2023.jsonl', 'r') as rf:
            print("add label")
            for data,label in zip(tqdm(rf), last_label):
                write = data
                write['label'] = str(label)
                cf.write(write)

def show_2d():
    pass

dim_reduction(2)
dim_reduction(3)