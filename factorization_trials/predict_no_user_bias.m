% makes predictions based on factorized matrices and biases (does not use
% user bias)


function [predictions] = predict_no_user_bias(test,U,B,mymu,bb)

% find nonzeros
[rows,cols,vals] = find(test);
sz = size(rows);
len = sz(1);

test_sz = size(test);
predictions = sparse([1,test_sz(1)],[1,test_sz(2)],zeros(2,1));

for i=1:len
   row = rows(i);
   col = cols(i);
   predictions(row,col) = max(1,min(5,mymu+bb(col)+U(row,:)*B(:,col))); 
end

predictions;

end