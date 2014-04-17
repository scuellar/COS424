
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

    plt.figure(1)
    plt.plot(x,linear, 'bs', label="Linear error")
    plt.hlines(average(linear),xmin, xmax, 'b', label="Average Linear")
    plt.plot(x,ridge, 'r+', label="Ridge error")
    plt.hlines(average(ridge),xmin, xmax, 'r', label="Average Ridge")
    plt.plot(x,lasso, 'g^', label="Lasso error")
    plt.hlines(average(lasso),xmin, xmax, 'g', label="Average Lasso")
    plt.xlabel('User number')
    plt.ylabel('Error')
    plt.xlim(0., len(x)+2)
    plt.ylim(0.)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    plt.show()

    #displayRegression([1,2],[2.2,3],[2.5, 4])

    
def displayRegressionInOrder(linear, ridge, lasso, users):
    if not (len(linear) == len(ridge) and len(ridge)==len(lasso) and len(lasso)==len(users)):
        print "Samples don't have the sema length. CHECK YOUR WORK"

    reviews_numb = [len(reviews) for user, reviews in users.iteritems()]

    xmin = 0
    xmax = max(reviews_numb) + (max(reviews_numb) - xmin)/25

    plt.figure(2)
    plt.plot(reviews_numb,linear, 'bs', label="Linear error")
    plt.hlines(average(linear),xmin, xmax, 'b', label="Average Linear error")
    plt.plot(reviews_numb,ridge, 'ro', label="Ridge error")
    plt.hlines(average(ridge),xmin, xmax, 'r', label="Average Ridge error")
    plt.plot(reviews_numb,lasso, 'g^', label="Lasso error")
    plt.hlines(average(lasso),xmin, xmax, 'g', label="Average Lasso error")
    plt.xlabel('Number of reviews')
    plt.ylabel('Error')
    plt.xlim(0., xmax)
    plt.ylim(0.)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    plt.show()

    #displayRegression([1,2],[2.2,3],[2.5, 4])

def displayRegressionCompare1(ridge, dumb):
    if not (len(dumb) == len(ridge)):
        print "Samples don't have the sema length. CHECK YOUR WORK"

    xmin = 0
    xmax = len(dumb)+2
    x = [i+1 for i in range(len(dumb))]

    plt.plot(x,ridge, 'bo', label="Average Linear error")
    plt.hlines(average(ridge),xmin, xmax, 'b', label="Ridge error")
    plt.plot(x,dumb, 'rs', label="Yelp error")
    plt.hlines(average(dumb),xmin, xmax, 'r', label="Average Yelp error")
    plt.xlabel('User number')
    plt.ylabel('Error')
    plt.xlim(0., xmax)
    plt.ylim(0.)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    plt.show()
    
def displayRegressionCompare(ridge, dumb, users):
    if not (len(dumb) == len(ridge) and len(ridge)==len(users)):
        print "Samples don't have the sema length. CHECK YOUR WORK"

    reviews_numb = [len(reviews) for user, reviews in users.iteritems()]

    xmin = 0
    xmax = max(reviews_numb) + (max(reviews_numb) - xmin)/25

    plt.plot(reviews_numb,ridge, 'bo', label="Average Linear error")
    plt.hlines(average(ridge),xmin, xmax, 'b', label="Ridge error")
    plt.plot(reviews_numb,dumb, 'rs', label="Yelp error")
    plt.hlines(average(dumb),xmin, xmax, 'r', label="Average Yelp error")
    plt.xlabel('Number of reviews')
    plt.ylabel('Error')
    plt.xlim(0., xmax)
    plt.ylim(0.)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    plt.show()

    #displayRegression([1,2],[2.2,3],[2.5, 4])
