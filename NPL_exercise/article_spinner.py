import nltk
import random

from bs4 import BeautifulSoup

# read data
pos_reviews = BeautifulSoup(open('../data/electronics/positive.review').read())
pos_reviews = pos_reviews.findAll('review_text')

# extract trigram
trigrams = {}
for review in pos_reviews:
    s = review.text.lower()
    # ?
    tokens = nltk.tokenize.word_tokenize(s)
    for i in range(len(tokens) -2):
        k = (tokens[i], tokens[i+2])
        if k not in trigrams:
            trigrams[k] = []
        trigrams[k].append(tokens[i+1])

# turn to probabilities
trigram_probabilities = {}
for k, words in trigrams.items():
    if len(set(words)) > 1:
        d = {}
        n = 0
        for w in words:
            if w not in d:
                d[w] = 0;
            d[w] += 1
            n += 1
        for w, c in d.items():
            d[w] = float(c) / n
        trigram_probabilities[k] = d

# choose a random sample from dictionary where values are the probabilities
def random_sample(d):
    r = random.random()
    cumulative = 0;
    for w, p in d.items():
        cumulative += p
        if r < cumulative:
            return w

def test_spinner():
    # 随机选一句话
    review = random.choice(pos_reviews)
    s = review.text.lower()
    print("Original: ", s)

    # 两两组合选取
    tokens = nltk.tokenize.word_tokenize(s)
    for i in range(len(tokens) -2):
        # 选出key
        k = (tokens[i], tokens[i+2])
        if k in trigram_probabilities:
            # 找到key对应的小字典， 并从中随机选一个词
            w = random_sample(trigram_probabilities[k])
            #替换词
            tokens[i+1] = w
    print("Spun:")
    # 消除空格
    print(" ".join(tokens).replace(" .", ".").replace(" '", "'").replace(" ,", ",").replace("$ ", "$").replace(" !", "!"))


if __name__ == '__main__':
    test_spinner()
