from math import log, exp
from sys import stderr, argv
import re
import pickle

alpha = exp(1)  # cause why not?
popularity_cutoff = 10

def clean(str):
    web = re.compile('http://[^ ]+')
    words = re.compile('\W+')
    str = web.sub('URL', str)
    return words.sub(' ', str).strip().lower()

def train(sub):
    good = dict()
    bad = dict()
    good_wc = 0.0
    bad_wc = 0.0
    try:
        training = file("comments/" + sub.lower()).read().split('\n')
        for line in training:
            if line == '':
                continue

            score, text = line.split('\t', 1)
            text = clean(text)
            if int(score) > popularity_cutoff:
                for word in text.split():
                    try:
                        good[word] += 1
                    except KeyError:
                        good[word] = 1
                    good_wc += 1 + alpha
            else:
                for word in text.split():
                    try:
                        bad[word] += 1
                    except KeyError:
                        bad[word] = 1
                    bad_wc += 1 + alpha

        for key, count in good.iteritems():
            good[key] = log(count) - log(good_wc)
        for key, count in bad.iteritems():
            bad[key] = log(count) - log(bad_wc)
        good['__unknown__'] = log(alpha) - log(good_wc)
        bad['__unknown__']  = log(alpha) - log(bad_wc)
    except IOError:
        print "No training data. run \"./manage.sh make-dev\" or \"./manage.sh make\""
    return good, bad

if __name__ == "__main__":
    sub = argv[1]
    popular, unpopular = train(sub)
    pickle.dump(popular, file('data/' + sub + '.popular.pickle', 'wb+'))
    pickle.dump(unpopular, file('data/' + sub + '.unpopular.pickle', 'wb+'))

