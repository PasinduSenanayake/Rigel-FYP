from Vectorizer.Vectorizer import Vectorizer

response = {
    "returncode":0,
    "error":"",
    "content":{}
    }

def modify(extractor,directory):
    global response
    vectorizer = Vectorizer(extractor, directory)
    return response
