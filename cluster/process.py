import langid
import jsonlines
from tqdm import tqdm

with jsonlines.open('./datasets/ift_cluster_given_fudandm2023.jsonl', 'r') as rf:
    print("按照语言分类")
    for data in tqdm(rf):
        prompt = data['label']
        print(prompt)
        prompt = prompt.replace("、",'')

    print("分类结束")
# Counter({'zh': 16428, 'en': 16328, 'es': 181, 'la': 124, 'ja': 88, 'hi': 65, 'ar': 64, 'bn': 55, 'fa': 49, 'ru': 31, 'gu': 30, 'te': 25, 'fr': 22, 'ur': 20, 'ta': 18, 'ml': 17, 'ky': 14, 'vi': 13, 'pl': 13, 'de': 12, 'pa': 11, 'lo': 11, 'kn': 10, 'he': 10, 'it': 9, 'mr': 8, 'ps': 5, 'nl': 5, 'pt': 5, 'ca': 5, 'or': 4, 'da': 3, 'th': 3, 'ko': 3, 'cs': 3, 'mk': 2, 'no': 2, 'si': 2, 'fi': 2, 'tl': 2, 'sv': 2, 'as': 2, 'eu': 1, 'hu': 1, 'sk': 1, 'br': 1, 'et': 1, 'tr': 1, 'el': 1, 'ms': 1, 'an': 1})
