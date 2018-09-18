from Vectorizer.Vectorizer import Vectorizer

response = {
    "returncode":0,
    "error":"",
    "content":{}
    }

def modify(extractor,directory):
    global response

    vectorizer = Vectorizer(extractor, directory)

    # pragma = source.offload(vector["line"], "parallel for", 4, "map")
    # pragma.modifyClause("num_threads", 5)
    return response
