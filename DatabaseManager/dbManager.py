import pickledb
import os

def write(key,value):
    print "hiii"
    db = pickledb.load(os.path.dirname(os.path.realpath(__file__))+'/rigel.db', True)
    if(db.get(key)==None):
        db.set(key, value)
    db.dump()

def overWrite(key,value):
    db = pickledb.load(os.path.dirname(os.path.realpath(__file__))+'/rigel.db', False)
    db.set(key, value)
    db.dump()

def read(key):
    db = pickledb.load(os.path.dirname(os.path.realpath(__file__))+'/rigel.db', True)
    return db.get(key)
    db.dump()

def delete(key):
    db = pickledb.load(os.path.dirname(os.path.realpath(__file__))+'/rigel.db', False)
    db.rem(key)
    db.dump()
