% calculates mean squared error and mean absolute error between test and
% predictions matrices

function [mse,mae] = calculate_error(test,predictions)

[rows,cols,vals] = find(test);
len = size(vals,1);

diff = test-predictions;

mse = sqrt(norm(diff,'fro')^2/len);
mae = sum(sum(abs(diff)))/len;

end