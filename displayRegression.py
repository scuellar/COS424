
import numpy as np
import matplotlib.pyplot as plt

def average(l):
    return float(sum(l))/len(l)
    
def displayRegression(linear, ridge, lasso):
    if not (len(linear) == len(ridge) and len(ridge)==len(lasso)):
        print "Samples don't have the sema length. CHECK YOUR WORK"
        
    x = [i+1 for i in range(len(linear))]
    xmin = 0
    xmax = len(x)+2

    plt.plot(x,linear, 'bs',)
    plt.hlines(average(linear),xmin, xmax, 'b')
    plt.plot(x,ridge, 'r+')
    plt.hlines(average(ridge),xmin, xmax, 'r')
    plt.plot(x,lasso, 'g^')
    plt.hlines(average(lasso),xmin, xmax, 'g')
    plt.xlabel('User number')
    plt.ylabel('Error')
    plt.xlim(0., len(x)+2)
    plt.ylim(0.)

    plt.show()

    #displayRegression([1,2],[2.2,3],[2.5, 4])

    
def displayRegressionInOrder(linear, ridge, lasso, users):
    if not (len(linear) == len(ridge) and len(ridge)==len(lasso) and len(lasso)==len(users)):
        print "Samples don't have the sema length. CHECK YOUR WORK"

    reviews_numb = [len(reviews) for user, reviews in users.iteritems()]

    xmax = max(reviews_numb)
    xmin = 0
    
    plt.plot(reviews_numb,linear, 'bs',)
    plt.hlines(average(linear),xmin, xmax, 'b')
    plt.plot(reviews_numb,ridge, 'r+')
    plt.hlines(average(ridge),xmin, xmax, 'r')
    plt.plot(reviews_numb,lasso, 'g^')
    plt.hlines(average(lasso),xmin, xmax, 'g')
    plt.xlabel('User number')
    plt.ylabel('Error')
    plt.xlim(0., xmax)
    plt.ylim(0.)

    plt.show()

    #displayRegression([1,2],[2.2,3],[2.5, 4])
