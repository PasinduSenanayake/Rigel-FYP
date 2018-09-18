import threading
import os

def f(name):
    print 'helloBob'

def g(name):
    print 'helloAliceob'

if __name__ == '__main__':
    name = "bob"
    t1 = threading.Thread(target=f,args=(name,))
    t2 = threading.Thread(target=g,args=(name,))
    t3 = threading.Thread(target=f,args=(name,))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()
