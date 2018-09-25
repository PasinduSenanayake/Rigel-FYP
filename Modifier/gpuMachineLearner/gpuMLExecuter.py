import os
import numpy as np
import pandas as pd
from sklearn import ensemble
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import SelectFromModel
import dbManager,logger

fileLocation = os.path.dirname(os.path.realpath(__file__))+"/"


def dataPreProcessor(filePath):
    if (os.path.isfile(fileLocation+'mlTemp.csv')):
        os.remove(fileLocation+'mlTemp.csv')
    dataSet = pd.read_csv(filePath+"gpuvscpu.csv")
    dataSet['coldref fraction'] = dataSet['coldref']/(dataSet['instructionCount']*dataSet['memops'])
    dataSet['resuseDist2 fraction'] = dataSet['reuseDist2']/(dataSet['instructionCount']*dataSet['memops'])
    dataSet.to_csv(fileLocation+'mlTemp.csv', index=False)
    return dataSet['dataSet']



def processMLData():
    data1 = pd.read_csv(fileLocation+"trainingData/group1.csv")
    df1 = pd.DataFrame(data1) # Converting data to Panda DataFrame
    data2 = pd.read_csv(fileLocation+"trainingData/group2.csv")
    df2 = pd.DataFrame(data2) # Converting data to Panda DataFrame
    data3 = pd.read_csv(fileLocation+"trainingData/group3.csv")
    df3 = pd.DataFrame(data3) # Converting data to Panda DataFrame
    data4 = pd.read_csv(fileLocation+"trainingData/group4.csv")
    df4 = pd.DataFrame(data4) # Converting data to Panda DataFrame
    data5 = pd.read_csv(fileLocation+"trainingData/group5.csv")
    df5 = pd.DataFrame(data5) # Converting data to Panda DataFrame


    X_1 = df1

    Weighted_X1 = X_1[["ilp32",'ilp256','ilp2048','ilp65536','memops','ctrlops','intops','flops','coldref fraction','resuseDist2 fraction','sfp','dfp','noconflict','broadCast','coalesced',
     'shMemBw',
     'gMemBw',
     'blocks',
     'pages',
     'lipRate',
     'mulf',
     'divf',
     'specialFn',
     'lbdiv16',
     'lbdiv32',
     'lbdiv64',
     'lbdiv128',
     'lbdiv256',
     'lbdiv512',
     'lbdiv1024']].multiply(df1["instructionCount"], axis="index")

    X_2 = df2

    Weighted_X2 = X_2[["ilp32",'ilp256','ilp2048','ilp65536','memops','ctrlops','intops','flops','coldref fraction','resuseDist2 fraction','sfp','dfp','noconflict','broadCast','coalesced',
     'shMemBw',
     'gMemBw',
     'blocks',
     'pages',
     'lipRate',
     'mulf',
     'divf',
     'specialFn',
     'lbdiv16',
     'lbdiv32',
     'lbdiv64',
     'lbdiv128',
     'lbdiv256',
     'lbdiv512',
     'lbdiv1024']].multiply(df2["instructionCount"], axis="index")

    X_3 = df3

    Weighted_X3 = X_3[["ilp32",'ilp256','ilp2048','ilp65536','memops','ctrlops','intops','flops','coldref fraction','resuseDist2 fraction','sfp','dfp','noconflict','broadCast','coalesced',
     'shMemBw',
     'gMemBw',
     'blocks',
     'pages',
     'lipRate',
     'mulf',
     'divf',
     'specialFn',
     'lbdiv16',
     'lbdiv32',
     'lbdiv64',
     'lbdiv128',
     'lbdiv256',
     'lbdiv512',
     'lbdiv1024']].multiply(df3["instructionCount"], axis="index")

    X_4 = df4

    Weighted_X4 = X_4[["ilp32",'ilp256','ilp2048','ilp65536','memops','ctrlops','intops','flops','coldref fraction','resuseDist2 fraction','sfp','dfp','noconflict','broadCast','coalesced',
     'shMemBw',
     'gMemBw',
     'blocks',
     'pages',
     'lipRate',
     'mulf',
     'divf',
     'specialFn',
     'lbdiv16',
     'lbdiv32',
     'lbdiv64',
     'lbdiv128',
     'lbdiv256',
     'lbdiv512',
     'lbdiv1024']].multiply(df4["instructionCount"], axis="index")

    X_5 = df5

    Weighted_X5 = X_5[["ilp32",'ilp256','ilp2048','ilp65536','memops','ctrlops','intops','flops','coldref fraction','resuseDist2 fraction','sfp','dfp','noconflict','broadCast','coalesced',
     'shMemBw',
     'gMemBw',
     'blocks',
     'pages',
     'lipRate',
     'mulf',
     'divf',
     'specialFn',
     'lbdiv16',
     'lbdiv32',
     'lbdiv64',
     'lbdiv128',
     'lbdiv256',
     'lbdiv512',
     'lbdiv1024']].multiply(df5["instructionCount"], axis="index")

    Y_train1 = df1['Class']
    Y_train2 = df2['Class']
    Y_train3 = df3['Class']
    Y_train4 = df4['Class']
    Y_train5 = df5['Class']

    selector1 = SelectKBest(chi2, k=25)
    X_new1 =selector1.fit_transform(Weighted_X1, Y_train1)
    idxs_selected1 = selector1.get_support(indices=True)
    selector2 = SelectKBest(chi2, k=25)
    X_new2 =selector2.fit_transform(Weighted_X2, Y_train2)
    idxs_selected2 = selector2.get_support(indices=True)
    selector3 = SelectKBest(chi2, k=25)
    X_new3 =selector3.fit_transform(Weighted_X3, Y_train3)
    idxs_selected3 = selector3.get_support(indices=True)
    selector4 = SelectKBest(chi2, k=25)
    X_new4 =selector4.fit_transform(Weighted_X4, Y_train4)
    idxs_selected4 = selector4.get_support(indices=True)
    selector5 = SelectKBest(chi2, k=25)
    X_new5 =selector5.fit_transform(Weighted_X5, Y_train5)
    idxs_selected5 = selector5.get_support(indices=True)

    data_test = pd.read_csv(fileLocation+'mlTemp.csv')
    df_test = pd.DataFrame(data_test) # Converting data to Panda DataFrame
    #df_test = df_test.sample(20)
    #df_test.head() #gives statistics about the columns of the dataframe

    X_test = df_test
    Weighted_XTest = X_test[["ilp32",'ilp256','ilp2048','ilp65536','memops','ctrlops','intops','flops',
     'coldref fraction',
     'resuseDist2 fraction',
     'sfp',
     'dfp',
     'noconflict',
     'broadCast',
     'coalesced',
     'shMemBw',
     'gMemBw',
     'blocks',
     'pages',
     'lipRate',
     'mulf',
     'divf',
     'specialFn',
     'lbdiv16',

     'lbdiv32',
     'lbdiv64',
     'lbdiv128',
     'lbdiv256',
     'lbdiv512',
     'lbdiv1024']].multiply(df_test["instructionCount"], axis="index")
    baggingClassifier1 = ensemble.BaggingClassifier(n_estimators=11,bootstrap_features=True,n_jobs=-1,random_state=0)
    baggingClassifier1.fit(X_new1,Y_train1)
    baggingClassifier2 = ensemble.BaggingClassifier(n_estimators=11,bootstrap_features=True,n_jobs=-1,random_state=0)
    baggingClassifier2.fit(X_new2,Y_train2)
    baggingClassifier3 = ensemble.BaggingClassifier(n_estimators=11,bootstrap_features=True,n_jobs=-1,random_state=0)
    baggingClassifier3.fit(X_new3,Y_train3)
    baggingClassifier4 = ensemble.BaggingClassifier(n_estimators=11,bootstrap_features=True,n_jobs=-1,random_state=0)
    baggingClassifier4.fit(X_new4,Y_train4)
    baggingClassifier5 = ensemble.BaggingClassifier(n_estimators=11,bootstrap_features=True,n_jobs=-1,random_state=0)
    baggingClassifier5.fit(X_new5,Y_train5)

    prediction1 = baggingClassifier1.predict(Weighted_XTest[Weighted_XTest.columns[idxs_selected1]])
    # print (prediction1)
    prediction2 = baggingClassifier2.predict(Weighted_XTest[Weighted_XTest.columns[idxs_selected2]])
    # print (prediction2)
    prediction3 = baggingClassifier3.predict(Weighted_XTest[Weighted_XTest.columns[idxs_selected3]])
    # print (prediction3)
    prediction4 = baggingClassifier4.predict(Weighted_XTest[Weighted_XTest.columns[idxs_selected4]])
    # print (prediction4)
    prediction5 = baggingClassifier5.predict(Weighted_XTest[Weighted_XTest.columns[idxs_selected5]])
    # print (prediction5)
    total = prediction1+prediction2+prediction3+prediction4+prediction5
    # print (total)
    totalNew = []
    for value in total:
        if value > 2:
            totalNew.append('Y')
        else:
            totalNew.append('N')
    # print (np.array(totalNew))
    # print (np.array(X_test['Class']))
    os.remove(fileLocation+'mlTemp.csv')
    return np.array(totalNew)

def mlModelExecutor(filePath):
    dataSection = dataPreProcessor(filePath+"/_profiling/")
    resultsSet = processMLData()
    loopData = dbManager.read('loopSections')
    summaryLoopData = dbManager.read('summaryLoops')
    subSections=[]
    for loopSection in dataSection:
        dataSource = {'fileName':'', 'loopSegementStartLine':'','loopSegementEndLine':''}
        dataSource['fileName'] = loopSection.split(' ')[1].split(':')[0]
        loopSubSection =  loopSection.split(' ')[1].split(':')[1].split('[')[1].split('-')
        dataSource['loopSegementStartLine'] = loopSubSection[0]
        dataSource['loopSegementEndLine'] = loopSubSection[1].split(']')[0]
        subSections.append(dataSource)

    resultLaunch =0
    for loopMatchSection in subSections:
        for dataItem in loopData:
            if(dataItem["startLine"]== loopMatchSection['loopSegementStartLine'] and dataItem["endLine"]== loopMatchSection['loopSegementEndLine'] and dataItem["fileName"]== loopMatchSection['fileName']):
                if(resultsSet[resultLaunch]=='Y'):
                    dataItem["optimizeMethod"] ='GPU'
                    for summaryLoopDataItem in summaryLoopData:
                        if(summaryLoopDataItem["startLine"]== loopMatchSection['loopSegementStartLine'] and summaryLoopDataItem["endLine"]== loopMatchSection['loopSegementEndLine'] and summaryLoopDataItem["fileName"]== loopMatchSection['fileName']):
                            summaryLoopDataItem["optimizeMethod"] ='GPU'
                            break
                resultLaunch= resultLaunch+1
                break
    dbManager.overWrite('loopSections',loopData)
    dbManager.overWrite('summaryLoops',summaryLoopData)
    return True
