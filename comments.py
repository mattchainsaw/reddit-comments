from math import log, exp
from sys import stderr, argv
import re

alpha = exp(1)  # cause why not?
maybe_good = 0.0   # for now, assigned in train
maybe_bad  = 0.0   # for now, assigned in train
popularity_cutoff = 10

def clean(str):
    web = re.compile('http://[^ ]+')
    words = re.compile('\W+')
    str = web.sub('URL', str)
    return words.sub(' ', str).strip().lower()

def train(sub):
    global maybe_good
    global maybe_bad
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

        maybe_good = log(alpha) - log(good_wc)
        maybe_bad  = log(alpha) - log(bad_wc)

        for key, count in good.iteritems():
            good[key] = log(count) - log(good_wc)
        for key, count in bad.iteritems():
            bad[key] = log(count) - log(bad_wc)
    except IOError:
        print "No training data. run \"./manage.sh make-dev\" or \"./manage.sh make\""
    return good, bad


def classify(comment, good, bad):
    score = 0
    for word in comment.split():
        try:
            score += good[word]
        except KeyError:
            score += maybe_good
        try:
            score -= bad[word]
        except KeyError:
            score -= maybe_bad
    return score

def test_comment(sub, comment):
    popular, unpopular = train(sub)
    comment = clean(comment)
    return classify(comment, popular, unpopular)


if __name__ == "__main__":
    sub = raw_input('Enter SubReddit: ')
    comment = raw_input('Enter Comment: ')
    karma = test_comment(sub, comment)
    if karma > 0:  # Truth is popular
        print 'Post it! Get Karma!'
    else:
        print 'Don\'t post it!'

