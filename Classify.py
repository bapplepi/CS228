import numpy as np
import pickle
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

train2 = pickle.load(open("train2.p", "rb"))
train3 = pickle.load(open("train3.p", "rb"))
test2 = pickle.load(open("test2.p", "rb"))
test3 = pickle.load(open("test3.p", "rb"))
train2 = ReduceData(train2)
train3 = ReduceData(train3)
test2 = ReduceData(test2)
test3 = ReduceData(test3)


def ReshapeData(set1, set2):
	x = np.zeros((2000,5*4*6),dtype='i')
	y = np.zeros(2000, dtype='i')
	for row in range(0,1000):
		col = 0
		for j in range(0,5):
			for k in range(0,2):
				for m in range(0,3):
					x[row,col] = set1[j,k,m,row]
					x[row+1000,col] = set2[j,k,m,row]
					y[row] = 2
					y[row+1000] = 3
					col = col + 1

	return (x, y)

trainX, trainY = ReshapeData(train2, train3)
testX, testY = ReshapeData(test2, test3)
knn.Fit(trainX,trainY)

correct = 0

for row in range(0,2000):
	itemClass = int(testY[row])
	prediction = knn.Predict( testX[row,:] )
	if(prediction == itemClass):
		correct = correct + 1

print trainX
print trainX.shape
print trainY
print trainY.shape
print 'num correct = ' + str(correct)
print 'percentage correct = ' + str(float(correct)/2000.0)