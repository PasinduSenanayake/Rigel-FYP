import os
import numpy as np
import pandas as pd
from sklearn import ensemble
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import SelectFromModel
import dbManager,logger

fileLocation = os.path.dirname(os.path.realpath(__file__))+"/"


def dataPreProcessor(filePath):
    if (os.path.isfile(fileLocation+'mlTemp.csv')):
        os.remove(fileLocation+'mlTemp.csv')
    dataSet = pd.read_csv(filePath+"out.csv")
    dataSet.to_csv(fileLocation+'mlTemp.csv', index=False)
    return dataSet



def processMLData():
    data1 = pd.read_csv(fileLocation+"trainingData/Dataset.csv")
    x_train_total = pd.DataFrame(data1) # Converting data to Panda DataFrame

    output = ['VECTORIZABLE']
    featureSet1 = [ 'CPI Rate', 'CPU_CLK_UNHALTED.THREAD',
                   'CPU_CLK_UNHALTED.REF_TSC', 'INST_RETIRED.ANY', 'INST_RETIRED.PREC_DIST',
                   'BR_MISP_RETIRED.ALL_BRANCHES_PS']
    featureSet2 = []
    featureSet3 = ['BACLEARS.ANY',
                   'CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE', 'CPU_CLK_UNHALTED.REF_XCLK', 'CPU_CLK_UNHALTED.THREAD_P',
                   'DSB2MITE_SWITCHES.PENALTY_CYCLES']
    featureSet4 = ['DTLB_LOAD_MISSES.STLB_HIT', 'DTLB_STORE_MISSES.STLB_HIT',
                   ]
    featureSet5 = ['IDQ.ALL_DSB_CYCLES_4_UOPS',
                   'IDQ.ALL_DSB_CYCLES_ANY_UOPS', 'IDQ.ALL_MITE_CYCLES_4_UOPS', 'IDQ.ALL_MITE_CYCLES_ANY_UOPS',
                   'IDQ.DSB_UOPS', 'IDQ.MITE_UOPS', 'IDQ.MS_SWITCHES', 'IDQ.MS_UOPS']
    featureSet6 = ['IDQ_UOPS_NOT_DELIVERED.CORE', 'IDQ_UOPS_NOT_DELIVERED.CYCLES_0_UOPS_DELIV.CORE',
                   'INT_MISC.RECOVERY_CYCLES',
                   'L1D_PEND_MISS.PENDING', 'L2_RQSTS.RFO_HIT', 'LD_BLOCKS.NO_SR', 'LD_BLOCKS.STORE_FORWARD',
                   'LD_BLOCKS_PARTIAL.ADDRESS_ALIAS']
    featureSet7 = ['MACHINE_CLEARS.COUNT', 'OFFCORE_REQUESTS_BUFFER.SQ_FULL',

                   'OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DATA_RD',
                   'OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DEMAND_RFO', 'RS_EVENTS.EMPTY_CYCLES',
                   'RS_EVENTS.EMPTY_END', 'UOPS_DISPATCHED_PORT.PORT_0', 'UOPS_DISPATCHED_PORT.PORT_1',
                   'UOPS_DISPATCHED_PORT.PORT_2']
    featureSet8 = ['UOPS_DISPATCHED_PORT.PORT_3', 'UOPS_DISPATCHED_PORT.PORT_4', 'UOPS_DISPATCHED_PORT.PORT_5',
                   'UOPS_DISPATCHED_PORT.PORT_6', 'UOPS_DISPATCHED_PORT.PORT_7',
                   'UOPS_ISSUED.ANY',
                   'UOPS_RETIRED.RETIRE_SLOTS']

    allFeatures = featureSet1 + featureSet2 + featureSet3 + featureSet4 + featureSet5 + featureSet6 + featureSet7 + featureSet8
    x = x_train_total[allFeatures]
    weightedX = x[allFeatures].multiply(x["CPU_CLK_UNHALTED.THREAD"], axis="index")
    y_train = x_train_total[output]


    selector1 = SelectKBest(chi2, k=25)
    X_new1 =selector1.fit_transform(weightedX, y_train)
    idxs_selected1 = selector1.get_support(indices=True)

    data_test = pd.read_csv(fileLocation+'mlTemp.csv')
    df_test = pd.DataFrame(data_test) # Converting data to Panda DataFrame
    #df_test = df_test.sample(20)
    #df_test.head() #gives statistics about the columns of the dataframe

    X_test = df_test
    Weighted_XTest = X_test[allFeatures].multiply(x["CPU_CLK_UNHALTED.THREAD"], axis="index")
    Weighted_XTest = Weighted_XTest.dropna()

    #create model
    baggingClassifier1 = ensemble.BaggingClassifier(n_estimators=11,bootstrap_features=True,n_jobs=-1,random_state=0)
    baggingClassifier1.fit(X_new1,y_train)

    # print(Weighted_XTest)
    prediction = baggingClassifier1.predict(Weighted_XTest[Weighted_XTest.columns[idxs_selected1]])
    # lrmodel = LogisticRegression()
    # lrmodel.fit(X_new1, y_train)
    # prediction = lrmodel.predict(Weighted_XTest[Weighted_XTest.columns[idxs_selected1]])
    print (prediction)

    # total = prediction1
    # # print (total)
    # totalNew = []
    # for value in total:
    #     if value > 2:
    #         totalNew.append('Y')
    #     else:
    #         totalNew.append('N')
    # # print (np.array(totalNew))
    # # print (np.array(X_test['Class']))
    # os.remove(fileLocation+'mlTemp.csv')
    # return np.array(totalNew)

def vecMlModelExecutor(filePath):
    dataSection = dataPreProcessor(filePath+"/_vector_profiling/")
    resultsSet = processMLData()
    loopData = dbManager.read('loopSections')
    # subSections=[]
    # for loopSection in dataSection:
    #     dataSource = {'fileName':'', 'loopSegementStartLine':'','loopSegementEndLine':''}
    #     dataSource['fileName'] = loopSection.split(' ')[1].split(':')[0]
    #     loopSubSection =  loopSection.split(' ')[1].split(':')[1].split('[')[1].split('-')
    #     dataSource['loopSegementStartLine'] = loopSubSection[0]
    #     dataSource['loopSegementEndLine'] = loopSubSection[1].split(']')[0]
    #     subSections.append(dataSource)
    #
    # resultLaunch =0
    # for loopMatchSection in subSections:
    #     for dataItem in loopData:
    #         if(dataItem["startLine"]== loopMatchSection['loopSegementStartLine'] and dataItem["endLine"]== loopMatchSection['loopSegementEndLine'] and dataItem["fileName"]== loopMatchSection['fileName']):
    #             if(resultsSet[resultLaunch]=='Y'):
    #                 dataItem["optimizeMethod"] ='GPU'
    #             resultLaunch= resultLaunch+1
    #             break
    # dbManager.overWrite('loopSections',loopData)
    return True
