import json
import time
import sys
import httplib

TIME_BETWEEN_GETS = 10
POSTS_PER_PAGE = 1
comments = []
sub = sys.argv[1]
outFile = sys.argv[2]
hdr = { 'User-Agent' : 'chainsaw flailing comment grabber' }

# pulls a web page and returns it as a json object
def get(url):
    conn = httplib.HTTPConnection('www.reddit.com')
    conn.request('GET', url, headers=hdr)
    txt = conn.getresponse().read()
    print 'download is successful'
    conn.close()
    time.sleep(TIME_BETWEEN_GETS)
    return json.loads(txt)

class comment:
    
    def __init__(self, s, u, d, b):
        self.sub = sub
        self.score = s
        self.down = d
        self.up = u
        b = ' '.join(b.split())
        self.body = b
    
    def __str__(self):
        return "%s\t%s\t%s\t%s\t%s" % (self.sub, self.score, self.up, self.down, self.body)

def parseComment(child):
    score = child['data']['score']
    ups = child['data']['ups']
    downs = child['data']['downs']
    body = child['data']['body']
    comments.append(comment(score, ups, downs, body))
    if child['data']['replies'] != '':
        n = len(child['data']['replies']['data']['children'])
        for i in range(n):
            grand = child['data']['replies']['data']['children'][i]
            parseComment(grand)


def parseComments(url):
    j = get(url)
    n = len(j[1]['data']['children'])
    for i in range(n):
        child = j[1]['data']['children'][i]
        parseComment(child)



def parseSub():
    url = '/r/%s.json' % sub
    j = get(url)
    key = j['data']['after']
    for i in range(POSTS_PER_PAGE): # 25 posts per page
        print 'looking at a new post'
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
    fd.close


if __name__ == "__main__":
    parseSub()
    finish(outFile)
