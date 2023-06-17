from selfcheck import *
import json

N_SAMPLES = 100


def check_ans(file):
    scores = []
    with open(file, 'r') as file:
        data = json.load(file)
        for i in range(N_SAMPLES):
            score = selfcheck(data[i]['question'])
            scores.append(score)
    return np.mean(scores)


if __name__ == "__main__":
    computation = check_ans("./dataset/computation.json")

    with open("computation.txt", "w", encoding='utf-8') as f:
        f.write("computation数据集平均分: {}".format(computation))
