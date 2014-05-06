% solves eq. 5 in Y. Koren's paper (factorization with biases)
% gives less weight to user biases because users have too few ratings
% (therefore, user bias lambda is 5 times larger than the other lambdas)

function [W,H,bu,bb] = factorize_no_mean(A,k,lambda,lrate,maxiter)

% find nonzeros
[rows,cols,vals] = find(A);
sz = size(rows);
len = sz(1);
% error vector
e = zeros(len,1);
% number of rows and columns
[r,c] = size(A);
% initialize ws and hs
W = rand(r,k);
H = rand(k,c);
% initialize bu and bb
bu = rand(r,1);
bb = rand(1,c);

for i=1:maxiter
    for j=1:len
        row = rows(j);
        col = cols(j);
        e(j) = vals(j)-bu(row)-bb(col)-W(row,:)*H(:,col);
        W(row,:) = W(row,:)+lrate*(e(j)*H(:,col)'-lambda*W(row,:));
        H(:,col) = H(:,col)+lrate*(e(j)*W(row,:)'-lambda*H(:,col));
        bu(row) = bu(row) + lrate*(e(j)-lambda*5*bu(row));
        bb(col) = bb(col) + lrate*(e(j)-lambda*bb(col));
    end
    norm(e)
end
W;
H;
bu;
bb;
end