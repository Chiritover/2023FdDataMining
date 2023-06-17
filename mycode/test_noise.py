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
  noise_injection = check_ans("./dataset/noise_injection.json")
  print("noise:",noise_injection)
