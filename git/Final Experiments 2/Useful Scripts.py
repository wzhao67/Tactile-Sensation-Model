

************Visualizing POINT predicted results:
for i in range(0, 3):
	pl.matshow(testing_data[i].reshape(28,28));
	pl.matshow(predict(testing_data)[i].reshape(28,28));

**************Visualize weights coming out of input unit 0:
pl.matshow(w_h.get_value()[0].reshape(28,28))

**************Visualize weights going into hidden unit 0:
pl.matshow(w_h.get_value().transpose()[0].reshape((28,28)))

*************Show images as part of subplots:
fig, figarr = pl.subplots(2,2)
figarr[0,0].matshow(data[0])

*************For instance:
fig, figarr=pl.subplots(5,5)
for i in [0,1,2,3,4]:
	for j in [0,1,2,3,4]:
		figarr[i][j].matshow(data[i*5+j])

**************Showing alphabet predicted results:
fig, figarr=pl.subplots(2,5)
for i in [0,1,2,3,4]:
	figarr[0][i].matshow(testing_data[i].reshape(28,28))
	figarr[1][i].matshow(predict(testing_data)[i].reshape(28,28))

**************Show input invisualizations:
fig, figarr=pl.subplots(3,3)
figarr[0][0].matshow(teX[0].reshape(28,28))
figarr[0][1].matshow(teX[1].reshape(28,28))
figarr[0][2].matshow(teX[2].reshape(28,28))
figarr[1][0].matshow(teX[3].reshape(28,28))
figarr[1][1].matshow(teX[4].reshape(28,28))
figarr[1][2].matshow(teX[5].reshape(28,28))
figarr[2][0].matshow(teX[6].reshape(28,28))
figarr[2][1].matshow(teX[7].reshape(28,28))
figarr[2][2].matshow(teX[8].reshape(28,28))

**************Visualize weights (of 70 hidden units):
row=2; col=4
fig, figarr=pl.subplots(row,col)
for i in range(0,row):
	for j in range(0,col):
		a=[]
		for k in range(0,784): a.append(w_h.get_value()[k][i*col+j])
		a = np.array(a)
		figarr[i][j].matshow(a.reshape(28,28))

Visualize output weights

********************Significance of results
import numpy
from sklearn import svm
from sklearn import cross_validation

mat = teX
nulldist=[]
for i in range(1000):
        if i%100==0:
                print i
               
        labels=numpy.random.permutation(teY)
        clf = svm.SVC(kernel='linear', C=1)
        scores = cross_validation.cross_val_score(clf, mat, labels, cv=12)
        nulldist.append(scores.mean())
       
hist(nulldist)  


********************Frobenius distance
target_matrix = np.array(
[[71,1,0,0,0,1,0,0,0,1,3,1,2,8,0,0,0,5,0,0,0,3,1,2,0,1],
[2,18,2,27,1,0,5,2,0,0,1,0,2,6,6,4,3,6,3,0,6,0,1,0,0,0],
[0,1,46,3,0,0,15,0,0,0,0,0,0,0,15,0,15,2,1,0,2,0,0,0,0,0],
[1,2,2,49,1,0,2,1,0,0,0,0,1,0,22,5,4,1,1,0,7,0,1,0,0,0],
[2,6,1,1,60,2,1,2,0,0,8,0,1,2,0,0,1,8,1,0,1,1,1,1,0,1],
[1,1,0,0,7,57,1,1,1,0,4,0,0,2,0,11,0,3,3,2,0,2,0,1,2,0],
[1,11,2,3,1,0,41,0,0,0,0,0,4,1,6,1,18,6,5,0,0,0,0,0,0,0],
[1,1,0,1,1,1,1,49,0,0,4,0,9,15,0,1,1,5,0,0,6,1,4,1,0,0],
[0,0,0,0,0,0,0,0,98,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,1,0,1,1,1,1,0,1,84,1,0,0,0,0,0,0,0,3,0,1,1,0,1,1,2],
[1,1,2,0,10,1,0,0,0,0,57,0,3,1,0,1,0,9,0,0,1,0,2,7,0,4],
[1,0,1,0,0,0,0,0,0,1,1,93,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
[1,4,0,0,2,1,2,2,0,0,8,0,34,4,0,0,1,5,1,0,6,1,30,0,0,0],
[0,5,0,1,1,1,0,12,0,0,7,0,20,15,0,1,0,9,2,0,4,0,19,2,0,0],
[0,1,2,6,0,0,4,0,0,0,0,0,0,0,83,1,3,0,0,0,0,0,0,0,0,0],
[0,2,1,1,1,23,2,1,0,0,3,0,0,2,0,44,1,2,4,5,0,3,1,0,4,1],
[0,2,2,8,0,0,7,0,0,0,0,0,0,1,49,1,28,1,1,0,0,0,0,0,0,0],
[6,4,1,4,1,0,2,17,0,0,3,0,8,14,1,2,0,31,0,0,4,0,1,0,0,0],
[0,21,2,6,2,0,14,1,0,0,1,1,2,1,5,3,6,8,25,0,1,0,2,0,0,1],
[1,1,1,0,0,2,0,0,1,1,1,1,1,0,0,1,0,0,3,61,0,2,0,4,15,3],
[0,1,0,2,0,0,1,1,0,0,0,0,1,1,2,1,1,1,1,0,80,4,2,0,0,1],
[0,0,0,1,0,0,0,0,0,0,3,0,0,2,0,2,0,0,1,0,3,62,3,1,21,1],
[1,1,0,0,1,1,1,1,0,0,3,0,11,2,0,1,0,1,2,0,1,1,71,0,0,1],
[1,1,1,0,5,1,0,0,0,1,11,0,2,1,0,0,1,3,1,1,0,0,2,57,1,12],
[0,0,0,0,0,2,1,0,0,2,5,0,1,2,0,1,0,1,1,6,0,15,0,3,58,3],
[1,0,0,0,3,3,1,1,1,2,7,0,0,1,0,0,0,2,1,2,0,0,1,31,2,41]])

confusion_matrix = np.zeros((26,26))
predicted_all = predict(teX)
for i in range(0,len(teX)):
	confusion_matrix[np.argmax(teY[i])][predicted_all[i]] +=1  
confusion_matrix = (confusion_matrix/300)*100
print np.linalg.norm(target_matrix-confusion_matrix)

