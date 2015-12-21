# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 12:07:28 2015

@author: charlie
"""
import theano
from theano import tensor as T
import numpy as np
import skimage.filters
import skimage.transform
#import math
import matplotlib.pylab as pl
import random
import scipy.stats as ss
import sklearn.metrics as sm
import numpy.fft as fft
#%pylab

'''
Initialize random weights
'''
def init_weights(shape):
    return theano.shared(floatX(np.absolute(np.random.randn(*shape)*0.01)))

'''
Initialize randomly pixelated weights
'''
def init_weights_random_pixels(shape, sigma=2.0):
    x,y = shape
    weights=np.zeros((y,x))
    pixel = np.zeros((28,28))
    pixel[14][14] = 1
    pixel = skimage.filters.gaussian_filter(pixel, sigma)
    for i in range(weights.shape[0]):
        trans_x = np.random.randn()*5
        trans_y = np.random.randn()*5
        translate_params = skimage.transform.AffineTransform(translation=(trans_x,trans_y))
        translated_pixel = skimage.transform.warp(pixel, translate_params)
        translated_pixel = translated_pixel.reshape(784)
        weights[i] = translated_pixel
    return theano.shared(floatX(np.absolute(weights.transpose())))

'''
Initialize spacially optimized pixelated weights
'''
def init_weights_regular_pixels(shape, sigma=2.0):
    x,y = shape #x = 784, y = hidden unit size
    dist = (int)(x/y)
    d=0
    weights = np.zeros((x,y))
    for i in range(0,y):
        pixel = np.zeros(784)
        pixel[d] = 1
        pixel = skimage.filters. gaussian_filter(pixel.reshape(28,28), sigma)
        weights.transpose()[i] = pixel.reshape(784)
        d = d+dist
    return theano.shared(floatX(np.absolute(weights)))

'''
Display layer 1 weights
'''
def display_L1_weights(w_h, row=7, col=12): 
    
    if(w_h.get_value().shape[1] == 84):
        row = 7
        col = 12
    if(w_h.get_value().shape[1] == 42):
        row = 6
        col = 7    
     
    fig, figarr=pl.subplots(row,col)
    for i in range(0,row):
        for j in range(0,col):
            figarr[i][j].matshow(w_h.get_value().transpose()[i*col+j].reshape(28,28)) 

def display_L2_weights(w_o, row=7, col=12):  

   if(w_o.get_value().shape[0] == 84):
        row = 7
        col = 12
   if(w_o.get_value().shape[0] == 42):
        row = 6
        col = 7     

   fig, figarr=pl.subplots(row,col)
   w_o = w_o.get_value().transpose()
   for i in range(0,row):
       for j in range(0,col):
           figarr[i][j].matshow(w_o.get_value()[i*col+j].reshape(28,28)) 

'''
Display input data
'''
def display_input_data(data, x=2, y=4):
    fig, figarr=pl.subplots(x,y)
    for i in range(x):
        for j in range(y):
            figarr[i][j].matshow(data[i*y+j].reshape(28,28))

'''
Display predictions of autoencoder
'''
def display_autoencoder_results(testing_data, begin=0, end=10):
    fig, figarr = pl.subplots(2, end-begin)
    for i in range(begin, end):
        figarr[0][i].matshow(testing_data[i].reshape(28,28))
        figarr[1][i].matshow(predict(testing_data)[i].reshape(28,28))

'''
Find the pearson correlation of l1 and l2 weights
'''
def L1_L2_correlation(w_h, w_o, hu=84):
    
    correlation = 0;    
    
    for i in range(1000):
        ran = random.randint(0, hu-1)
        l1 = w_h.get_value().transpose()[ran]
        l2 = w_o.get_value()[ran]
        correlation = correlation + ss.pearsonr(l1,l2)[0]
    return correlation/1000    

def L1_pixelation_score_array(w_h):
    
    hu = w_h.get_value().shape[1]
    score_array = []
    
    for i in range(hu):
        field = w_h.get_value().transpose()[i]
        maximum = max(field)
        mean = np.mean(field)
        stddev = np.std(field)
        score_array.append((maximum-mean)/stddev)
        
    return score_array
    
def L2_pixelation_score_array(w_o):
    
    hu = w_h.get_value().shape[0]
    score_array = []

    for i in range(hu):
        field = w_h.get_value()[i]
        maximum = max(field)
        mean = np.mean(field)
        stddev = np.std(field)
        score_array.append((maximum-mean)/stddev)
        
    return score_array
    

'''
Alphabet confusion matrix from paper
'''
def human_alphabet_confusion_matrix():
    return np.array(
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
