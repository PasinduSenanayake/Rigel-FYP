
import os,logger,dbManager,json,csv
import pandas as pd


def metaDataExtractor():
    if "metadata" in os.listdir(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/Sandbox"):
        logger.loggerInfo("Meta data insertion Initiated")
        metaDataSet =[]
        if os.path.isfile(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/Sandbox/metadata/checksum.json"):
            with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/Sandbox/metadata/checksum.json") as f:
                metaDataInfo = json.load(f)
                for fileInfo in metaDataInfo['mapper']:
                    if not (metaDataInfo['mapper'][fileInfo]['checksum'] == None):
                        validData = {'fileName':fileInfo,'checksumValue':metaDataInfo['mapper'][fileInfo]['checksum'],'csv':None}
                        if not (metaDataInfo['mapper'][fileInfo]['csv'] == None):
                            if os.path.isfile(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/Sandbox/metadata/"+metaDataInfo['mapper'][fileInfo]['csv']):
                                 filePathCsv = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/Sandbox/metadata/"+metaDataInfo['mapper'][fileInfo]['csv']
                                 validData['csv'] = pd.Series.from_csv(filePathCsv, header=None).to_dict()
                        metaDataSet.append(validData)

                    else:
                        continue

            dbManager.write('metaDataExists',True)
            dbManager.write('metaData',metaDataSet)
            logger.loggerSuccess("Meta data insertion Completed")
        else:
            dbManager.write('metaDataExists',False)
            logger.loggerInfo("No checksum.json found. Meta data insertion skipped")
    else:
        dbManager.write('metaDataExists',False)
        logger.loggerInfo("No Meta data found. Meta data insertion skipped")
