import sys
sys.path.insert(0, '..')

import numpy as np
import pickle
import os
from knn import KNN


knn = KNN()
knn.Use_K_Of(15)

def CenterData(X):
	allXCoordinates = X[:,:,0,:]
	meanValue = allXCoordinates.mean()
	X[:,:,0,:] = allXCoordinates - meanValue

	allYCoordinates = X[:,:,1,:]
	meanValue = allYCoordinates.mean()
	X[:,:,1,:] = allYCoordinates - meanValue

	allZCoordinates = X[:,:,2,:]
	meanValue = allZCoordinates.mean()
	X[:,:,2,:] = allZCoordinates - meanValue

	return X


def ReduceData(X):
	X = np.delete(X,1,1)
	X = np.delete(X,1,1)
	X = np.delete(X,0,2)
	X = np.delete(X,0,2)
	X = np.delete(X,0,2)
	X = CenterData(X)
	return X

trainingData = []
testingData = []
dataClasses = []

for dirName, subdirList, fileList in os.walk('./userData'):
	for dataFile in fileList:
		isTrain = dataFile.find('train')
		if isTrain != -1:
			#print dataFile
			trainX = pickle.load(open('userData/' + str(dataFile), 'rb'))
			tokens = dataFile.split('_')
			if(len(tokens) == 3):
				testX = pickle.load(open('userData/' + tokens[0] + '_' + tokens[1] + '_test' + tokens[2][len(tokens[2])-3:], 'rb'))
			else:
				testX = pickle.load(open('userData/' + tokens[0] + '_test' + tokens[1][len(tokens[1])-3:], 'rb'))
			trainX = ReduceData(trainX)
			testX = ReduceData(testX)
			#print trainX.shape
			trainingData.append(trainX)
			testingData.append(testX)
			if(len(tokens) == 3):
				dataClasses.append(int(tokens[2][len(tokens[2])-3]))
			else:
				dataClasses.append(int(tokens[1][len(tokens[1])-3]))

def ReshapeData(trainingData, dataClasses):
	x = np.zeros((1000*len(trainingData),5*2*3),dtype='i')
	y = np.zeros(1000*len(trainingData), dtype='i')

	for i in range(0,len(trainingData)):
		print "Added data set #" + str(i) + " for ASL digit " + str(dataClasses[i])
		dataSet = trainingData[i]
		for row in range(0,1000):
			col = 0
			for j in range(0,5):
				for k in range(0,2):
					for m in range(0,3):
						x[row+1000*i,col] = dataSet[j,k,m,row]
						y[row+1000*i] = dataClasses[i]
						col = col + 1

	return (x, y)

trainX, trainY = ReshapeData(trainingData, dataClasses)
testX, testY = ReshapeData(testingData, dataClasses)
knn.Fit(trainX,trainY)

correct = 0
#correct = np.zeros(10)

print "data points: " + str(len(testY))
for row in range(0,len(testY),100):
	itemClass = int(testY[row])
	prediction = knn.Predict( testX[row,:] )
	if(prediction == itemClass):
		#print "correct = " + str(correct) + "    row = " + str(row) + "   class = " + str(itemClass)
		#correct[itemClass] = correct[itemClass] + 1
		correct = correct + 1

print trainX
print trainX.shape
print trainY
print trainY.shape
print 'num correct = ' + str(correct)
print 'percentage correct = ' + str(float(correct)/840.0)
pickle.dump(knn, open('userData/classifier.p','wb'))