import matplotlib.pyplot as plt
from knn import KNN
import numpy as np



knn = KNN()
knn.Load_Dataset('iris.csv')

colors = np.zeros((3,3),dtype='f')
colors[0,:] = [1,0.5,0.5]
colors[1,:] = [0.5,1,0.5]
colors[2,:] = [0.5,0.5,1]

black = [0,0,0]

x = knn.data[:,0]
y = knn.data[:,1]

trainX = knn.data[::2,1:3]
trainY = knn.target[::2]

testX = knn.data[1::2,1:3]
testY = knn.target[1::2]

knn.Use_K_Of(15)
knn.Fit(trainX,trainY)
[numItems,numFeatures] = knn.data.shape

#for i in range(0,numItems/2):
#	actualClass = testY[i]
#	prediction = int( knn.Predict( testX[i,:] ) )
#	print(actualClass, prediction)


plt.figure()

for i in range(0,numItems/2):
	itemClass = int(trainY[i])
	currColor = colors[itemClass,:]
	plt.scatter(trainX[i,0],trainX[i,1],facecolor=currColor,s=50,edgecolor=black,linewidth=2)

correct = 0
for i in range(0,numItems/2):
	itemClass = int(testY[i])
	prediction = int( knn.Predict( testX[i,:] ) )
	if itemClass == prediction:
		correct += 1
	currColor = colors[itemClass,:]
	edgeColor = colors[prediction,:]
	plt.scatter(testX[i,0],testX[i,1],facecolor=currColor,edgecolor=edgeColor,s=50,linewidth=2)

correct = correct*(200./numItems)
print(correct)
#plt.scatter(trainX[:,0],trainX[:,1],c=trainY)
#plt.scatter(testX[:,0],testX[:,1],c=testY)
plt.show()
