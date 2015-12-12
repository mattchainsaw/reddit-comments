from sys import stderr, argv
from build import clean
import pickle


def rand_score():
    import random
    if random.random() > 0.5:
        return 1
    else:
        return -1


def test_comment(comment, pop, unpop):
    comment = clean(comment)
    score = 0
    for word in comment.split():
        try:
            score += pop[word]
        except KeyError:
            score += pop['__unknown__']
        try:
            score -= unpop[word]
        except KeyError:
            score -= unpop['__unknown__']
    return score


if __name__ == "__main__":
    global threshold
    right = 0
    total = 0
    pop = 0
    unpop = 0
    sub = argv[1]
    threshold = int(argv[2])
    comments = file('test/' + sub + '.test').read().split('\n')
    popular = pickle.load(open('data/' + sub + '.popular.pickle', 'rb'))
    unpopular = pickle.load(open('data/' + sub + '.unpopular.pickle', 'rb'))
    for c in comments:
        if c == '':
            continue
        s, comm = c.split('\t', 1)
        score = int(s)
        guess = test_comment(comm, popular, unpopular)
        #guess = rand_score()
        if score >= threshold:
            pop += 1
        else:
            unpop += 1
        if (guess > 0 and score >= threshold) or (guess < 0 and score < threshold):
            right = right + 1
        total = total + 1

    perc = float(right)/float(total)
    print "%s\n\t%s correct\n\t%s popular\n\t%s unpopular" % (sub, perc, pop, unpop)
