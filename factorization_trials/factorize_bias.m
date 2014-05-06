% solves eq. 5 in Y. Koren's paper (factorization with biases)

function [W,H,mymu,bu,bb] = factorize_bias(A,k,lambda,lrate,maxiter)

% find nonzeros
[rows,cols,vals] = find(A);
vals(isnan(vals)) = 0;
sz = size(rows);
len = sz(1);
% error vector
e = zeros(len,1);
% number of rows and columns
[r,c] = size(A);
% initialize ws and hs
W = rand(r,k);
H = rand(k,c);
% calculate mu
sm_vals = vals/len;
sm_vals(isnan(sm_vals))=0;
mymu = sum(sm_vals);
% initialize bu and bi
bu = rand(r,1);
bb = rand(1,c);

for i=1:maxiter
    for j=1:len
        row = rows(j);
        col = cols(j);
        e(j) = vals(j)-mymu-bu(row)-bb(col)-W(row,:)*H(:,col);
        W(row,:) = W(row,:)+lrate*(e(j)*H(:,col)'-lambda*W(row,:));
        H(:,col) = H(:,col)+lrate*(e(j)*W(row,:)'-lambda*H(:,col));
        bu(row) = bu(row) + lrate*(e(j)-lambda*bu(row));
        bb(col) = bb(col) + lrate*(e(j)-lambda*bb(col));
    end
    norm(e)
end
W;
H;
bu;
bb;
end