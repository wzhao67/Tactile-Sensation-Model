import theano
from theano import tensor as T
import numpy as np
import matplotlib.pyplot as pl
import skimage.filters
import skimage.io
from Tkinter import *
from DataGenerator import *
from ANNUI import *
from ANNTools import *

#create UI
root = Tk()
root.title("SA1 Afferent Model using an ANN")
root.geometry("600x250")
app = UI(root)
root.mainloop()

#Set variables 
unlabelled_flags = app.unlabelled_inputs
labelled_flags = app.labelled_inputs
hu = app.num_hidden_units
pxsigma = app.pixelation_sigma
unlabelled_epochs = app.unlabelled_epochs
labelled_epochs = app.labelled_epochs
unlabelled_lambda = app.unlabelled_lambda
labelled_lambda = app.labelled_lambda
unlabelled_LR = app.unlabelled_LR
labelled_LR = app.labelled_LR

'''
Input data
'''
#initialize unlabelled input data

if(pxsigma == 0 and unlabelled_epochs != 0):

    unlabelled_data = np.zeros((1, 784))

    if 0 in unlabelled_flags:
        num_single_points = app.num_SPs
        mul = (int) (num_single_points/784)
        single_pt_data = gen_one_point_inputs_unlabelled(sigma = app.unlabelled_sigma, multiplier = mul)
        unlabelled_data = np.concatenate((unlabelled_data, single_pt_data))
    if 1 in unlabelled_flags:
        mixed_pt_data, _ = gen_one_and_two_point_inputs_labelled_set_two_points(sigma = app.unlabelled_sigma)
        unlabelled_data = np.concatenate((unlabelled_data, mixed_pt_data))
    if 2 in unlabelled_flags:
        alpha_data, _ = gen_labelled_training_alphabets()
        alpha_data = alpha_data[:31200]
        unlabelled_data = np.concatenate((unlabelled_data, alpha_data))
    if 3 in unlabelled_flags:
        braille_data, _ = gen_labelled_training_braille()
        braille_data = braille_data[:31200]
        unlabelled_data = np.concatenate((unlabelled_data, braille_data))

    unlabelled_data = unlabelled_data[1:]
    temp = list(unlabelled_data)
    random.shuffle(temp)
    trX_u = np.asarray(temp)

#initialize labelled input data
labelled_data_X = np.zeros((1, 784))
labelled_data_Y = np.zeros((1, 26))

if 1 in labelled_flags:
    mixed_pt_data_X, mixed_pt_data_Y = gen_one_and_two_point_inputs_labelled_set_two_points(sigma = app.labelled_sigma)
    labelled_data_X = np.concatenate((labelled_data_X, mixed_pt_data_X))
    labelled_data_Y = np.concatenate((labelled_data_Y, mixed_pt_data_Y))
if 2 in labelled_flags:
    alpha_data_X, alpha_data_Y = gen_labelled_training_alphabets()
    alpha_data_X, alpha_data_Y = alpha_data_X[:31200], alpha_data_Y[:31200]
    labelled_data_X = np.concatenate((labelled_data_X, alpha_data_X))
    labelled_data_Y = np.concatenate((labelled_data_Y, alpha_data_Y))
if 3 in labelled_flags:
    braille_data_X, braille_data_Y = gen_labelled_training_braille()
    braille_data_X, braille_data_Y = braille_data_X[:31200], braille_data_Y[:31200]
    labelled_data_X = np.concatenate((labelled_data_X, braille_data_X))
    labelled_data_Y = np.concatenate((labelled_data_Y, braille_data_Y))

#release GUI window
app.quit()

labelled_data_X = labelled_data_X[1:]
labelled_data_Y = labelled_data_Y[1:]
temp = list(zip(labelled_data_X, labelled_data_Y))
random.shuffle(temp)
temp_X, temp_Y = zip(*temp)
trX_l = np.asarray(temp_X)
trY_l = np.asarray(temp_Y)
    

#helper functions
def floatX(X):
    return np.array(X, dtype=theano.config.floatX)

def init_weights(shape):
    return theano.shared(floatX(np.absolute(np.random.randn(*shape)*0.01)))    

def rectify(X):
    return T.maximum(X,0.)
 
#theano declarations
X = T.fmatrix()
Y = T.fmatrix()

'''
Autoencoder layers (only if no pixelation enforcement)
'''        
if(pxsigma == 0 and unlabelled_epochs != 0):

    def sgd(cost, params, reg, lr=unlabelled_LR):
        grads = T.grad(cost=cost, wrt = params)
        updates=[]
        for p,g in zip(params, grads):
            updates.append((p,(p-g*lr-reg*lr)))
        return updates

    def model(X,w_h,w_o):
        h = rectify(T.dot(X,w_h))
        pyx = T.nnet.softmax(T.dot(h,w_o))
        return pyx
        
    def Regularizer(w_h, w_o, lambda_l1=unlabelled_lambda):
        return lambda_l1*((w_h.get_value().mean() + w_o.get_value().mean())/2)    

    w_h = init_weights((784, hu))
    w_o = init_weights((hu, 784))
    
    #Learning parameters
    pred_y = model(X, w_h, w_o)
    cost = T.mean(T.nnet.categorical_crossentropy(pred_y,Y)) + Regularizer(w_h,w_o)
    params = [w_h, w_o]
    updates = sgd(cost, params, Regularizer(w_h,w_o))

    #theano functions
    train = theano.function(inputs=[X,Y], outputs=cost, updates=updates, allow_input_downcast=True)
    predict = theano.function(inputs = [X], outputs = pred_y, allow_input_downcast=True)
    cc_u=[] #check this for convergence

    #Training time!
    for i in range(unlabelled_epochs):
        for start, end in zip(range(0,len(trX_u),256), range(256,len(trX_u),256)):
            cost = train(trX_u[start:end], trX_u[start:end])
        cc_u.append(cost)
        print i, cost

else:
    w_h = init_weights_regular_pixels((784, hu), sigma = pxsigma)
    w_o = init_weights((hu, 784))

'''
Classifier layers
'''
###new definition for our model and regularizer

def sgd(cost, params, reg, lr=labelled_LR):
    grads = T.grad(cost=cost, wrt = params)
    updates=[]
    for p,g in zip(params, grads):
        updates.append((p,(p-g*lr-reg*lr)))
    return updates
        
def model(X, w_h, w_o, w_o2):
    h = rectify(T.dot(X,w_h))
    o = rectify(T.dot(h,w_o))
    pyx = T.nnet.softmax(T.dot(o,w_o2))
    return pyx
    
def Regularizer(w_o, w_o2, lambda_l1=labelled_lambda):
    return lambda_l1*((w_o.get_value().mean() + w_o2.get_value().mean())/2)

w_o2 = init_weights((784,26))
pred_y = model(X, w_h, w_o, w_o2)
cost = T.mean(T.nnet.categorical_crossentropy(pred_y,Y)) + Regularizer(w_o, w_o2)
params = [w_o, w_o2]
updates = sgd(cost, params, Regularizer(w_o, w_o2))
train = theano.function(inputs=[X,Y], outputs=cost, updates=updates, allow_input_downcast=True)
predict = theano.function(inputs = [X], outputs = pred_y, allow_input_downcast=True)
cc_l=[] #check this for convergence

for i in range(labelled_epochs):
    for start, end in zip(range(0,len(trX_l),256), range(256,len(trY_l),256)):
        cost = train(trX_l[start:end], trY_l[start:end])
    cc_l.append(cost)
    print i, cost


'''
Network tests: Alpha classify, Braille classify, Mixed classify, TPDT
'''

#testing data
alpha_teX, alpha_teY = gen_labelled_testing_alphabets()

braille_teX, braille_teY = gen_labelled_testing_braille()

mixed_teX = np.concatenate((alpha_teX, braille_teX))
mixed_teY = np.concatenate((alpha_teY, braille_teY))
temp = list(zip(mixed_teX, mixed_teY))
random.shuffle(temp)
mixed_teX, mixed_teY = zip(*temp)
mixed_teX = np.asarray(mixed_teX)[:7800]
mixed_teY = np.asarray(mixed_teY)[:7800]

#alphabet accuracy test
alpha_acc = np.mean(np.argmax(alpha_teY, axis=1) == np.argmax(predict(alpha_teX), axis=1)) * 100

#braille accuracy test
braille_acc = np.mean(np.argmax(braille_teY, axis=1) == np.argmax(predict(braille_teX), axis=1)) * 100

#mixed accuracy test
mixed_acc = np.mean(np.argmax(mixed_teY, axis=1) == np.argmax(predict(mixed_teX), axis=1)) * 100

#TPDT
TPDT_results_X=[]
TPDT_results_Y=[]

for i in range(2,24,2):

    TPDT_teX, TPDT_teY = gen_inputs_for_TPDT(dist=i)
    TPDT_results_X.append(i)
    
    predicted = predict(TPDT_teX)
    modified_predicted = np.zeros((len(TPDT_teX), 2))
    
    for j in range(len(predicted)):
    
        if(predicted[j][:13].sum() > predicted[j][13:].sum()):
            modified_predicted[j][0] = 1
        else:
            modified_predicted[j][1] = 1
    
    predicted_indices = np.argmax(modified_predicted, axis=1)
    TPDT_data_Y_indices = np.argmax(TPDT_teY, axis=1)
    
    conmat = np.zeros(4)
    for j in range(len(predicted_indices)):
        if(predicted_indices[j]==1 and TPDT_data_Y_indices[j]==1): conmat[0] = conmat[0]+1
        elif(predicted_indices[j]==1 and TPDT_data_Y_indices[j]==0): conmat[1] = conmat[1]+1
        elif(predicted_indices[j]==0 and TPDT_data_Y_indices[j]==1): conmat[2] = conmat[2]+1
        elif(predicted_indices[j]==0 and TPDT_data_Y_indices[j]==0): conmat[3] = conmat[3]+1
        
    print (float)((conmat[0]+conmat[3])/(conmat[0]+conmat[1]+conmat[2]+conmat[3]))
    TPDT_results_Y.append((float)((conmat[0]+conmat[3])/(conmat[0]+conmat[1]+conmat[2]+conmat[3])))
    
pl.plot(TPDT_results_X, TPDT_results_Y)    
TPDT_four_acc = TPDT_results_Y[1]

#Network internal metrics
L1L2cor = L1_L2_correlation(w_h, w_o)
L1PxArr = np.asarray(L1_pixelation_score_array(w_h))
L1PxScore = np.mean(L1PxArr)
L2PxArr = np.asarray(L2_pixelation_score_array(w_o))
L2PxScore = np.mean(L2PxArr)


#print summary
np.set_printoptions(precision = 3, linewidth = 10000)
    
print "**********SUMMARY************************"
print "Unlabelled input flags: ", unlabelled_flags
print "Labelled input flags: ", labelled_flags
print "Num of hidden units: ", hu
print "Pixelation: ", pxsigma
print "Unlabelled epochs: ", unlabelled_epochs
print "Labelled epochs: ", labelled_epochs
print "Unlabelled Lambda: ", unlabelled_lambda
print "Labelled Lambda: ", labelled_lambda
print "Unlabelled LR: ", unlabelled_LR
print "Labelled LR: ", labelled_LR

print "*********INTERNAL METRICS***************"
print "L1L2 Correlation: ", L1L2cor
print "L1 Px Score: ", L1PxScore
print "L2 Px Score: ", L2PxScore
print "L1 Px Array: ", L1PxArr
print "L2 Px Array: ", L2PxArr

print "*********TESTS**************************"
print "Alphabet Classification: ", alpha_acc
print "Braille Classification: ", braille_acc
print "Mixed Classification: ", mixed_acc
print "TPDT: ", TPDT_results_Y
print "TPDT at dist=4: ", TPDT_four_acc
