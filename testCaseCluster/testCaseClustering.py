import sys
import csv

FINALClusters = list()
MINSIMVALUE = 0
STOPCLUSTERINGSIMVALUE = 0.01
DISTFUNCVALUE = 0.5
TESTCASENAMEDict = dict() #testcase[id] = name

class AlgClass:
    distFunc = ""
    mergeFunc = ""
    K = 0 #iteration number
    simM = list()
    pre = "TS"   #testcase clustering
    feature = ""

    def __init__(self):
        print "init: do nothing"

    def setDistFunc(self, func):
        self.distFunc = func

    def setMergeFunc(self, func):
        self.mergeFunc = func

    def setK(self, k):
        self.K = k

    def setFeature(self, feature):
        self.feature = feature

    #simM may be not a N*N, may be M*N
    def setSimM(self, M):
        N = len(M)    #row
        m = len(M[0]) #col
        for index in range(0, N):
            tmpList = [0] * m #generat a list whole len = N
            self.simM.append(tmpList)
        for i in range(0, N):
            for j in range(0, m):
                self.simM[i][j] = M[i][j]


def readCSV(fileName):
    resList = list()
    with open(fileName, "rb") as fp:
        reader = csv.reader(fp, delimiter = ',')
        for eachLine in reader:
            resList.append(eachLine)
    return resList

def writeCSV(fileName,listlist):
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        for eachList in listlist:
            writer.writerow(eachList)

def isLess(floatNum, threshold):
    if floatNum - threshold <= 0.001:
        return True
    else:
        return False

def isEqual(floatNum1, floatNum2):
    if abs(floatNum1 - floatNum2) <= 0.0001:
        return True
    else:
        return False


#delete the first column, that is testcase ID
def delFirstCol(fv):
    newFv = list()
    testCaseID = 0
    for eachList in fv:
        TESTCASENAMEDict[testCaseID] = eachList[0]
        testCaseID += 1
        del eachList[0]
        for index in range(0, len(eachList)):
            eachList[index] = int(eachList[index])
        newFv.append(eachList)
    return newFv


#find the differ between two feature vector
def WCAFindDiffer(vector_i, vector_j, thr):
    bothIndex = list()
    onlyBIndex = list()
    onlyAIndex = list()
    bothNotIndex = list()
    bothVal = list()
    onlyBVal = list()
    onlyAVal = list()
    bothNotVal = list()

    n = len(vector_i) #  len(vector_i) = len(vector_j)
    #notice: elment of vector is float, how to compare float with 0
    for index in range(0, n): #list=[0,1,..., n-1]
        if not isLess(vector_i[index], thr)  and  not isLess(vector_j[index], thr):
            bothIndex.append(index)
            bothVal.append(vector_i[index] + vector_j[index])
        elif isLess(vector_i[index], thr) and not isLess(vector_j[index], thr):
            onlyBIndex.append(index)
            onlyBVal.append(vector_j[index])
        elif not isLess(vector_i[index], thr) and isLess(vector_j[index], thr):
            onlyAIndex.append(index)
            onlyAVal.append(vector_i[index])
	elif isLess(vector_i[index], thr) and  isLess(vector_j[index], thr):
            bothNotIndex.append(index)
            bothNotVal.append(vector_i[index])

    return bothIndex, onlyAIndex, onlyBIndex, bothNotIndex, bothVal, onlyAVal, onlyBVal, bothNotVal


#for this distance, the more, the marrier
def WCACalDistClass_ij(i, j, class1Fv, class2Fv, distFunc, thr):
    if i == j:
        return 0

    if len(class1Fv) != len(class2Fv):
        print "this two feature vector donnot have same len\n"
        return


    [bothIndex, onlyAIndex, onlyBIndex, bothNotIndex, bothVal, onlyAVal, onlyBVal, bothNotVal] = WCAFindDiffer(class1Fv, class2Fv, thr ) #aIndex is the index array
    if distFunc == "jm":
        fenzi = len(bothIndex)
        fenmu = len(bothIndex) + len(onlyAIndex) + len(onlyBIndex)
    elif distFunc == "uem":
        fenzi = 0.5 * sum(bothVal)
        fenmu = 0.5 * sum(bothVal) + len(onlyAIndex) + len(onlyBIndex)   # dist is more, the similarity is stronger
    elif distFunc == "uemnm":
        fenzi = 0.5 * sum(bothVal)
        fenmu = 0.5 * sum(bothVal) + 2 * len(onlyAIndex) + 2 * len(onlyBIndex) + len(bothIndex) + len(bothNotIndex)

    if not isEqual(fenmu, 0):
        return fenzi / float(fenmu)
    else:
        return 0



#generate TsSimM listlist,   duichen juzhen
def WCACalTsSim(fv, distFunc):
    N = len(fv)
    tsSimM = list()

    #initialize tsSimM
    for index in range(0, N):
        tmpList = [MINSIMVALUE] * N #generat a list whole len = N
        tsSimM.append(tmpList)

    for i in range(0, N):
        for j in range(0, N):
            if i != j:
                tsSimM[i][j] = WCACalDistClass_ij(i, j, fv[i], fv[j], distFunc,  thr = DISTFUNCVALUE)

    return tsSimM




#compute the distance/similarity between two cluster
#cluster_i =[node1, node2, node3]; clustr_j =[];
def WCACalDistCluster_ij(cluster_i, cluster_j):
    distList = list()
    #print cluster_i, cluster_j
    for eachNode_i in cluster_i:
        for eachNode_j in cluster_j:
            #print eachNode_i, eachNode_j, structSimM[eachNode_i][eachNode_j]
            distList.append(oneAlg.simM[eachNode_i][eachNode_j])

    if oneAlg.mergeFunc == "MAX_SINGLE": # choose the maxNodeDistance as cluster distance
        return max(distList)
    elif oneAlg.mergeFunc == "MIN_SINGLE": # choose the minNodeDistance as cluster distance
        return min(distList)
    elif oneAlg.mergeFunc == "AVG": # choose the avg nodeNodeDistance as cluster distance
        return sum(distList) / float(len(distList))
    else:
        print "wrong merge function!!!!!!!!!!"

#choose most similar clusters to merge
def WCAChooseMostSim(N):
    tmpList = list() # all cluster_pair distance

    for i in range(0, N):
        for j in range(0, N):
            if i != j:
                simVal = WCACalDistCluster_ij(FINALClusters[i], FINALClusters[j])
                #print i, j, clusters[i], clusters[j], simVal
                tmpList.append([i,j, simVal])

    #sort tmpList from big to small
    sortedList = sorted(tmpList, key=lambda x:x[2], reverse=True)

    maxValue = sortedList[0][2]
    tmpIndex = 0
    for each in sortedList:
        if not isEqual(each[2], maxValue):
            break
        else:
            tmpIndex += 1
    #print tmpIndex

    #choose from 0 to tmpIndex-1 randomly
    import random
    rd = random.randint(0, tmpIndex-1)
    merge_i = sortedList[rd][0]
    merge_j = sortedList[rd][1]
    mergeSimVal = sortedList[rd][2]

    return merge_i, merge_j, mergeSimVal


#run clustering WCA
def WCAClustering(fv):
    #compute the tsSimM (a duichen juzhen)
    tsSimM = WCACalTsSim(fv, oneAlg.distFunc)
    oneAlg.setSimM(tsSimM)

    iterk = 1
    origN = len(FINALClusters)
    N = len(FINALClusters)
    merge_simVal = 1
    while N > oneAlg.K and  merge_simVal >=  STOPCLUSTERINGSIMVALUE:
        merge_i = -1
        merge_j = -1

        (merge_i, merge_j, merge_simVal) = WCAChooseMostSim(N)

        if merge_i == -1 and merge_j == -1:
            print merge_i, merge_j, "no merge"
            break
        else:
            #merge the cluster_i and cluster_j, and update FINALClusters
            print FINALClusters[merge_i], " and ",  FINALClusters[merge_j], " simVal=", merge_simVal
            FINALClusters[merge_i].extend(FINALClusters[merge_j])
            del FINALClusters[merge_j]

            if N-1 <= int(origN):
                outfileName = oneAlg.pre + '_' + oneAlg.feature + '_' + oneAlg.distFunc + '_' + oneAlg.mergeFunc + '_' + str(N-1) + '.csv'
                print "clustering result file: ", outfileName
                printClustering(outfileName)
        iterk = iterk + 1
        N = N - 1

    print "clustering end...."


def printClustering(fileName):
    num = len(FINALClusters)
    resList = list()
    #print TESTCASENAMEDict
    for index in range(0, num):
        clusterID = index
        for eachTsID in FINALClusters[clusterID]:
            resList.append([clusterID, eachTsID, TESTCASENAMEDict[eachTsID]])
    writeCSV(fileName, resList)


def initCluster(N):
    for i in range(0, N):
        FINALClusters.append([i])

oneAlg = AlgClass()
#use testcase feature to do clustering
#python pro.py   tsfv.csv   distFunc=jm, uem, uemnm       mergeFunc= MIN_SINGLE, MAX_SINGLE, AVG       K=iterNum   feature=TS
if __name__ == "__main__":
    featureFileName = sys.argv[1]    #testcase feature maxtrix filename
    distFunc = sys.argv[2]           #similaroty distance metric
    mergeFunc = sys.argv[3]          #how to merge the two similar custers to be a new cluster
    K = int(sys.argv[4])
    feature = sys.argv[5]  #Test case
    oneAlg.setDistFunc(distFunc)
    oneAlg.setMergeFunc(mergeFunc)
    oneAlg.setK(K)
    oneAlg.setFeature(feature)

    #init fecture vector
    tsFv = readCSV(featureFileName)
    newTsFv = delFirstCol(tsFv)
    #init clusters
    tsCount = len(newTsFv)
    initCluster(tsCount)
    #clustering
    WCAClustering(newTsFv)