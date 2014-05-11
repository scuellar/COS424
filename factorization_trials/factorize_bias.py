import numpy as np

def factorize_bias(A,k,lam,lrate,maxiter):
    #remove None entrie
    #noZeros(A)
    # find nonzeros
    #print A.shape
    (rows,cols) = A.nonzero() #np.nonzero(A);
    vals = np.array([ A[rows[i], cols[i]] for i in range(len(rows))])
    #print "vals: ", vals
    #Check there is no None!
    # Assume A has
    leng = len(rows);
    # error vector
    e = np.zeros((leng, 1))
    # number of rows and columns
    (r,c) = A.shape
    # initialize ws and hs
    W = np.random.rand(r,k)
    H = np.random.rand(k,c)
    # calculate mu
    sm_vals = [val/leng for val in vals];
    #Check there is no None!
    #sm_vals(isnan(sm_vals))=0;
    mymu = sum(sm_vals);
    # initialize bu and bi
    bu = np.random.rand(r,1)
    bb = np.random.rand(1,c)
    #print "Enter loop"
    log = []
    for i in range(maxiter):
        for j in range(leng):
            row = rows[j]
            col = cols[j]
            try:
                e[j,0] = vals[j]-mymu-bu[row,0]-bb[0,col]-np.dot(W[row,:], H[:,col])
                factor = e[j,0]* lrate 
                W[row,:] = W[row,:] + np.dot(factor, np.transpose(H[:,col]) - np.dot(lam, W[row,:]) )
                H[:,col] = H[:,col] + np.dot(factor, np.transpose(W[row,:]) - np.dot(lam, H[:,col]) ) 
            except IndexError:
                print "here is the error!"
            try:
                bu[row,0] = bu[row,0] + lrate*(e[j,0]-lam*bu[row,0])
                bb[0,col] = bb[0,col] + lrate*(e[j,0]-lam*bb[0,col])
            except IndexError:
                print "here is the error!2"
        log.append(int(np.linalg.norm(e)))
    print "Done factorizing. Aprox errors ", log 
    return (W,H,mymu,bu,bb)


#from scipy import io
#import scipy as sp
#np.seterr(all='print')
#M = sp.io.mmread("fact_ratings_matrix.mtx")
#N = M.todok()
#(W,H,mymu,bu,bb) = factorize_bias(N,10,0.2,.001,40)
