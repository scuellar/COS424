% solves eq. 2 in Y. Koren's paper

function [W,H] = factorize(A,k,lambda,lrate,maxiter)

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

for i=1:maxiter
    % calculate error
    for j=1:len
        row = rows(j);
        col = cols(j);
        e(j) = vals(j)-W(row,:)*H(:,col);
        W(row,:) = W(row,:)+lrate*(e(j)*H(:,col)'-lambda*W(row,:));
        H(:,col) - H(:,col)+lrate*(e(j)*W(row,:)'-lambda*H(:,col));
    end
    norm(e)
end
W;
H;
end