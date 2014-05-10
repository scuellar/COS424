import numpy as np

def factorize_bias(A,k,lam,lrate,maxiter):
    #remove None entrie
    #noZeros(A)
    # find nonzeros
    (rows,cols) = np.nonzero(A);
    print "rows: ", rows
    print "cols: ", cols
    vals = np.array([ A[rows[i]][cols[i]] for i in range(len(rows))])
    print "vals: ", vals
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
    for i in range(maxiter):
        for j in range(leng):
            row = rows[j]
            col = cols[j]
            e[j,0] = vals[j]-mymu-bu[row,0]-bb[0,col]-np.dot(W[row,:], H[:,col])
            W[row,:] = W[row,:] + np.dot(lrate, np.dot( e[j,0], np.transpose(H[:,col]) - np.dot(lam, W[row,:]) ))
            H[:,col] = H[:,col] + np.dot(lrate , (np.dot( e[j,0], np.transpose(W[row,:])-np.dot(lam, H[:,col]) ) ) )
            bu[row,0] = bu[row,0] + lrate*(e[j,0]-lam*bu[row,0])
            bb[0,col] = bb[0,col] + lrate*(e[j,0]-lam*bb[0,col])
        print np.linalg.norm(e)

    return (W,H,mymu,bu,bb)


factorize_bias(np.array([[1,2,3],[0, 2,0],[1,0,0]]),2,5,.001,5)
