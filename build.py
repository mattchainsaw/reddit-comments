from math import log, exp
from sys import stderr, argv
from most_common_words import most_common
import re
import pickle

alpha = exp(1)  # cause why not?

def clean(str):
    web = re.compile('http://[^ ]+')
    words = re.compile('\W+')
    str = web.sub('URL', str)
    str = words.sub(' ', str).strip().lower()
    str = ' '.join(w for w in str.split() if w not in most_common)
    return str

def train(sub, dir):
    good = dict()
    bad = dict()
    good_wc = 0.0
    bad_wc = 0.0
    try:
        training = file(dir + '/' + sub.lower()).read().split('\n')
        for line in training:
            if line == '':
                continue

            score, text = line.split('\t', 1)
            score = float(score)
            text = clean(text)
            if score <= 0:
                score = 0.01
            if score > popularity_cutoff:
                for word in text.split():
                    try:
                        good[word] += score/popularity_cutoff
                    except KeyError:
                        good[word] = score/popularity_cutoff
                    good_wc += score/popularity_cutoff + alpha
            else:
                for word in text.split():
                    try:
                        bad[word] += popularity_cutoff/score
                    except KeyError:
                        bad[word] = popularity_cutoff/score
                    bad_wc += popularity_cutoff/score + alpha

        for key, count in good.iteritems():
            good[key] = log(count) - log(bad_wc)
        for key, count in bad.iteritems():
            bad[key] = log(count) - log(good_wc)
        good['__unknown__'] = log(alpha) - log(good_wc)
        bad['__unknown__']  = log(alpha) - log(bad_wc)
    except IOError:
        print "No training data."
    return good, bad

if __name__ == "__main__":
    global popularity_cutoff
    sub = argv[1]
    dir = argv[2]
    popularity_cutoff = float(argv[3])
    popular, unpopular = train(sub, dir)
    pickle.dump(popular, file('data/' + sub + '.popular.pickle', 'wb+'))
    pickle.dump(unpopular, file('data/' + sub + '.unpopular.pickle', 'wb+'))

