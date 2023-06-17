#memorization数据集平均分: 0.0409011906310916
#computation数据集平均分: 0.05711951076984406
#counting数据集平均分: 0.0729929949939251
#noise_injection数据集平均分: 0.11578143765528996
#substitution: 0.16770769235491753
#positioning数据集平均分: 0.0922118888581665

import matplotlib.pyplot as plt

dataset = ['memorization', 'computation',
           'counting', 'positioning', 'noise_injection', 'substitution']
BERTScore = [0.0409011906310916, 0.05711951076984406,
             0.0729929949939251, 0.0922118888581665, 0.11578143765528996, 0.16770769235491753]
plt.rcParams["font.sans-serif"] = ['SimHei']
plt.rcParams["axes.unicode_minus"] = False

plt.figure(figsize=(10, 10))
for i in range(len(dataset)):
    plt.bar(dataset[i], BERTScore[i])


plt.title("不同数据集上的置信度得分")
plt.xlabel("数据集名称")
plt.ylabel("置信度(BERTScore)")

plt.show()

