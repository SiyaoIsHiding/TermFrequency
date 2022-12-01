import re, sys, collections, os
import threading

stopwords = set(open('stop_words').read().split(','))
result = collections.Counter({})
workers = []
paths = []

for dirpath, dnames, fnames in os.walk("./texts/"):
    for f in fnames:
        if f.endswith(".txt"):
            p = os.path.join(dirpath, f)
            paths.append(p)
            

barrier = threading.Barrier(len(paths)+1)

class Worker(threading.Thread):
    """
    path : str
    result : collections.Counter
    """
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.path = path
    def run(self):
        try:
            words = re.findall('\w{3,}',open(self.path).read().lower())
            self.result = collections.Counter(w for w in words if w not in stopwords)
            barrier.wait()
        except:
            print("Error analyzing "+self.path)

try:
    for p in paths:
        w = Worker(p)
        workers.append(w)
        w.start()

    barrier.wait()
except:
    print("Error in multi-threading and barrier")
result = collections.Counter({})
for w in workers:
    result = result + w.result

for (w, c) in result.most_common(25):
    print (w, '-', c)
