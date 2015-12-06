import json
import time
import sys
import httplib

TIME_BETWEEN_GETS = 2
POSTS_PER_PAGE = 25
comments = []
sub = sys.argv[1]
outFile = sys.argv[2]
hdr = {'User-Agent': 'chainsaw flailing comment grabber'}
conn = httplib.HTTPConnection('www.reddit.com')
clock = 0.0


# pulls a web page and returns it as a json object
def pull(url):
    global clock
    global conn
    t = time.time() - clock
    if t < 2:
        time.sleep(2 - t)
    clock = time.time()
    try:
        conn.request('GET', url, headers=hdr)
        txt = conn.getresponse().read()
        print 'download is successful: %s' % url
        return json.loads(txt)
    except:
        print 'download unsuccessful: %s' % url
        conn.close()
        conn = httplib.HTTPConnection('www.reddit.com')
    return None


class comment:
    def __init__(self, s, b):
        self.score = s
        b = ' '.join(b.split())
        self.body = b

    def __str__(self):
        return "%s\t%s" % (self.score, self.body)


def parseComment(child):
    try:
        score = child['data']['score']
        body = child['data']['body']
        comments.append(comment(score, body))
        if child['data']['replies'] != '':
            n = len(child['data']['replies']['data']['children'])
            for i in range(n):
                grand = child['data']['replies']['data']['children'][i]
                parseComment(grand)
    except KeyError as e:
        pass


def parseComments(url):
    j = pull(url)
    if j is None:
        return
    n = len(j[1]['data']['children'])
    for i in range(n):
        child = j[1]['data']['children'][i]
        parseComment(child)


def parseSub():
    url = '/r/%s.json' % sub
    j = pull(url)
    key = j['data']['after']
    for i in range(0, POSTS_PER_PAGE):  # 25 posts per page
        link = j['data']['children'][i]['data']['permalink']
        url = '%s.json' % link
        parseComments(url)
    return key


def finish(out):
    print 'Finishing up!'
    fd = open(out, 'w')
    for c in comments:
        try:
            fd.write(str(c))
            fd.write('\n')
        except UnicodeEncodeError:
            pass
    fd.close()


if __name__ == "__main__":
    key = parseSub()
    finish(outFile)
    conn.close()
