% makes predictions based on factorized matrices (does not use biases)

function [predictions] = predict_no_bias(test,U,B)

% find nonzeros
[rows,cols,vals] = find(test);
sz = size(rows);
len = sz(1);

predictions = sparse(rows,cols,zeros(len,1));

for i=1:len
   row = rows(i);
   col = cols(i);
   predictions(row,col) = max(1,min(5,U(row,:)*B(:,col))); 
end

predictions;

end