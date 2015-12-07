from sys import stderr, argv
from build_models import clean
import pickle

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
    sub = raw_input('Enter SubReddit: ')
    comment = raw_input('Enter Comment: ')
    popular = pickle.load(open('data/' + sub + '.popular.pickle', 'rb'))
    unpopular = pickle.load(open('data/' + sub + '.unpopular.pickle', 'rb'))
    karma = test_comment(comment, popular, unpopular)
    if karma > 0:  # Truth is popular
        print 'Post it! Get Karma!'
    else:
        print 'Don\'t post it!'

