from selfcheck import *
import json
from matplotlib import pyplot as plt
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

  positioning = check_ans("./dataset/positioning.json")
  print("positioning:", positioning)
