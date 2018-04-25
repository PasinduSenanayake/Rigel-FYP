import ompp

from Identifier import systemIdentifier

response = {
    "returncode":0,
    "error":"",
    "content":{}
}

def nestedloopAnalysis(filePath, compTimeArguments, runTimeArguments):
    try:
      if not (filePath == None):
          basicProfile = ompp.getBasicProfile(filePath, compTimeArguments=compTimeArguments,
                                                       runTimeArguments=runTimeArguments)
          #print basicProfile['content'][56]
          #print basicProfile['content'][53]
          threadsUsed= int(str(basicProfile['content'][53]).split(",")[1])
          systemIdentifier.__systemInformationIdentifier()
          systhreads=int(systemIdentifier.cpu_info_list["num_cores"])*int(systemIdentifier.cpu_info_list["threads_per_core"])
          if systhreads > threadsUsed:
              print "nested parallelism recommended"
          else:
              print "nested parallelism not recommended"
    except Exception as e:
      response['error'] = e
      response['content'] = {}
      response['returncode'] = 0
    return response
