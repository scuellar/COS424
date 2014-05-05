% solves eq. 5 in Y. Koren's paper but without the user bias
% assumption is that users have too few ratings, and therefore estimating
% user biases based off the ratings is not likely to yield representative
% results

function [W,H,mymu,bb] = factorize_no_user_bias(A,k,lambda,lrate,maxiter)

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
% calculate mu
mymu = sum(vals)/len;
% initialize bb
bb = rand(1,c);

for i=1:maxiter
    % calculate error
    for j=1:len
        row = rows(j);
        col = cols(j);
        e(j) = vals(j)-mymu-bb(col)-W(row,:)*H(:,col);
        W(row,:) = W(row,:)+lrate*(e(j)*H(:,col)'-lambda*W(row,:));
        H(:,col) - H(:,col)+lrate*(e(j)*W(row,:)'-lambda*H(:,col));
        bb(col) = bb(col) + lrate*(e(j)-lambda*bb(col));
    end
    %norm(e)
end
W;
H;
bb;
end